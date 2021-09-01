import PyQt5
import uinput
import usb.core
import usb.util

import time

import subprocess
import signal

from PyQt5 import *

USB_IF = 1  # Interface
USB_TIMEOUT = 1000  # Timeout in MS | defines the polling interval

USB_VENDOR = 0x046d # Logitech
USB_PRODUCT = 0xc335 # G910

testdev = uinput.Device(
    [
    uinput.KEY_F,
    uinput.KEY_U,
    uinput.KEY_C,
    uinput.KEY_K,
    uinput.KEY_PLAYPAUSE,
    uinput.KEY_STOP,
    uinput.KEY_NEXT,
    uinput.KEY_PREVIOUS,
    uinput.KEY_MUTE,
    uinput.KEY_F9,
    uinput.KEY_SEMICOLON,
    uinput.KEY_VOLUMEUP,
    uinput.KEY_VOLUMEDOWN,
    (0x01, 0x290),
    ],
    name="g910-virtual",
    vendor=USB_VENDOR
) 


GKEYS = {
    b'\x11\xff\x08\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g1',
    b'\x11\xff\x08\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g2',
    b'\x11\xff\x08\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g3',
    b'\x11\xff\x08\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g4',
    b'\x11\xff\x08\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g5',
    b'\x11\xff\x08\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g6',
    b'\x11\xff\x08\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g7',
    b'\x11\xff\x08\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g8',
    b'\x11\xff\x08\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'g9',
    b'\x02\x08': 'play/pause',
    b'\x02\x04': 'stop',
    b'\x02\x02': 'prev',
    b'\x02\x01': 'next',
    b'\x02@': 'mute',
    b'\x02\x10': "vol up",
    b'\x02 ': "vol down",
    b'\x11\xff\t\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'm1',
    b'\x11\xff\t\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'm2',
    b'\x11\xff\t\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'm3',
    b'\x11\xff\n\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': 'mr',
}

RELEASE = [
    b'\x11\xff\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', # G release
    b'\x02\x00', # media key release
    b'\x11\xff\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', # M release
    b'\x11\xff\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', # MR release
]

running = True


def disableGkeyMapping():
    subprocess.run("g810-led -gkm 1".split())

def test():
    time.sleep(2)

    print("PRINT")

    testdev.emit_click(uinput.KEY_F)
    testdev.emit_click(uinput.KEY_U)
    testdev.emit_click(uinput.KEY_C)
    testdev.emit_click(uinput.KEY_K)

def emitKeys(key: str):
    if key == "play/pause":
        testdev.emit_click(uinput.KEY_PLAYPAUSE)
    elif key == "stop":
        testdev.emit_click(uinput.KEY_STOP)
    elif key == "prev":
        testdev.emit_click(uinput.KEY_PREVIOUS)
    elif key == "next":
        testdev.emit_click(uinput.KEY_NEXT)
    elif key == "mute":
        testdev.emit_click(uinput.KEY_MUTE)
    elif key.startswith("m"):
        subprocess.run(["notify-send", "g910", key+" pressed"])
        #testdev.emit_click(uinput.KEY_SEMICOLON)
        #testdev.emit_click((0x01, 0x290))
    else:
        return

    print("trigger", key)


def _stop(a, b):
    global running
    print("stopping...")
    running = False


def main():
    global running

    g910: usb.core.Device = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

    print(g910)

    g910_endpoint: usb.core.Endpoint = g910[0][(USB_IF,0)][0]

    if g910.is_kernel_driver_active(USB_IF):
        g910.detach_kernel_driver(USB_IF)

    #usb.util.claim_interface(g910, USB_IF)

    while running:
        try:
            fromKeyboard = g910.read(
                g910_endpoint.bEndpointAddress,
                g910_endpoint.wMaxPacketSize,
                USB_TIMEOUT
            )

            if fromKeyboard:
                print(bytes(fromKeyboard))
                if bytes(fromKeyboard) in RELEASE:
                    pass
                else:
                    #print(fromKeyboard)
                    pressed = GKEYS.get(bytes(fromKeyboard))

                    print("pressed", pressed)

                    if pressed:
                        emitKeys(pressed)
        except usb.core.USBTimeoutError:
            pass


## systray stuff: https://www.geeksforgeeks.org/system-tray-applications-using-pyqt5/

if __name__ == "__main__":
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    #disableGkeyMapping()

    main()
