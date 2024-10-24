#! /usr/bin/env python3

import sys
import signal
import logging
import asyncio
import time
from usb import core
from .lib import hid
from .lib.hid import Device as HIDDevice
from .lib.hid import HIDException

usbConfiguration = 0
usbInterface = (1, 0)
usbEndpoint = 0
disableGKeysInterface = 1
usbUseWrite = False

## Logitech, Inc. G910 Orion Spark Mechanical Keyboard
#usbVendor = 0x046d
#usbProduct = 0xc335

## Logitech, Inc. G815
#usbVendor = 0x046d
#usbProduct = 0xc33f

## Logitech, Inc. G915
#usbVendor = 0x046d
#usbProduct = 0xc33e

## Logitech, Inc. G510
#usbVendor = 0x046d
#usbProduct = 0xc22d

## Logitech, Inc. G510 (2011)
usbVendor = 0x046d
usbProduct = 0xc22e

## G510
disableGKeys = [
    bytes([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    bytes([7, 3, 0]),
    bytes([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
]

## G710+
#disableGKeys = [b'\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']

## G910
#disableGKeys = [
#    b'\x11\xff\x10>\x00\x04\x00\x00\x00\x00\x00\x00\xd0\x01d\x07\x00\x00\x00\x00', # keyboard reset
#    b'\x11\xff\x08.\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', # disable GMapping
#]

## G815
#disableGKeys = [
#    b'\x11\xff\x11\x1a\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 
#    b'\x11\xff\n*\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
#    b'\x11\xff\x0fZ\x01\x03\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
#    b'\x11\xff\x0f\x1a\x00\x02\x00\x00\x00\x00\x00\x084d\x00\x00\x01\x00\x00\x00',
#    b'\x11\xff\x0f\x1a\x01\x04\x00\x00\x00\x00\x00\x004\x01d\x08\x01\x00\x00\x00',
#]

## G915
#disableGKeys = [
#    b'\x11\x01\x11\x1a\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 
#    b'\x11\x01\n*\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
#    b'\x11\x01\x0fZ\x01\x03\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
#    b'\x11\x01\x0f\x1a\x00\x02\x00\x00\x00\x00\x00\x084d\x00\x00\x01\x00\x00\x00',
#    b'\x11\x01\x0f\x1a\x01\x04\x00\x00\x00\x00\x00\x004\x01d\x08\x01\x00\x00\x00',
#]


TIMEOUT = 0.2

def _stop(*args):
    global evLoop
    global keyboard
    global usbInterface

    #keyboard.attach_kernel_driver(usbInterface[0])
    logging.info("stopping...")

    evLoop.stop()

def getHIDpaths():
    HIDpath, HIDpath_disable = None, None

    for dev in hid.enumerate(usbVendor, usbProduct):
        if dev.get("interface_number") == usbInterface[0]:
            HIDpath: bytes = dev.get("path")
            logging.debug(f"HIDraw read endpoint found: {HIDpath.decode()}")

        if dev.get("interface_number") == disableGKeysInterface:
            HIDpath_disable: bytes = dev.get("path")
            logging.debug(f"HIDraw disable endpoint found: {HIDpath_disable.decode()}")

    if not HIDpath:
        raise RuntimeError("Failed to find HIDpath (does other app have exclusive access?)")
    if not HIDpath_disable:
        raise RuntimeError("Failed to find HIDpath_disable (does other app have exclusive access?)")

    logging.debug("Checking for HID availability...")
    def __HIDavailable(HIDpath: bytes, tries: int) -> bool:
        try:
            with HIDDevice(path=HIDpath) as _:
                logging.debug(f"Connected to {HIDpath.decode()}")
            return True
        except RuntimeError:
            if tries <= 0:
                return False
            else:
                logging.warning("Could not open HID device, retrying...")
                time.sleep(1000)
                return __HIDavailable(HIDpath, tries-1)

    numTries = 10
    if HIDpath and not __HIDavailable(HIDpath, numTries):
        raise RuntimeError(f"Unable to open device {HIDpath.decode()}")
    if HIDpath_disable and not __HIDavailable(HIDpath_disable, numTries):
        raise RuntimeError(f"Unable to open device {HIDpath_disable.decode()}")

    return HIDpath, HIDpath_disable

async def disableGkeyMapping(HIDpath: str):
    logging.debug("Connection using HIDAPI...")
    with HIDDevice(path=HIDpath) as hdev:
        logging.debug("Sending sequence to disable G keys")

        if usbUseWrite:
            for i, data in enumerate(disableGKeys):
                print(f"{i}: {data}")
                hdev.write(data)
                time.sleep(TIMEOUT)
        else:
            for i, data in enumerate(disableGKeys):
                print(f"{i}: {data}")
                hdev.send_feature_report(data)
                time.sleep(TIMEOUT)


async def usbListener(keyboardEndpoint: core.Endpoint,
                HIDpath: str, HIDpathDisable: str):

    _usbTimeout: int = 5000

    await asyncio.sleep(0)
    
    # Send the sequence to disable the G keys
    if disableGKeys:
        await disableGkeyMapping(HIDpathDisable)

    await asyncio.sleep(0)

    logging.debug(f"listening to USB Interface {usbInterface} | {HIDpath}")

    with HIDDevice(path=HIDpath) as hdev:
        hdev.nonblocking = True
        while True:
            await asyncio.sleep(0)

            try:
                fromKeyboard = hdev.read(
                    keyboardEndpoint.wMaxPacketSize,
                    _usbTimeout
                )

                if len(fromKeyboard) > 0:
                    print("got data from keyboard: ", end="")
                    print(fromKeyboard)
            
            except HIDException as e:
                print(f"HIDerrpr: {str(e)}")


def main(info=False, reset=False):
    global usbInterface

    logging.debug("Searching for keyboard...")
    keyboard: core.Device = core.find(
        idVendor=usbVendor, idProduct=usbProduct
    )

    if keyboard:
        logging.debug("Keyboard found! :)")
    else:
        logging.critical("Keyboard not found :(")
        sys.exit(1)

    logging.debug("requesting USB endpoint...")
    keyboardEndpoint: core.Endpoint = keyboard\
                                        [usbConfiguration]\
                                        [usbInterface]\
                                        [usbEndpoint]
    
    #logging.debug("check and detach kernel driver if active")
    #if keyboard.is_kernel_driver_active(usbInterface[0]):
    #    keyboard.detach_kernel_driver(usbInterface[0])
    #if reset:
    #    keyboard.attach_kernel_driver(usbInterface[0])
    #    sys.exit()

    if info:
        print("###")
        print(keyboard)
        print("###")

        sys.exit()

    HIDpath, HIDpathDisable = getHIDpaths()

    logging.info("starting listener...")
    global evLoop
    evLoop = asyncio.new_event_loop()
    evLoop.create_task(usbListener(keyboardEndpoint, HIDpath, HIDpathDisable))
    evLoop.add_signal_handler(signal.SIGINT, _stop)
    evLoop.add_signal_handler(signal.SIGTERM, _stop)
    evLoop.run_forever()

if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s: %(message)s", level=logging.DEBUG
    )

    if len(sys.argv) > 1:
        info = "--info" in sys.argv
        reset = "--reset" in sys.argv
        main(info, reset)
    else:
        main()
