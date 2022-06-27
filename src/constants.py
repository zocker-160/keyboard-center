#! /usr/bin/env python3

import os

APP_NAME = "Keyboard Center"
VERSION = "0.2.1"

PARENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_LOCATION = os.path.join(
    PARENT_LOCATION, "config", "testconfig-example.yml")

ICON_LOCATION = os.path.join(
    PARENT_LOCATION, "assets", "input-keyboard-virtual.png")
