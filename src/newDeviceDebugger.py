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


async def usbListener(keyboard: core.Device,
                keyboardEndpoint: core.Endpoint,
                disableGKeys: bytes = None):

    _usbTimeout: int = 1000

    await asyncio.sleep(0)
    # disable G key mapping in case g810-led is installed
    await disableGkeyMapping()

    await asyncio.sleep(0)
    # Send the sequence to disable the G keys
    if disableGKeys:
        logging.debug("Sending sequence to disable G keys")

        keyboard.write(
            keyboardEndpoint.bEndpointAddress,
            disableGKeys,
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
                print("got data from keyboard:", end="")
                print(data)

        # older versions of python3-usb throw USBError instead of USBTimeoutError
        # all glory to backwards compatibility I guess....
        except core.USBError:
            pass        
        except core.USBTimeoutError:
            pass

def main():

    # Logitech, Inc. G910 Orion Spark Mechanical Keyboard
    usbVendor = 0x046d
    usbProduct = 0xc32b

    usbConfiguration = 0
    usbInterface = (1, 0)
    usbEndpoint = 0

    disableGKeys = None

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

    logging.debug("check and detach kernel driver if active")
    if keyboard.is_kernel_driver_active(usbInterface[0]):
        keyboard.detach_kernel_driver(usbInterface[0])

    logging.debug("creating uinput device...")
    global virtualKeyboard
    virtualKeyboard = uinput.Device(
        ALL_KNOWN_KEYS,
        name="Testkeyboard vdev",
        vendor=usbVendor
    )

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
