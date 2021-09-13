#! /usr/bin/env python3

import sys
import signal
import logging
import asyncio

from usb import core
import hid
from hid import Device as HIDDevice

## Logitech, Inc. G910 Orion Spark Mechanical Keyboard
usbVendor = 0x046d
usbProduct = 0xc335

# Logitech, Inc. G815
#usbVendor = 0x046d
#usbProduct = ?

usbConfiguration = 0
usbInterface = (1, 0)
usbIntefaceNumber = 1
usbEndpoint = 0

## G710+
#disableGKeys = b'\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

## G910
disableGKeys = b'\x11\xff\x08\x2e\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

## G815
#disableGKeys = b'\x11\xff\x0a\x2b\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def _stop(*args):
    global evLoop
    logging.info("stopping...")

    evLoop.stop()

async def disableGkeyMapping(data: bytes):
    logging.debug("Connection using HIDAPI...")
    with HIDDevice(usbVendor, usbProduct) as hdev:
        logging.debug("Sending sequence to disable G keys")
        hdev.write(data)


async def usbListener(keyboard: core.Device,
                keyboardEndpoint: core.Endpoint,
                disableGKeys: bytes = None):

    _usbTimeout: int = 2000

    await asyncio.sleep(0)
    
    ## Send the sequence to disable the G keys
    #await disableGkeyMapping(disableGKeys)

    await asyncio.sleep(0)

    for dev in hid.enumerate(usbVendor, usbProduct):
        if dev.get("interface_number") == usbIntefaceNumber:
            path: bytes = dev.get("path")
            print("PAATH:", path.decode())
            break
    else:
        print("NOTHING")

    #with HIDDevice(usbVendor, usbProduct) as dev:
    with HIDDevice(path=path) as dev:
        dev.nonblocking = True
        while True:
            await asyncio.sleep(0)
            data = dev.read(20, timeout=_usbTimeout)
            print(data)

    logging.debug(f"listening to USB Interface {usbInterface}")
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
                print("got data from keyboard:", end="")
                print(data)

        # older versions of python3-usb throw USBError instead of USBTimeoutError
        # all glory to backwards compatibility I guess....
        except core.USBError:
            pass        
        except core.USBTimeoutError:
            pass

def main():

    logging.debug("Searching for keyboard...")
    keyboard: core.Device = core.find(
        idVendor=usbVendor, idProduct=usbProduct
    )

    if keyboard:
        logging.debug("Keyboard found! :)")
    else:
        logging.critical("Keyboard not found :(")
        sys.exit(1)

    #logging.debug("requesting USB endpoint...")
    keyboardEndpoint = None
    #keyboardEndpoint: core.Endpoint = keyboard\
    #                                    [usbConfiguration]\
    #                                    [usbInterface]\
    #                                    [usbEndpoint]

    #logging.debug("check and detach kernel driver if active")
    #if keyboard.is_kernel_driver_active(usbInterface[0]):
    #    keyboard.detach_kernel_driver(usbInterface[0])

    print("###")
    print(keyboard)
    print("###")

    logging.info("starting service...")
    global evLoop
    evLoop = asyncio.get_event_loop()
    evLoop.create_task(usbListener(keyboard, keyboardEndpoint, disableGKeys))
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

    main()
