import os
from ruamel.yaml import YAML
import logging

TYPE_CLICK = 0x01
TYPE_PRESSDOWN = 0x02
TYPE_PRESSUP = 0x03
TYPE_DELAY = 0x04

TYPE_KEY = "key"
TYPE_COMBO = "combo"
TYPE_MACRO = "macro"
TYPE_DELAY_STR = "delay"

MOD_CTRL = "Ctrl"
MOD_ALT = "Alt"
MOD_SHIFT = "Shift"
MOD_META = "Meta"

from lib.configtypes import ConfigEntry

class Configparser:

    def __init__(self, locConfTemplate: str, *args, silent=True):
        self.configFile, self.configFolder = \
            self._getConfigLocation(locConfTemplate, args)

        self.configYAML = YAML(typ='safe')
        self.load(silent)

    def _getConfigLocation(self, confTemplate: str, *args):
        xdg_home = os.environ.get("XDG_CONFIG_HOME")

        if not xdg_home:
            home = os.environ.get("HOME") or args[1]
            xdg_home = os.path.join(home, ".config")
        
        confFolder = os.path.join(xdg_home, "keyboard-center")
        confLoc = os.path.join(confFolder, "settings.yml")

        logging.debug("Config file location: "+confLoc)

        # check if file and folder exists
        if not os.path.isdir(confFolder):
            logging.debug("creating confFolder "+confFolder)
            os.mkdir(confFolder)
        if not os.path.isfile(confLoc):
            self._copyConfig(confTemplate, confLoc)

        return confLoc, confFolder

    def getSettings(self) -> dict:
        return self.settings["settings"]

    def getMappings(self) -> dict:
        return self.settings["mappings"]

    def getProfile(self, profile) -> dict:
        d = self.getMappings().get(profile)
        return d if d else {}

    def getOpenRGB(self) -> dict:
        d = self.settings.get("openRGB")
        if d:
            return d
        else:
            self.settings["openRGB"] = {}
            return self.settings["openRGB"]

    def getShowNotifications(self) -> bool:
        d = self.getSettings().get("showNotifications")
        if d != None:
            return d
        else:
            return True

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

            elif macro["type"] == TYPE_COMBO:
                return TYPE_COMBO, [ tuple(x) for x in macro["value"] ], macro.get("gamemode")

            elif macro["type"] == TYPE_MACRO:
                res = list()
                for combo in macro["value"]:
                    res.append([ tuple(x) for x in combo ])
                return TYPE_MACRO, res, macro.get("gamemode")
        else:
            logging.info(f"key {key} does not have any mapping for {profile}")

            return TYPE_KEY, None, None
    
    ## load and store from GUI

    def saveFromGui(self, 
            profile: str, macroKey: str, 
            orgb: str,
            data: ConfigEntry,
            notifications: bool, bSavetoFile=False):
        mapping = self.getMappings()
        openRGB = self.getOpenRGB()
        globalSettings = self.getSettings()

        print(mapping)

        if data:
            print(data.toConfig())

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

        print(self.settings)
        if bSavetoFile: self.save()

    def loadForGui(self, profile: str, macroKey: str):
        data: dict = self.getProfile(profile).get(macroKey)
        openRGB: dict = self.getOpenRGB().get(profile)
        openRGB = openRGB if openRGB else ""
        notification = self.getShowNotifications()

        if data:
            return ConfigEntry.fromConfig(data), openRGB, notification
        else:
            return None, openRGB, notification

    ## load and store from config file

    def load(self, silent=True) -> dict:
        try:
            logging.debug("loading config file " + self.configFile)
            with open(self.configFile, "r") as yaml:
                data = self.configYAML.load(yaml)
            logging.debug("config loaded: " + str(data))

            self.settings: dict = data

            self._configIntegrityCheck()
            return True

        except FileNotFoundError:
            logging.critical("config file not found")
            raise
        except TypeError as e:
            # from _configIntegrityCheck
            logging.exception(e)
            logging.critical("config file is missing important fields")
            raise
        except AssertionError as e:
            # from _configIntegrityCheck
            logging.exception(e)
            logging.critical("config file integrity check failed")
            raise
        except Exception as e:
            logging.exception(e)
            if not silent: raise

    def save(self, silent=True):
        try:
            logging.debug("saving into config file " + self.configFile)
            with open(self.configFile, "w") as yaml:
                self.configYAML.dump(self.settings, yaml)

        except FileNotFoundError:
            logging.critical("config file not found")
            if not silent: raise
        except Exception as e:
            logging.exception(e)
            if not silent: raise

    def _copyConfig(self, src: str, dest: str):
        logging.info("copying template config file")
        logging.debug("source: "+src)
        logging.debug("destinatin: "+dest)

        with open(src, "r") as s:
            with open(dest, "w") as d:
                d.write(s.read())

    def _configIntegrityCheck(self):
        settings = self.getSettings()
        mappings = self.getMappings()

        assert type(settings) == dict
        assert type(mappings) == dict
