#! /usr/bin/env python3

import os
import sys
import time
import shlex
import signal
import asyncio
import shutil
import subprocess

import logging
from logging import handlers

from threading import Event, Thread

import uinput
from usb import core
from lib import openrgb

from lib.configparser import *
from lib.pynotifier import Notification
from lib.inotify_simple import INotify, flags
from lib.hid import Device as HIDDevice, HIDFailedToOpenException
import lib.hid as hid

from lib.openrgb.orgb import OpenRGBClient

from devices.keyboard import SUPPORTED_DEVICES, KeyboardInterface
from devices.allkeys import *
from lib.servicehelper import executeCommand

currProfile = MEMORY_1
client = None
openRGBProcess = None

RETRY_COUNT = 5
RETRY_TIMEOUT = 5 # in seconds
USB_TIMEOUT = 1000 # in milliseconds
USB_SEND_WAIT = 0.2 # in seconds

APP_NAME = "Keyboard Center Service"

PARENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_LOCATION = os.path.join(
    PARENT_LOCATION, "config", "testconfig-example.yaml"
)
ICON_LOCATION = os.path.join(
    PARENT_LOCATION, "assets", "input-keyboard-virtual.png"
)

from PyQt5.QtCore import QThread, pyqtSignal

class NoKeyboardException(Exception):
    pass
class NoEndpointException(Exception):
    pass

class BackgroundService(QThread):

    keyboard: core.Device
    keyboardDev: KeyboardInterface
    keyboardEndpoint: core.Endpoint

    virtualKeyboard: uinput.Device

    rgbClient: OpenRGBClient = None
    openRGBProcess: subprocess.Popen = None

    HIDpath: bytes
    HIDpath_write: bytes

    notificationEvent = pyqtSignal(str, str, bool) # title, message, urgent
    notificationIconEvent = pyqtSignal(str, str, str) # title, message, iconPath
    waitingForKeyboardEvent = pyqtSignal()
    quitTriggered = pyqtSignal()

    stopEvent = Event()

    def __init__(self, config: Configparser, useOpenRGB=True):
        super().__init__()
        self.logger = logging.getLogger("BGService")
        self.rgbLogger = logging.getLogger("RGB Thread")

        self.config = config
        self.currProfile = MEMORY_1
        self.useOpenRGB = useOpenRGB

        self.logger.info("setting up service...")
        self.logger.info("searching for supported keyboard...")
        self._initKeyboard()

    def _initKeyboard(self, retry=RETRY_COUNT):
        if retry <= 0:
            raise NoKeyboardException()

        tStart = time.time()
        for i, device in enumerate(SUPPORTED_DEVICES):
            keyboard: core.Device = core.find(
                idVendor=device.usbVendor, idProduct=device.usbProduct)

            if keyboard:
                self.logger.info("keyboard found: "+device.devicename)

                self.config.setAndSaveDeviceID(i)

                self.keyboardDev = device
                break

        if not keyboard:
            self.logger.critical("no supported keyboard found, retrying...")
            self.config.setAndSaveDeviceID("None")

            if retry == RETRY_COUNT:
                self.waitingForKeyboardEvent.emit()

            time.sleep(1)
            return self._initKeyboard(retry-1)

        self.keyboard = keyboard

        tEnd = time.time()
        self.logger.debug(f"time taken to find keyboard in ms: {(tEnd-tStart)*1000}")

        self.logger.debug("requesting USB endpoint...")
        self.keyboardEndpoint: core.Endpoint = self.keyboard\
                                            [self.keyboardDev.usbConfiguration]\
                                            [self.keyboardDev.usbInterface]\
                                            [self.keyboardDev.usbEndpoint]

        self.logger.debug("searching HIDpaths...")
        try:
            self._getHIDpaths()
        except:
            raise
        
        self.logger.debug("creating uinput device")
        self.virtualKeyboard = uinput.Device(
            ALL_KNOWN_KEYS,
            name=self.keyboardDev.devicename+" (keyboard-center)",
            vendor=self.keyboardDev.usbVendor
        )

    def _getHIDpaths(self):
        self.HIDpath, self.HIDpath_write = None, None

        for dev in hid.enumerate(self.keyboardDev.usbVendor, self.keyboardDev.usbProduct):

            if dev.get("interface_number") == self.keyboardDev.usbInterface[0]:
                HIDpath: bytes = dev.get("path")
                self.logger.debug(f"HIDraw read endpoint found: {HIDpath.decode()}")

            if dev.get("interface_number") == self.keyboardDev.disableGKeysInterface:
                HIDpath_disable: bytes = dev.get("path")
                self.logger.debug(f"HIDraw write endpoint found: {HIDpath_disable.decode()}")

        self.logger.debug("Checking for HID availability...")
        def __HIDavailable(HIDpath: bytes, tries: int) -> bool:
            try:
                with HIDDevice(path=HIDpath) as _:
                    self.logger.debug(f"Connected to {HIDpath.decode()}")
                return True
            except HIDFailedToOpenException:
                if tries <= 0:
                    return False
                else:
                    self.logger.warning("Could not open HID device, retrying...")
                    time.sleep(RETRY_TIMEOUT)
                    return __HIDavailable(HIDpath, tries-1)

        numTries = self.config.getSettings().get("retryCount") or RETRY_COUNT
        
        if HIDpath and not __HIDavailable(HIDpath, numTries):
            raise HIDFailedToOpenException(f"Unable to open device {HIDpath.decode()}")

        if not HIDpath or not HIDpath_disable:
            raise NoEndpointException()

        self.HIDpath = HIDpath
        self.HIDpath_write = HIDpath_disable

    ##

    def _setOpenRGBProfile(self, retry: int, first: bool):
        if not self.useOpenRGB: return

        orgb = self.config.getOpenRGB().get(self.currProfile)
        if not orgb: return

        try:
            self.rgbLogger.debug("Setting OpenRGB profile "+orgb)

            if first and not self.rgbClient:
                self.rgbClient = OpenRGBClient()
                self.rgbClient.load_profile(orgb) # we need to run this first, in case the profile does not exist
                self.rgbClient.clear() # we need to clear because sometimes load_profile just does not fucking work
                time.sleep(0.5) # we need to wait a moment after clear

            self.rgbClient.load_profile(orgb)

        except ConnectionRefusedError:
            if retry <= 0 or not first:
                self.rgbLogger.debug("giving up reaching OpenRGB SDK")
                return

            if retry == RETRY_COUNT and shutil.which("openrgb"):
                self.openRGBProcess = subprocess.Popen(["openrgb", "--server"], shell=False)

            self.rgbLogger.debug("could not reach OpenRGB SDK, retrying...")
            time.sleep(RETRY_TIMEOUT)
            self._setOpenRGBProfile(retry-1, first)

        except ValueError as e:
            self.rgbLogger.exception(e)

    def _switchProfile(self, profile: str, first=False):
        self.currProfile = profile

        # switch Mkey LED
        if self.keyboardDev.memoryKeysLEDs:
            with HIDDevice(path=self.HIDpath_write) as hdev:
                hdev.nonblocking = True
                self._sendData(
                    hdev, self.keyboardDev.memoryKeysLEDs[profile])

        # set openRGB profile
        Thread(
            target=self._setOpenRGBProfile,
            args=(RETRY_COUNT, first), daemon=True
        ).start()

        path = os.path.join(
            PARENT_LOCATION, "assets", f"{profile}.png")

        self.notificationIconEvent.emit(
            f"Switched to profile {profile}", "", path)

    def _sendData(self, hdev: HIDDevice, data: bytes):
        if self.keyboardDev.disableGKeysUseWrite:
            hdev.write(data)
        else:
            hdev.send_feature_report(data)

    def _disableGkeyMapping(self):
        self.logger.debug("Sending sequence to disable G keys")
        with HIDDevice(path=self.HIDpath_write) as hdev:
            for data in self.keyboardDev.disableGKeys:
                self._sendData(hdev, data)
                time.sleep(USB_SEND_WAIT)

    def _emitKeys(self, key, uinput=False):
        """ 
        Function that emits the requested keys

        this function can be blocking
        """
        self.logger.debug(f"{key} pressed")

        if uinput:
            type, data, gamemode = TYPE_KEY, key, False
        else:
            type, data, gamemode = self.config.getKey(self.currProfile, key)

        if type == TYPE_KEY and data:
            self.virtualKeyboard.emit_click(data)

        elif type == TYPE_COMMAND and data:
            executeCommand(data)

        elif type == TYPE_COMBO and data:
            self._executeCombo(data, gamemode)

        elif type == TYPE_MACRO and data:
            print(data)
            # TODO: macros are ignoring game mode??
            self._executeMacro(data)

    def _executeCombo(self, combo: list, gamemode=0):
        if gamemode > 1:
            for i, c in enumerate(combo):
                self.virtualKeyboard.emit(c, 1, i == len(combo)-1)
            time.sleep(gamemode / 1000)
            for i, c in enumerate(combo):
                self.virtualKeyboard.emit(c, 0, i == len(combo)-1)
        else:
            self.virtualKeyboard.emit_combo(combo)

    def _executeMacro(self, macro: list):
        for action in macro:
            if len(action) == 1:
                if action[0][0] == TYPE_CLICK:
                    self.virtualKeyboard.emit_click(action[0])

                elif action[0][0] == TYPE_DELAY:
                    time.sleep(action[0][1] / 1000)
                
                elif action[0][0] == TYPE_COMMAND:
                    executeCommand(action[0][1])

            elif all([ x[0] == TYPE_CLICK for x in action ]):
                self.virtualKeyboard.emit_combo(action)
            else:
                self.logger.error("unknown keyboard action...."+str(action))

    def _handleRawData(self, fromKeyboard):

        data = bytes(fromKeyboard)
        pressed = self.keyboardDev.macroKeys.get(data)

        if data in self.keyboardDev.macroKeys:
            if pressed:
                if isinstance(pressed, str):
                    Thread(
                        target=self._emitKeys,
                        args=(pressed,), daemon=True
                    ).start()
                
                else: # uinput key
                    Thread(
                        target=self._emitKeys,
                        args=(pressed,True), daemon=True
                    ).start()
            
            else:
                pass
                #logging.debug("recieved data could not get mapped to a macro key")
                #logging.debug(data)

        elif data in self.keyboardDev.memoryKeys:
            Thread(
                target=self._switchProfile, 
                args=(self.keyboardDev.memoryKeys[data],), daemon=True
            ).start()

        #elif keyboardDev.useLibUsb and data in keyboardDev.mediaKeys:
        #    Thread(target=emitKeys, args=(currProfile,pressed,True), daemon=True).start()

        else:
            pass

    ##

    def run(self):
        self.logger.info("starting service loop...")
        self.stopEvent.clear()
        
        _usbTimeout: int = self.config.getSettings().get("usbTimeout") or USB_TIMEOUT

        if self.keyboardDev.disableGKeys:
            self._disableGkeyMapping()

        with HIDDevice(path=self.HIDpath) as hdev:
            hdev.nonblocking = True

            self._switchProfile(self.currProfile, True)

            errorCount = 0
            while not self.stopEvent.isSet():
                try:
                    fromKeyboard = hdev.read(
                        self.keyboardEndpoint.wMaxPacketSize, _usbTimeout)

                    if fromKeyboard:
                        self._handleRawData(fromKeyboard)
                        errorCount = 0

                except hid.HIDException as e:
                    self.logger.error(f"HIDerror: ({e})")

                    if errorCount > 5:
                        self.logger.error("keyboard disconnected...")
                        self.quit()
                    else:
                        errorCount += 1
            else:
                self.logger.debug("left runloop")

    def quit(self, error=True):
        self.logger.info("thread stop triggered...")
        self.stopEvent.set()

        try:
            self.virtualKeyboard.destroy()
        except OSError:
            # this gets thrown when keyboard is unplugged
            pass

        if self.rgbClient: self.rgbClient.disconnect()
        if self.openRGBProcess and self.openRGBProcess.poll():
            self.logger.info("stopping openRGB server...")

            self.openRGBProcess.send_signal(signal.SIGINT)
            self.openRGBProcess.wait()

        if error: self.quitTriggered.emit()

        return super().quit()
