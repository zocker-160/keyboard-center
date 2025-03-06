import os
import time
import shutil
import subprocess

import logging

from threading import Event, Thread

import uinput
from usb import core

from .lib import hid
from .lib.hid import Device as HIDDevice, HIDFailedToOpenException
from .lib.openrgb.orgb import OpenRGBClient

from .lua import lua
from .lib import utils
from .config import config

from .devices.allkeys import ALL_UINPUT_KEYS, Mkey, Gkey
from .devices.keyboard import SUPPORTED_DEVICES, KeyboardInterface


PARENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
ICON_LOCATION = os.path.join(
    PARENT_LOCATION, "assets", "input-keyboard-virtual.png"
)

from PyQt5.QtCore import QThread, pyqtSignal

class NoKeyboardException(Exception):
    pass
class NoEndpointException(Exception):
    pass

class BackgroundService(QThread):

    logger = logging.getLogger("BGService")
    rgbLogger = logging.getLogger("RGB Thread")

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
    keyReleasedEvent = Event()

    currProfile = Mkey.M1

    LUAglobalRegister = dict()

    def __init__(self, config: config.ConfigLoader, devmode=False):
        super().__init__()

        self.config = config
        self.devmode = devmode
        self.retryCount = self.config.data.settings.retryCount
        self.retryTimeout = self.config.data.settings.retryTimeout

        self.logger.info("setting up service")
        self.logger.debug("searching for supported keyboard")
        self._initKeyboard()

    def _initKeyboard(self, retryCount=0):
        if retryCount >= self.config.data.settings.retryCount:
            raise NoKeyboardException()

        tStart = time.time()
        for i, device in enumerate(SUPPORTED_DEVICES):
            keyboard: core.Device = core.find(
                idVendor=device.usbVendor, idProduct=device.usbProduct)

            if keyboard:
                self.logger.info(f"keyboard found: {device.devicename}")

                self.config.data.settings.usbDeviceID = i
                self.keyboardDev = device
                break

        if not keyboard:
            if retryCount == 0:
                self.logger.critical("no supported keyboard found, retrying...")
                self.config.data.settings.usbDeviceID = 0
                self.waitingForKeyboardEvent.emit()

            time.sleep(self.retryTimeout) # FIXME this is blocking the UI, really fk bad design
            return self._initKeyboard(retryCount + 1)

        tEnd = time.time()
        self.logger.debug(f"time taken to find keyboard in ms: {(tEnd-tStart)*1000}")

        self.keyboard = keyboard
        self.config.save()

        self.logger.debug("requesting USB endpoint")
        self.keyboardEndpoint: core.Endpoint = self.keyboard\
                                            [self.keyboardDev.usbConfiguration]\
                                            [self.keyboardDev.usbInterface]\
                                            [self.keyboardDev.usbEndpoint]

        self.logger.debug("searching for HID endpoints")
        self._getHIDpaths()

        self.logger.debug("creating uinput device")
        self.virtualKeyboard = uinput.Device(
            #ALL_KNOWN_KEYS,
            ALL_UINPUT_KEYS,
            name=f"{self.keyboardDev.devicename} (keyboard-center)",
            vendor=self.keyboardDev.usbVendor
        )

    def _getHIDpaths(self):
        self.HIDpath, self.HIDpath_write = None, None
        HIDpath, HIDpath_disable = None, None

        for dev in hid.enumerate(self.keyboardDev.usbVendor, self.keyboardDev.usbProduct):

            if dev.get("interface_number") == self.keyboardDev.usbInterface[0]:
                HIDpath: bytes = dev.get("path")
                self.logger.debug(f"HIDraw read endpoint found: {HIDpath.decode()}")

            if dev.get("interface_number") == self.keyboardDev.disableGKeysInterface:
                HIDpath_disable: bytes = dev.get("path")
                self.logger.debug(f"HIDraw write endpoint found: {HIDpath_disable.decode()}")

            if HIDpath and HIDpath_disable:
                break

        def __HIDavailable(HIDpath: bytes, tries: int) -> bool:
            try:
                with HIDDevice(path=HIDpath) as _:
                    self.logger.debug(f"connected to {HIDpath.decode()}")
                return True
            except HIDFailedToOpenException:
                if tries <= 0:
                    return False
                else:
                    self.logger.warning("could not open HID device, retrying")
                    time.sleep(self.retryTimeout)
                    return __HIDavailable(HIDpath, tries-1)

        if not HIDpath or not HIDpath_disable:
            raise NoEndpointException()

        self.logger.debug("checking for HID availability")

        if not __HIDavailable(HIDpath, self.retryCount):
            raise HIDFailedToOpenException(f"unable to open device {HIDpath.decode()}")
        if HIDpath != HIDpath_disable and not __HIDavailable(HIDpath_disable, self.retryCount):
            raise HIDFailedToOpenException(f"unable to open device {HIDpath_disable.decode()}")

        self.HIDpath = HIDpath
        self.HIDpath_write = HIDpath_disable

    ##

    def _setOpenRGBProfile(self, retry: int, first: bool):
        if not self.config.data.settings.useOpenRGB or self.devmode:
            return

        orgb = self.config.data.getRGBprofile(self.currProfile)
        if not orgb: return

        try:
            self.rgbLogger.debug(f"Setting OpenRGB profile {orgb}")

            if first and not self.rgbClient:
                self.rgbClient = OpenRGBClient()
                self.rgbClient.clear() # we need to clear because sometimes load_profile just does not fucking work
                time.sleep(0.5) # we need to wait a moment after clear

            try:
                print(self.rgbClient.profiles)
                self.rgbClient.load_profile(orgb)
            except ValueError:
                self.rgbLogger.warning(f"openRGB profile {orgb} does not exist")

        except ConnectionRefusedError:
            if retry <= 0 or not first or not shutil.which("openrgb"):
                self.rgbLogger.debug("giving up reaching OpenRGB SDK")
                return

            if retry >= self.config.data.settings.retryCount:
                self.openRGBProcess = subprocess.Popen(["openrgb", "--server"], shell=False)

            self.rgbLogger.debug("could not reach OpenRGB SDK, retrying...")
            time.sleep(self.config.data.settings.retryTimeout)
            self._setOpenRGBProfile(retry-1, first)

        except ValueError as e:
            self.rgbLogger.exception(e)

    def _switchProfile(self, profile: Mkey, first=False):
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
            args=(self.config.data.settings.retryCount, first), daemon=True
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
                time.sleep(self.config.data.settings.usbSendDelay)

    def _emitKeys(self, key: Gkey):
        """ 
        function that emits the requested keys
        should be run in a separate thread
        """
        self.logger.debug(f"{self.currProfile.name} / {key.name} pressed")

        entry: config.Entry = self.config.data.getEntry(self.currProfile, key)
        if entry is None:
            return

        if entry.type == config.EntryType.UI and isinstance(entry.values, list):
            nval = len(entry.values)
            if nval == 0:
                return
            elif nval == 1:
                self._emitSingle(entry.values[0], wait=True)
            else:
                for value in entry.values:
                    self._emitSingle(value, wait=False)
                    time.sleep(entry.gamemode)

        elif entry.type == config.EntryType.SCRIPT:
            keyUp = Event()

            runner = lua.Runner(keyUp, self.config.configFolder, self.currProfile, key)
            runner.initScript()
            runner.validateScript()
            runner.setCallbacks(
                keyClick=lambda key: self.virtualKeyboard.emit_click((1, key)),
                keyEmit=lambda key, val: self.virtualKeyboard.emit((1, key), val, syn=False),
                keySyn=self.virtualKeyboard.syn,
                setGlobalRegister=self._setLuaGlobal,
                getGlobalRegister=self._getLuaGlobal,
                clearGlobalRegister=self.LUAglobalRegister.clear
            )
            runner.start()

            self.keyReleasedEvent.wait()
            self.keyReleasedEvent.clear()
            keyUp.set()

            runner.join()

    def _emitSingle(self, value: config.Value, wait: bool):
        if isinstance(value, config.KeyValue):
            self._emitModifiers(value, 1)
            self.virtualKeyboard.emit((1, value.keycode), 1, syn=False)
            self.virtualKeyboard.syn()

            if wait:
                self.keyReleasedEvent.wait()
                self.keyReleasedEvent.clear()

            self._emitModifiers(value, 0)
            self.virtualKeyboard.emit((1, value.keycode), 0, syn=False)
            self.virtualKeyboard.syn()

        elif isinstance(value, config.DelayValue):
            time.sleep(value.delay / 1000)

        elif isinstance(value, config.CommandValue):
            utils.executeCommand(value.command)

    def _emitModifiers(self, keyValue: config.KeyValue, value: int):
        btnFlags = keyValue.modFlags
        if isinstance(btnFlags, int):
            btnFlags = config.Modifiers(btnFlags)

        if not btnFlags.isSet():
            return

        if config.Modifiers.CTRL in btnFlags:
            self.virtualKeyboard.emit(uinput.KEY_LEFTCTRL, value, syn=False)

        if config.Modifiers.ALT in btnFlags:
            self.virtualKeyboard.emit(uinput.KEY_LEFTALT, value, syn=False)

        if config.Modifiers.ALTGR in btnFlags:
            self.virtualKeyboard.emit(uinput.KEY_RIGHTALT, value, syn=False)

        if config.Modifiers.SHIFT in btnFlags:
            self.virtualKeyboard.emit(uinput.KEY_LEFTSHIFT, value, syn=False)

        if config.Modifiers.META in btnFlags:
            self.virtualKeyboard.emit(uinput.KEY_LEFTMETA, value, syn=False)

        if config.Modifiers.CUSTOM in btnFlags:
            self.virtualKeyboard.emit((1, keyValue.customKeycode), value, syn=False)

    def _handleRawData(self, fromKeyboard: bytes):

        self.keyReleasedEvent.clear()

        if fromKeyboard in self.keyboardDev.macroKeys:
            pressed = self.keyboardDev.macroKeys[fromKeyboard]
            Thread(
                target=self._emitKeys,
                args=(pressed,), daemon=True
            ).start()

        elif fromKeyboard in self.keyboardDev.memoryKeys:
            pressed = self.keyboardDev.memoryKeys[fromKeyboard]
            Thread(
                target=self._switchProfile,
                args=(pressed,), daemon=True
            ).start()

        elif fromKeyboard in self.keyboardDev.releaseEvents:
            self.logger.debug("release event")
            self.keyReleasedEvent.set()

        else:
            pass

    ##

    def _setLuaGlobal(self, key: int, value: int):
        self.LUAglobalRegister[key] = value

    def _getLuaGlobal(self, key: int) -> int:
        return self.LUAglobalRegister.get(key, 0)

    ##

    def run(self):
        self.logger.info("Starting service loop")
        self.stopEvent.clear()
        
        usbTimeout = self.config.data.settings.usbTimeout

        if self.keyboardDev.disableGKeys:
            self._disableGkeyMapping()

        with HIDDevice(path=self.HIDpath) as hdev:
            hdev.nonblocking = True
            self._switchProfile(self.currProfile, first=True)

            errorCount = 0
            while not self.stopEvent.isSet():
                try:
                    fromKeyboard = hdev.read(
                        self.keyboardEndpoint.wMaxPacketSize, usbTimeout)

                    if fromKeyboard:
                        self._handleRawData(bytes(fromKeyboard))
                        errorCount = 0

                except hid.HIDException as e:
                    self.logger.error(f"HIDerror: ({e})")

                    if errorCount > 5:
                        self.logger.error("Keyboard disconnected...")
                        self.quit()
                    else:
                        errorCount += 1
            else:
                self.logger.debug("Left runloop")

    def quit(self, error=True):
        self.logger.debug("Thread stop triggered")
        self.stopEvent.set()

        if self.virtualKeyboard:
            try:
                self.virtualKeyboard.destroy()
            except OSError:
                # this gets thrown when keyboard is unplugged
                pass

        if self.rgbClient: self.rgbClient.disconnect()
        if self.openRGBProcess:
            self.rgbLogger.info("Stopping openRGB server")

            if self.openRGBProcess.poll() is None: # no exit code = process running
                #self.openRGBProcess.send_signal(signal.SIGINT)
                #self.openRGBProcess.send_signal(signal.SIGTERM)
                self.openRGBProcess.terminate()

                self.rgbLogger.info("Waiting for openRGB server to stop...")
                retcode = self.openRGBProcess.wait()

                self.rgbLogger.debug(
                    f"openRGB server stopped with ({retcode})")

            else:
                self.rgbLogger.debug("openRGB server is not running")

        if error: self.quitTriggered.emit()

        self.LUAglobalRegister.clear()

        return super().quit()
