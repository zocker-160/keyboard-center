#! /usr/bin/env python3
""" small application to test openRGB SDK """

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

client = OpenRGBClient()

#keyboard = client.get_devices_by_type(DeviceType.KEYBOARD)[0]

client.load_profile("G815gg")
