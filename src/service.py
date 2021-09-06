#! /usr/bin/env python3

import os
import sys
import time
import subprocess
import signal

import logging

import asyncio

import uinput
from usb import core

from pynotifier import Notification
from inotify_simple import INotify, flags

from lib.configparser import *

from devices.keyboard import SUPPORTED_DEVICES, KeyboardInterface
from devices.allkeys import *

currProfile = MEMORY_1

APP_NAME = "Keyboard Center Service"

PARENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_LOCATION = os.path.join(
    PARENT_LOCATION, "config", "testconfig.yaml.example"
)
ICON_LOCATION = os.path.join(
    PARENT_LOCATION, "assets", "input-keyboard-virtual.png"
)

def _stop(*args):
    global evLoop
    logging.info("stopping...")

    evLoop.stop()
    virtualKeyboard.destroy()

async def disableGkeyMapping():
    try:
        logging.debug("disabling g810-led gkey mapping")
        subprocess.Popen("g810-led -gkm 1".split())
    except FileNotFoundError:
        logging.info("g810-led could not be found")
    except Exception as e:
        logging.warning(e)


async def switchProfile(profile):
    global currProfile
    currProfile = profile

    path = os.path.join(
        PARENT_LOCATION,
        "assets", f"{profile}.png"
    )
    logging.debug("notification icon path " + path)
    logging.debug("triggering notification")

    Notification(
        app_name=APP_NAME,
        title=f"Switched to profile {profile}",
        icon_path=path,
        urgency="normal"
    ).send_linux() # this shit is targeted at linux only fuck anything else

async def executeMacro(macro: list):
    for action in macro:
        if len(action) == 1:
            if action[0][0] == TYPE_CLICK:
                virtualKeyboard.emit_click(action[0])
            elif action[0][0] == TYPE_DELAY:
                await asyncio.sleep(action[0][1] / 1000)
            
        elif all([ x[0] == TYPE_CLICK for x in action ]):
            virtualKeyboard.emit_combo(action)
        else:
            logging.error("unknown keyboard action...."+str(action))

async def emitKeys(profile, key, uinput=False):
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
        await executeMacro(macro)

async def usbListener(keyboard: core.Device,
                keyboardEndpoint: core.Endpoint,
                keyboardDev: KeyboardInterface):

    _usbTimeout: int = config.settings["settings"].get("usbTimeout") or 1000

    await asyncio.sleep(0)
    # disable G key mapping in case g810-led is installed
    await disableGkeyMapping()

    await asyncio.sleep(0)
    # Send the sequence to disable the G keys
    if keyboardDev.disableGKeys:
        logging.debug("Sending sequence to disable G keys")

        keyboard.write(
            keyboardEndpoint.bEndpointAddress,
            keyboardDev.disableGKeys,
            _usbTimeout
        )

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
                data = bytes(fromKeyboard)
                #print(data)
                
                if data in keyboardDev.macroKeys:
                    pressed = keyboardDev.macroKeys.get(data)

                    if pressed:
                        if isinstance(pressed, str):
                            await emitKeys(currProfile, pressed)
                            #Thread(target=emitKeys, args=(currProfile,pressed), daemon=True).start()
                        else: # uinput key
                            await emitKeys(currProfile, pressed, True)
                            #Thread(target=emitKeys, args=(currProfile,pressed,True), daemon=True).start()
                    else:
                        pass
                        #logging.debug("recieved data could not get mapped to a macro key")
                        #logging.debug(data)

                elif data in keyboardDev.memoryKeys:
                    await switchProfile(keyboardDev.memoryKeys[data])
                    #Thread(target=switchProfile, args=(keyboardDev.memoryKeys[data],), daemon=True).start()
                else:
                    pass
        
        # older versions of python3-usb throw USBError instead of USBTimeoutError
        # all glory to backwards compatibility I guess....
        except core.USBError:
            pass        
        except core.USBTimeoutError:
            pass

def inotifyReader(inotify: INotify):
    for _ in inotify.read():
        # reload configuration
        logging.info("config changed - realoading...")
        if config.load():
            Notification(
                app_name=APP_NAME,
                title="Configuration changed",
                description="new config loaded!",
                icon_path=ICON_LOCATION,
                urgency="normal"
            ).send_linux()


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

            logging.debug("requesting USB endpoint...")
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

    keyboardEndpoint: core.Endpoint = keyboard\
                                        [keyboardDev.usbConfiguration]\
                                        [keyboardDev.usbInterface]\
                                        [keyboardDev.usbEndpoint]

    logging.debug("check and detach kernel driver if active")
    if keyboard.is_kernel_driver_active(keyboardDev.usbInterface[0]):
        keyboard.detach_kernel_driver(keyboardDev.usbInterface[0])

    logging.debug("creating uinput device...")
    global virtualKeyboard
    virtualKeyboard = uinput.Device(
        ALL_KNOWN_KEYS,
        name=keyboardDev.devicename+" vdev",
        vendor=keyboardDev.usbVendor
    )

    logging.info("starting service...")
    global evLoop
    evLoop = asyncio.get_event_loop()
    evLoop.create_task(usbListener(keyboard, keyboardEndpoint, keyboardDev))

    try:
        inotify = INotify()
        inotify.add_watch(config.configFile, flags.MODIFY)
        evLoop.add_reader(inotify, lambda: inotifyReader(inotify))
    except Exception as e:
        logging.exception("Failed to init inotify :(...", str(e))

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
