import usb.core
import usb.util
import time


import uinput

gkeys = {
    'dump': bytearray(b'\x11\xff\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g1': bytearray(b'\x11\xff\x08\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g2': bytearray(b'\x11\xff\x08\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g3': bytearray(b'\x11\xff\x08\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g4': bytearray(b'\x11\xff\x08\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g5': bytearray(b'\x11\xff\x08\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g6': bytearray(b'\x11\xff\x08\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g7': bytearray(b'\x11\xff\x08\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g8': bytearray(b'\x11\xff\x08\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    'g9': bytearray(b'\x11\xff\x08\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
}


def emitKeys(key):
    if key is 'g1':
        device.emit(uinput.KEY_LEFTCTRL, 1)
        device.emit(uinput.KEY_C, 1)
        device.emit(uinput.KEY_LEFTCTRL, 0)
        device.emit(uinput.KEY_C, 0)
    elif key is 'g2':
        device.emit(uinput.KEY_LEFTCTRL, 1)
        device.emit(uinput.KEY_V, 1)
        device.emit(uinput.KEY_LEFTCTRL, 0)
        device.emit(uinput.KEY_V, 0)


def first_diff_index(ls1, ls2):
    l = min(len(ls1), len(ls2))
    return next((i for i in range(l) if ls1[i] != ls2[i]), l)


device = uinput.Device([
    uinput.KEY_C, uinput.KEY_LEFTCTRL, uinput.KEY_V
])

USB_IF = 1  # Interface
USB_TIMEOUT = 5  # Timeout in MS

USB_VENDOR = 0x046d
USB_PRODUCT = 0xc335

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
print(dev[0][(1, 0)])
endpoint = dev[0][(1, 0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
    dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

while True:
    control = None

    try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)

        if control:
            b = bytearray(control)
            if b in gkeys.values():
                if b == gkeys['dump']:
                    pass
                else:
                    key = list(gkeys.keys())[list(gkeys.values()).index(b)]
                    print(key)
                    emitKeys(key)
            else:
                print(b, 'no match')
    except:
        pass

    time.sleep(0.01)  # Let CTRL+C actually exit```
