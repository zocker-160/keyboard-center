#! /usr/bin/env python3

import os

APP_NAME = "Keyboard Center"
VERSION = "1.0"

APPUUID = "0eBJVKjwTanGP7aenveagSRi1c9poja2"

PARENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_LOCATION = os.path.join(
    PARENT_LOCATION, "config", "testconfig-example.yml")

ICON_LOCATION = os.path.join(
    PARENT_LOCATION, "assets", "input-keyboard-virtual.png")
