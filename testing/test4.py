#! /usr/bin/env python3

import time

while True:
    with open("/dev/hidraw1", "rb") as hid:
        print(hid.read())
