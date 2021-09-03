import uinput
from devices import allkeys as key
from dataclasses import dataclass, field


@dataclass(frozen=True)
class KeyboardInterface:

    devicename: str

    usbVendor: int
    usbProduct: int
    usbConfiguration: int
    usbInterface: tuple # tuple[int, int] | (index of interface, index of alternate setting)
    usbEndpoint: int

    numMacroKeys: int
    numMemoryKeys: int # number of memory / profile keys

    macroKeys: dict # dict[bytes, str]
    memoryKeys: dict # dict[bytes, str]
    releaseEvents: str # str[bytes]

    # Following is sent to disable the default G keys mapping
    disableGKeys: bytes = field(default=b'')


@dataclass(frozen=True)
class Logitech_G910(KeyboardInterface):

    devicename = "Logitech G910"

    usbVendor = 0x046d
    usbProduct = 0xc335
    usbConfiguration = 0
    usbInterface = (1, 0)
    usbEndpoint = 0

    numMacroKeys = 9
    numMemoryKeys = 3

    macroKeys = {
        b'\x11\xff\x08\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_1,
        b'\x11\xff\x08\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_2,
        b'\x11\xff\x08\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_3,
        b'\x11\xff\x08\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_4,
        b'\x11\xff\x08\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_5,
        b'\x11\xff\x08\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_6,
        b'\x11\xff\x08\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_7,
        b'\x11\xff\x08\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_8,
        b'\x11\xff\x08\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MACRO_9,
        b'\x02\x08': uinput.KEY_PLAYPAUSE,
        b'\x02\x04': uinput.KEY_STOP,
        b'\x02\x02': uinput.KEY_PREVIOUS,
        b'\x02\x01': uinput.KEY_NEXT,
        b'\x02@': uinput.KEY_MUTE,
        b'\x02\x10': uinput.KEY_VOLUMEUP,
        b'\x02 ': uinput.KEY_VOLUMEDOWN,
        b'\x11\xff\n\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MEMORY_RECORD,
    }

    memoryKeys = {
        b'\x11\xff\t\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MEMORY_1,
        b'\x11\xff\t\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MEMORY_2,
        b'\x11\xff\t\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00': key.MEMORY_3,
    }

    releaseEvents = {
        b'\x11\xff\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', # G release
        b'\x02\x00', # media key release
        b'\x11\xff\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', # M release
        b'\x11\xff\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', # MR release
    }

@dataclass(frozen=True)
class Logitech_G710p(KeyboardInterface):

    devicename = "Logitech G710+"

    usbVendor = 0x046d
    usbProduct = 0xc24d
    usbConfiguration = 0
    usbInterface = (1, 0)
    usbEndpoint = 0

    numMacroKeys = 6
    numMemoryKeys = 3

    macroKeys = {
        b'\x03\x01\x00\x00': key.MACRO_1,
        b'\x03\x02\x00\x00': key.MACRO_2,
        b'\x03\x04\x00\x00': key.MACRO_3,
        b'\x03\x08\x00\x00': key.MACRO_4,
        b'\x03\x10\x00\x00': key.MACRO_5,
        b'\x03\x20\x00\x00': key.MACRO_6,
        b'\x02\x08': uinput.KEY_PLAYPAUSE,
        b'\x02\x04': uinput.KEY_STOP,
        b'\x02\x02': uinput.KEY_PREVIOUS,
        b'\x02\x01': uinput.KEY_NEXT,
        b'\x02\x40': uinput.KEY_MUTE,
        b'\x02\x10': uinput.KEY_VOLUMEUP,
        b'\x02\x20': uinput.KEY_VOLUMEDOWN,
        b'\x03\x00\x80\x00': key.MEMORY_RECORD,
    }

    memoryKeys = {
        b'\x03\x00\x10\x00': key.MEMORY_1,
        b'\x03\x00\x20\x00': key.MEMORY_2,
        b'\x03\x00\x40\x00': key.MEMORY_3,
    }

    releaseEvents = {
        b'\x03\x00\x00\x00', # G release
        b'\x02\x00', # media key release
        b'\x03\x00\x00\x00', # M release
        b'\x03\x00\x00\x00', # MR release
    }

    disableGKeys = b'\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

SUPPORTED_DEVICES = [
    Logitech_G910,
    Logitech_G710p,
]
