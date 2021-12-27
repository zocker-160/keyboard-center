import logging

from lib.configparser import (
    TYPE_CLICK,
    TYPE_DELAY,
    TYPE_DELAY_STR,
    TYPE_KEY,
    TYPE_COMBO,
    TYPE_MACRO
)

log = logging.getLogger("ConfigTypes")

class ConfigEntry:
    type: str
    name: str = ""
    gamemode: bool = False

    @staticmethod
    def genConfig(type, string, value, name="", gamemode=False):
        return {
            "name": name,
            "gamemode": gamemode,
            "type": type,
            "string": string,
            "value": value
        }

    @staticmethod
    def fromConfig(data: dict): # -> ConfigEntry
        name = data.get("name")
        gamemode = data.get("gamemode")
        type = data.get("type")
        string = data.get("string")
        value = data.get("value")

        result: ConfigEntry = None

        if type == TYPE_KEY:
            result = Key(value[1], string)

        elif type == TYPE_DELAY_STR:
            result = Delay(value[0][1])

        elif type == TYPE_COMBO:
            keylist = list()
            for i, entry in enumerate(string):
                keylist.append( Key(value[i][1], entry) )
            result = Combo(keylist)

        elif type == TYPE_MACRO:
            comboKeylist = list()
            for i, entry in enumerate(string):
                if len(entry) == 1:
                    if entry[0] == TYPE_DELAY_STR:
                        comboKeylist.append( Delay(value[i][0][1]) )
                    else:
                        comboKeylist.append( Key(value[i][0][1], entry[0]) )
                else:
                    keylist = list()
                    for j, subentry in enumerate(entry):
                        keylist.append( Key(value[i][j][1], subentry) )

                    comboKeylist.append( Combo(keylist) )

            result = Macro(comboKeylist)

        if name: result.name = name
        if gamemode: result.gamemode = gamemode

        return result

    def toConfig(self):
        return self.genConfig(
            self.type, self.toConfigString(), self.toConfigValue(),
            name=self.name,
            gamemode=self.gamemode
        )

    def toConfigValue(self) -> list:
        raise NotImplementedError

    def toConfigString(self) -> list:
        raise NotImplementedError

class Key(ConfigEntry):
    def __init__(self, keycode: int, keyString: str):
        self.type = TYPE_KEY
        self.keycode = keycode
        self.keyString = keyString

    def toConfigValue(self) -> list:
        return [ (TYPE_CLICK, self.keycode) ]

    def toConfigString(self) -> list:
        return [ self.keyString ]

    def toConfig(self, entryName=""):
        return self.genConfig(
            entryName, self.type, 
            self.toConfigString().pop(), self.toConfigValue().pop()
        )

class Delay(ConfigEntry):
    def __init__(self, durationInMS: int):
        self.type = TYPE_DELAY_STR
        self.duration = durationInMS
        self.keyString = TYPE_DELAY_STR

    def toConfigValue(self):
        return [ (TYPE_DELAY, self.duration) ]

    def toConfigString(self):
        return [ self.keyString ]

class Combo(ConfigEntry):
    def __init__(self, keylist: list):
        self.type = TYPE_COMBO
        self.keylist = keylist

    def toConfigValue(self):
        return [ key.toConfigValue().pop() for key in self.keylist ]

    def toConfigString(self):
        return [ key.toConfigString().pop() for key in self.keylist ]

class Macro(ConfigEntry):
    def __init__(self, comboKeyList: list):
        self.type = TYPE_MACRO
        self.comboKeyList = comboKeyList

    def toConfigString(self):
        return [ x.toConfigString() for x in self.comboKeyList ]

    def toConfigValue(self):
        return [ x.toConfigValue() for x in self.comboKeyList ]
