#! /usr/bin/env python3

import os
import sys
import time
import signal
import logging
import asyncio
import shutil
import subprocess

from threading import Thread

import uinput
from usb import core

from lib.configparser import *
from lib.pynotifier import Notification
from lib.inotify_simple import INotify, flags
from lib.hid import Device as HIDDevice, HIDFailedToOpenException
import lib.hid as hid

from lib.openrgb.orgb import OpenRGBClient

from devices.keyboard import SUPPORTED_DEVICES, KeyboardInterface
from devices.allkeys import *

currProfile = MEMORY_1

RETRY_COUNT = 5
RETRY_TIMEOUT = 5 # in seconds
USB_TIMEOUT = 1000 # in milliseconds

APP_NAME = "Keyboard Center Service"

PARENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_LOCATION = os.path.join(
    PARENT_LOCATION, "config", "testconfig-example.yaml"
)
ICON_LOCATION = os.path.join(
    PARENT_LOCATION, "assets", "input-keyboard-virtual.png"
)

def _stop(*args):
    global evLoop
    global attachDriver

    logging.info("stopping...")

    try:
        attachDriver()
    except NameError:
        # is not defined when using HID interface
        pass
    evLoop.stop()
    virtualKeyboard.destroy()

def setOpenRGBProfile(profile: str, retry: int, first: bool):
    try:
        client = OpenRGBClient()
        client.load_profile(profile)
    except ConnectionRefusedError:
        if retry <= 0 or not first:
            return
        #if retry == RETRY_COUNT and shutil.which("openrgb"):
        #    subprocess.Popen(["openrgb", "--server"], shell=False)
        logging.debug("Could not reach OpenRGB SDK, retrying...")
        time.sleep(RETRY_TIMEOUT)
        setOpenRGBProfile(profile, retry-1)
    except ValueError as e:
        logging.error(str(e))

def _sendData(hdev: HIDDevice, data: bytes, useWrite: bool=True):
    if useWrite:
        hdev.write(data)
    else:
        hdev.send_feature_report(data)

async def disableGkeyMapping(keyDev: KeyboardInterface, HIDpath: str):
    logging.debug("Sending sequence to disable G keys")
    with HIDDevice(path=HIDpath) as hdev:
        for data in keyDev.disableGKeys:
            _sendData(hdev, data, keyDev.disableGKeysUseWrite)

def switchProfile(profile: str,
                    keyDev: KeyboardInterface, HIDpath: str=None,
                    first=False):
    global currProfile
    currProfile = profile

    # switch Mkey LED
    if HIDpath and not keyDev.useLibUsb and keyDev.memoryKeysLEDs:
        with HIDDevice(path=HIDpath) as hdev:
            hdev.nonblocking = True
            _sendData(hdev,
                keyDev.memoryKeysLEDs[profile],
                keyDev.disableGKeysUseWrite
            )

    # set openRGB profile
    Thread(target=setOpenRGBProfile, args=(profile, RETRY_COUNT, first), daemon=True).start()

    path = os.path.join(
        PARENT_LOCATION,
        "assets", f"{profile}.png"
    )
    #logging.debug("notification icon path " + path)
    #logging.debug("triggering notification")

    Notification(
        app_name=APP_NAME,
        title=f"Switched to profile {profile}",
        icon_path=path,
        urgency="normal"
    ).send_linux() # this shit is targeted at linux only fuck anything else

def executeMacro(macro: list):
    for action in macro:
        if len(action) == 1:
            if action[0][0] == TYPE_CLICK:
                virtualKeyboard.emit_click(action[0])
            elif action[0][0] == TYPE_DELAY:
                time.sleep(action[0][1] / 1000)
            
        elif all([ x[0] == TYPE_CLICK for x in action ]):
            virtualKeyboard.emit_combo(action)
        else:
            logging.error("unknown keyboard action...."+str(action))

def emitKeys(profile, key, uinput=False):
    """ 
    Function that emits the requested keys

    this function can be blocking
    """
    logging.debug(f"{key} pressed")

    if uinput:
        type, macro = TYPE_KEY, key
    else:
        type, macro = config.getKey(profile, key)

    if type == TYPE_KEY and macro:
        virtualKeyboard.emit_click(macro)

    elif type == TYPE_COMBO and macro:
        virtualKeyboard.emit_combo(macro)

    elif type == TYPE_MACRO and macro:
        print(macro)
        executeMacro(macro)

async def handleRawData(fromKeyboard, 
                    keyboardDev: KeyboardInterface,
                    HIDpath: str=None):

    data = bytes(fromKeyboard)
    #print(data)
    pressed = keyboardDev.macroKeys.get(data)

    if data in keyboardDev.macroKeys:
        if pressed:
            if isinstance(pressed, str):
                Thread(target=emitKeys, args=(currProfile,pressed), daemon=True).start()
            else: # uinput key
                Thread(target=emitKeys, args=(currProfile,pressed,True), daemon=True).start()
        else:
            pass
            #logging.debug("recieved data could not get mapped to a macro key")
            #logging.debug(data)

    elif data in keyboardDev.memoryKeys:
        Thread(target=switchProfile, args=(keyboardDev.memoryKeys[data],keyboardDev, HIDpath), daemon=True).start()

    elif keyboardDev.useLibUsb and data in keyboardDev.mediaKeys:
        Thread(target=emitKeys, args=(currProfile,pressed,True), daemon=True).start()
    else:
        pass    

async def usbListener(keyboard: core.Device,
                keyboardEndpoint: core.Endpoint,
                keyboardDev: KeyboardInterface,
                HIDpath: str=None,
                HIDpath_disable: str=None):

    _usbTimeout: int = config.settings["settings"].get("usbTimeout") or USB_TIMEOUT

    await asyncio.sleep(0)
    
    # Send the sequence to disable the G keys
    if keyboardDev.disableGKeys:
        await disableGkeyMapping(keyboardDev, HIDpath_disable)

    if not keyboardDev.useLibUsb:
        with HIDDevice(path=HIDpath) as hdev:
            hdev.nonblocking = True

            # give visual feedback that application is now running
            switchProfile(currProfile, keyboardDev, HIDpath_disable, True)

            while True:
                await asyncio.sleep(0)
                try:
                    fromKeyboard = hdev.read(
                        keyboardEndpoint.wMaxPacketSize,
                        _usbTimeout
                    )

                    if fromKeyboard:
                        await handleRawData(fromKeyboard, keyboardDev, HIDpath_disable)
                except hid.HIDException as e:
                    logging.debug(f"HIDerror: probably exiting? ({str(e)})")
    else:
        logging.debug("Using libusb backend...")
        while True:
            await asyncio.sleep(0)
            try:
                # hmm this could end up problematic if it blocks while
                # running slower macros.....might need to go back to Threads
                fromKeyboard = keyboard.read(
                    keyboardEndpoint.bEndpointAddress,
                    keyboardEndpoint.wMaxPacketSize,
                    _usbTimeout
                )

                if fromKeyboard:
                    await handleRawData(fromKeyboard, keyboardDev)
            
            # older versions of python3-usb throw USBError instead of USBTimeoutError
            # all glory to backwards compatibility I guess....
            except core.USBError:
                pass
            except core.USBTimeoutError:
                pass

def inotifyReader(inotify: INotify):
    for _ in inotify.read():
        # reload configuration
        logging.info("config changed - reloading...")
        if config.load():
            Notification(
                app_name=APP_NAME,
                title="Configuration changed",
                description="new config loaded!",
                icon_path=ICON_LOCATION,
                urgency="normal"
            ).send_linux()

def _getHIDpaths(keyboardDev: KeyboardInterface):
    HIDpath, HIDpath_disable = None, None

    for dev in hid.enumerate(keyboardDev.usbVendor, keyboardDev.usbProduct):
        if dev.get("interface_number") == keyboardDev.usbInterface[0]:
            HIDpath: bytes = dev.get("path")
            logging.debug(f"HIDraw read endpoint found: {HIDpath.decode()}")

        if dev.get("interface_number") == keyboardDev.disableGKeysInterface:
            HIDpath_disable: bytes = dev.get("path")
            logging.debug(f"HIDraw disable endpoint found: {HIDpath_disable.decode()}")

    logging.debug("Checking for HID availability...")
    def __HIDavailable(HIDpath: bytes, tries: int) -> bool:
        try:
            with HIDDevice(path=HIDpath) as _:
                logging.debug(f"Connected to {HIDpath.decode()}")
            return True
        except HIDFailedToOpenException:
            if tries <= 0:
                return False
            else:
                logging.warning("Could not open HID device, retrying...")
                time.sleep(RETRY_TIMEOUT)
                return __HIDavailable(HIDpath, tries-1)

    numTries = config.settings["settings"].get("retryCount") or RETRY_COUNT
    if HIDpath and not __HIDavailable(HIDpath, numTries):
        raise HIDFailedToOpenException(f"Unable to open device {HIDpath.decode()}")

    return HIDpath, HIDpath_disable

def main():
    global currProfile

    logging.info("searching for supported keyboard...")

    t1 = time.time()
    for i, device in enumerate(SUPPORTED_DEVICES):
        keyboard: core.Device = core.find(
            idVendor=device.usbVendor, idProduct=device.usbProduct
        )

        if keyboard:
            logging.info("keyboard found: " + device.devicename)
            Notification(
                app_name=APP_NAME,
                title="Keyboard Search",
                description="keyboard found: " + device.devicename,
                icon_path=ICON_LOCATION,
                urgency="low"
            ).send_linux()

            logging.info("saving deviceID into config")
            config.settings["settings"]["usbDeviceID"] = i
            config.save()

            keyboardDev: KeyboardInterface = device
            break
    t2 = time.time()

    if not keyboard:
        logging.critical("no supported keyboard found")
        config.settings["settings"]["usbDeviceID"] = "None"
        config.save()

        Notification(
            app_name=APP_NAME,
            title="Keyboard Search",
            description="no supported keyboard found!",
            icon_path=ICON_LOCATION,
            urgency="critical"
        ).send_linux()

        sys.exit(1)
    else:
        logging.debug(f"time taken to find keyboard in ms: {t2-t1}")

    logging.debug("requesting USB endpoint...")
    keyboardEndpoint: core.Endpoint = keyboard\
                                        [keyboardDev.usbConfiguration]\
                                        [keyboardDev.usbInterface]\
                                        [keyboardDev.usbEndpoint]

    logging.debug("Searching for HIDraw endpoint...")
    HIDpath, HIDpath_disable = _getHIDpaths(keyboardDev)
    
    if not HIDpath or not HIDpath_disable:
        if keyboardDev.useLibUsb:
            logging.warning("HIDraw endpoint could not be found!\n\
                switching to libusb as backup")
        
            logging.debug("check and detach kernel driver if active")
            try:
                if keyboard.is_kernel_driver_active(keyboardDev.usbInterface[0]):
                    keyboard.detach_kernel_driver(keyboardDev.usbInterface[0])
                    global attachDriver
                    attachDriver = lambda: keyboard.attach_kernel_driver(
                        keyboardDev.usbInterface[0]
                    )

            except core.USBError as e:
                print("AAA")
                Notification(
                    app_name=APP_NAME,
                    title="Kernel driver init",
                    description=str(e),
                    icon_path=ICON_LOCATION,
                    urgency="critical"
                ).send_linux()

                Notification(
                    app_name=APP_NAME,
                    title="Kernel driver init",
                    description="Please plug your keyboard out and in again\n\
                        or a restart could solve this issue.",
                    icon_path=ICON_LOCATION,
                    urgency="critical"
                ).send_linux()
                sys.exit(1)
        else:
            logging.error("HIDraw endpoint could not be found!")
            sys.exit(1)

    logging.debug("creating uinput device...")
    global virtualKeyboard
    virtualKeyboard = uinput.Device(
        ALL_KNOWN_KEYS,
        name=keyboardDev.devicename+" (keyboard-center)",
        vendor=keyboardDev.usbVendor
    )

    logging.info("starting service...")
    global evLoop
    evLoop = asyncio.get_event_loop()
    evLoop.create_task(usbListener(
        keyboard, keyboardEndpoint, keyboardDev, HIDpath, HIDpath_disable))

    try:
        inotify = INotify()
        inotify.add_watch(config.configFile, flags.MODIFY)
        evLoop.add_reader(inotify, lambda: inotifyReader(inotify))
    except Exception as e:
        # TODO: switch to polling (not great, but better than nothing)
        logging.critical("Failed to init inotify :(..."+str(e))

        Notification(
            app_name=APP_NAME,
            title="Inotify Init",
            description="Failed to init inotify! :(\n"+str(e),
            icon_path=ICON_LOCATION,
            urgency="critical"
        ).send_linux()

    evLoop.add_signal_handler(signal.SIGINT, _stop)
    evLoop.add_signal_handler(signal.SIGTERM, _stop)
    evLoop.run_forever()

if __name__ == "__main__":
    #logging.basicConfig(
    #    filename="",
    #    format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
    #    level=logging.DEBUG
    #)

    logging.basicConfig(
        format="%(levelname)s: %(message)s", level=logging.DEBUG
    )

    global config
    config = Configparser(TEMPLATE_LOCATION, sys.argv) # TODO: catch possible errors

    main()
