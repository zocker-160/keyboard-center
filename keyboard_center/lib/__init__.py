from .openrgb.openrgb import OpenRGBClient

from . import hid
from .hid import (
    Device as HIDDevice,
    HIDFailedToOpenException,
    HIDException
)