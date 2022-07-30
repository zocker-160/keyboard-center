import os
import logging

from ruamel.yaml import YAML

TYPE_CLICK = 0x01
TYPE_PRESSDOWN = 0x02
TYPE_PRESSUP = 0x03
TYPE_DELAY = 0x04
TYPE_COMMAND = 0x05

TYPE_KEY = "key"
TYPE_COMBO = "combo"
TYPE_MACRO = "macro"
TYPE_DELAY_STR = "delay"
TYPE_COMMAND_STR = "command"

MOD_CTRL = "Ctrl"
MOD_ALT = "Alt"
MOD_ALTGR = "AltGr"
MOD_SHIFT = "Shift"
MOD_META = "Meta"

from lib.configtypes import ConfigEntry

class Configparser:

    @staticmethod
    def getLogfile():
        folder = os.path.join(
            os.environ["HOME"], ".var", "log")

        if not os.path.isdir(folder):
            os.makedirs(folder, exist_ok=True)

        return os.path.join(folder, "keyboardCenter.log")

    @staticmethod
    def getPrivatePath(path: str):
        return path.replace(os.environ.get("USER"), "XXXX")

    def __init__(self, locConfTemplate: str, silent=True):
        self._pp = lambda x: Configparser.getPrivatePath(x)

        self.log = logging.getLogger("Configparser")

        self.configFile, self.configFolder = \
            self._getConfigLocation(locConfTemplate)

        self.configYAML = YAML(typ='safe')
        self.load(silent)

    def _getConfigLocation(self, confTemplate: str):
        xdg_home = os.environ.get("XDG_CONFIG_HOME") # XDG_DATA_HOME

        if not xdg_home:
            home = os.environ.get("HOME")
            xdg_home = os.path.join(home, ".config")
        
        confFolder = os.path.join(xdg_home, "keyboard-center")
        confLoc = os.path.join(confFolder, "settings.yml")

        self.log.debug("Config file location: "+self._pp(confLoc))

        # check if file and folder exists
        if not os.path.isdir(confFolder):
            self.log.debug("creating confFolder "+self._pp(confFolder))
            os.makedirs(confFolder, exist_ok=True)
        
        if not os.path.isfile(confLoc):
            self._copyConfig(confTemplate, confLoc)

        return confLoc, confFolder

    ## getter

    def getSettings(self) -> dict:
        return self.settings["settings"]

    def getMappings(self) -> dict:
        return self.settings["mappings"]

    def getProfile(self, profile) -> dict:
        return self.getMappings().get(profile, dict())

    def getDeviceID(self):
        return self.getSettings().get("usbDeviceID")

    def getOpenRGB(self) -> dict:
        d = self.settings.get("openRGB")
        if d:
            return d
        else:
            self.settings["openRGB"] = {}
            return self.settings["openRGB"]

    def getShowNotifications(self) -> bool:
        return self.getSettings().get("showNotifications", True)

    def getMinimizeOnStart(self) -> bool:
        return self.getSettings().get("minOnStart", True)

    def getKey(self, profile: str, key: str) -> tuple:
        """ 
        gets the pressed key + profile and returns either the key tuple 
        or a combo (for macros)

        @returns TYPE_KEY, keytuple, gamemode
        @returns TYPE_COMBO, array[keytuples], gamemode

        keytuple or array is None when no mapping is found
        """

        macro: dict = self.getProfile(profile).get(key)
        if macro:
            if macro["type"] == TYPE_KEY:
                return TYPE_KEY, tuple(macro["value"]), macro.get("gamemode")

            if macro["type"] == TYPE_COMMAND_STR:
                return TYPE_COMMAND, macro["value"][1], None

            elif macro["type"] == TYPE_COMBO:
                return TYPE_COMBO, [ tuple(x) for x in macro["value"] ], macro.get("gamemode")

            elif macro["type"] == TYPE_MACRO:
                res = list()
                for combo in macro["value"]:
                    res.append([ tuple(x) for x in combo ])
                return TYPE_MACRO, res, macro.get("gamemode")
        else:
            self.log.debug(
                f"(ignoring) key {key} does not have any mapping for {profile}")

            return TYPE_KEY, None, None
    
    ## setter

    def setAndSaveDeviceID(self, id):
        self.log.debug("setting deviceID to "+str(id))

        if self.getDeviceID() != id:
            self.getSettings()["usbDeviceID"] = id
            self.save()

    ## load and store from GUI

    def saveFromGui(self, 
            profile: str, macroKey: str, 
            orgb: str,
            data: ConfigEntry,
            notifications: bool,
            minOnStart: bool, bSavetoFile=False):
        mapping = self.getMappings()
        openRGB = self.getOpenRGB()
        globalSettings = self.getSettings()

        self.log.debug(mapping)

        if data:
            self.log.debug(data.toConfig())

            if not mapping.get(profile):
                mapping[profile] = dict()
        
            mapping[profile][macroKey] = data.toConfig()
        else:
            try:
                del mapping[profile][macroKey]
            except KeyError:
                pass

        if orgb:
            openRGB[profile] = orgb
        else:
            try:
                del openRGB[profile]
            except KeyError:
                pass

        globalSettings["showNotifications"] = notifications
        globalSettings["minOnStart"] = minOnStart

        self.log.debug("config from GUI: "+str(self.settings))
        if bSavetoFile: self.save()

    def loadForGui(self, profile: str, macroKey: str):
        data: dict = self.getProfile(profile).get(macroKey)
        openRGB: dict = self.getOpenRGB().get(profile)
        openRGB = openRGB if openRGB else ""
        notification = self.getShowNotifications()
        minOnStart = self.getMinimizeOnStart()

        if data:
            return ConfigEntry.fromConfig(data), openRGB, notification, minOnStart
        else:
            return None, openRGB, notification, minOnStart

    ## load and store from config file

    def load(self, silent=True) -> dict:
        try:
            self.log.debug("loading config file "+self._pp(self.configFile))
            with open(self.configFile, "r") as yaml:
                data = self.configYAML.load(yaml)
            self.log.debug("config loaded: " + str(data))

            self.settings: dict = data

            self._configIntegrityCheck()
            return True

        except FileNotFoundError:
            self.log.critical("config file not found")
            raise
        except TypeError as e:
            # from _configIntegrityCheck
            self.log.exception(e)
            self.log.critical("config file is missing important fields")
            raise
        except AssertionError as e:
            # from _configIntegrityCheck
            self.log.exception(e)
            self.log.critical("config file integrity check failed")
            raise
        except Exception as e:
            self.log.exception(e)
            if not silent: raise

    def save(self, silent=True):
        try:
            self.log.debug("saving into config file "+self._pp(self.configFile))
            with open(self.configFile, "w") as yaml:
                self.configYAML.dump(self.settings, yaml)

        except FileNotFoundError:
            self.log.critical("config file not found")
            if not silent: raise
        except Exception as e:
            self.log.exception(e)
            if not silent: raise

    def _copyConfig(self, src: str, dest: str):
        self.log.info("copying template config file")
        self.log.debug("source: "+self._pp(src))
        self.log.debug("destination: "+self._pp(dest))

        with open(src, "r") as s:
            with open(dest, "w") as d:
                d.write(s.read())

    def _configIntegrityCheck(self):
        settings = self.getSettings()
        mappings = self.getMappings()

        assert type(settings) == dict
        assert type(mappings) == dict
