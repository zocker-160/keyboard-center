import os
import shutil
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

class Configparser:

    def __init__(self, locConfTemplate: str, *args, silent=True):
        self.configFile = self._getConfigLocation(locConfTemplate, args)

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
            os.mkdir(confFolder)
        if not os.path.isfile(confLoc):
            shutil.copyfile(confTemplate, confLoc)

        return confLoc

    def getSettings(self) -> dict:
        return self.settings["settings"]

    def getMappings(self) -> dict:
        return self.settings["mappings"]

    def getProfile(self, profile) -> dict:
        d = self.getMappings().get(profile)
        return d if d else {}

    def getKey(self, profile: str, key: str) -> tuple:
        """ 
        gets the pressed key + profile and returns either the key tuple 
        or a combo (for macros)

        @returns tuple(TYPE_KEY, keytuple)
        @returns tuple(TYPE_COMBO, array[keytuples])

        keytuple or array is None when no mapping is found
        """

        macro = self.getProfile(profile).get(key)
        if macro:
            if macro["type"] == TYPE_KEY:
                return (TYPE_KEY, tuple(macro["value"]))

            elif macro["type"] == TYPE_COMBO:
                return (TYPE_COMBO, [ tuple(x) for x in macro["value"] ])

            elif macro["type"] == TYPE_MACRO:
                res = list()
                for combo in macro["value"]:
                    res.append([ tuple(x) for x in combo ])
                return (TYPE_MACRO, res)
        else:
            logging.info(f"key {key} does not have any mapping for {profile}")

            return (TYPE_KEY, None)

    def _generateEntry(self, type, value, string, name) -> dict:
        return {
            "name": name,
            "type": type,
            "value": value,
            "string": string
        }

    ## load and store from GUI

    def saveFromGui(self, profile: str, macroKey: str, name: str,
            data, bSavetoFile=False):
        mapping = self.getMappings()
        print(mapping)

        data = self._convertDataFromGuiToYaml(data, name)

        if data != False:
            if not mapping.get(profile):
                mapping[profile] = dict()
        
            mapping[profile][macroKey] = data
        else:
            try:
                del mapping[profile][macroKey]
            except KeyError:
                pass

        print(self.settings)
        if bSavetoFile: self.save()

    def loadForGui(self, profile: str, macroKey: str):
        data: dict = self.getProfile(profile).get(macroKey)
        if data:
            if data.get("type") == TYPE_COMBO: # TODO: remove this nonsense
                return ([data.get("string")], data.get("name"), [data.get("value")])
            elif data.get("type") == TYPE_KEY:
                return ([[data.get("string")]], data.get("name"), [[data.get("value")]])
            else:
                return (data.get("string"), data.get("name"), data.get("value"))
        else:
            return ({}, "", {})

    def _convertDataFromGuiToYaml(self, data: list, name="") -> dict:
        """ 
        Converts data returned by the GUI to the YAML format

        @example key: [[('A', 38)]]
        @example combo: [[('Ctrl', 29), ('Shift', 42), ('A', 38)]]
        @example macro: [[('Ctrl', 29), ('Shift', 42), ('D', 40)], [('Shift', 42), ('A', 38)]]

        @returns dict with data or "False" if entry needs to get removed
        """
        getType = lambda x: TYPE_DELAY if x == TYPE_DELAY_STR else TYPE_CLICK

        if len(data) == 0:
            # no data -> delete this entry
            return False
            #raise KeyError("No data was returned from the GUI thread! (0x1)")
        elif len(data) == 1:
            keycombo: list = data.pop()

            if len(keycombo) == 1:
                string, val = keycombo.pop()
                return self._generateEntry(
                    TYPE_KEY,
                    (getType(string), val),
                    string,
                    name
                )

            elif len(keycombo) > 1:
                string, val = list(), list()
                for key in keycombo:
                    s, v = key
                    string.append(s)
                    val.append( (getType(s), v) )
                return self._generateEntry(TYPE_COMBO, val, string, name)

            else:
                raise KeyError("No data was returned from the GUI thread! (0x2)")

        else:
            string, val = list(), list()
            for keycombo in data:
                kstring, kval = list(), list()
                for key in keycombo:
                    s, v = key
                    kstring.append(s)
                    kval.append( (getType(s), v) )

                string.append(kstring)
                val.append(kval)
            return self._generateEntry(TYPE_MACRO, val, string, name)

    ## load and store from config file

    def load(self, silent=True) -> dict:
        try:
            logging.debug("loading config file " + self.configFile)
            with open(self.configFile, "r") as yaml:
                data = self.configYAML.load(yaml)
            logging.debug("config loaded: " + str(data))
            
            self.settings = data
            return True

        except FileNotFoundError:
            logging.critical("config file not found")
            if not silent: raise
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
