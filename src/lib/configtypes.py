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

class ConfigEntry_old:
    name: str
    stringValue: list
    type: str
    value: list

    @staticmethod
    def fromConfig(data: dict):
        _type = data.get("type")
        if _type == TYPE_KEY:
            return Key(
                data.get("name"),
                data.get("value"),
                data.get("string")
            )
        elif _type == TYPE_COMBO:
            return Combo(
                data.get("name"),
                data.get("value"),
                data.get("string")
            )
        elif _type == TYPE_MACRO:
            return Macro(
                data.get("name"),
                data.get("value"),
                data.get("string")
            )
        else:
            raise TypeError(f"unknwon data type ({_type})")

    @staticmethod
    def fromGUI(data: list, name=""):
        """ 
        Reads data returned by the GUI

        @example data key: [[('A', 38)]]
        @example data combo: [[('Ctrl', 29), ('Shift', 42), ('A', 38)]]
        @example data macro: [[('Ctrl', 29), ('Shift', 42), ('D', 40)], [('Shift', 42), ('A', 38)]]
        """
        if len(data) <= 0:
            return False
        elif len(data) == 1:
            keycombo: list = data.pop()

            if len(keycombo) == 1:
                return Key(name, keycombo[1], keycombo[0])

            elif len(keycombo) > 1:
                _keylist = [ Key(name, x[1], x[0]) for x in keycombo ]
                return Combo(name, *Combo.fromKeylist(_keylist))

            else:
                raise KeyError("No data was returned from the GUI thread! (0x2)")

        else:
            pass

    def toConfig(self):
        data = {
            "name": self.name,
            "type": self.type,
            "string": self.stringValue,
            "value": self.value
        }
        return data
##

class ConfigEntry:
    type: str

    @staticmethod
    def genConfig(name, type, string, value):
        return {
            "name": name,
            "type": type,
            "string": string,
            "value": value
        }

    @staticmethod
    def fromConfig(data: dict) -> tuple:
        name = data.get("name")
        type = data.get("type")
        string = data.get("string")
        value = data.get("value")

        if type == TYPE_KEY:
            return Key(value[1], string), name

        elif type == TYPE_DELAY_STR:
            return Delay(value[0][1]), name

        elif type == TYPE_COMBO:
            keylist = list()
            for i, entry in enumerate(string):
                keylist.append( Key(value[i][1], entry) )
            return Combo(keylist), name

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

            return Macro(comboKeylist), name
        else:
            return None, ""

    def toConfig(self, entryName=""):
        return self.genConfig(
            entryName, self.type, self.toConfigString(), self.toConfigValue())

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


##

class Key_old(ConfigEntry_old):
    def __init__(self, name, value, stringValue):
        self.name = name
        self.type = TYPE_KEY
        self.value = (TYPE_CLICK, value)
        self.stringValue = stringValue

    def toTuple(self):
        return (self.stringValue, self.value)

    def toGUI(self):
        return [[(self.stringValue, self.value)]]

class Combo_old(ConfigEntry_old):
    def __init__(self, name, value, stringValue):
        self.name = name
        self.type = TYPE_COMBO
        self.value = value
        self.stringValue = stringValue

    def toGUI(self):
        pass

    @staticmethod
    def fromKeylist(data: list): # list[Key]
        v, sv = list(), list()
        for key in data:
            v.append(key.value)
            sv.append(key.stringValue)
        return (v, sv)

class Macro_old(ConfigEntry_old):
    def __init__(self, name, value, stringValue):
        self.name = name
        self.type = TYPE_MACRO
        self.value = value
        self.string = stringValue

    @staticmethod
    def fromComboList(data: list):  # list[Combo]
        v, sv = list(), list()
        for combo in data:
            v.append(combo.value)
            sv.append(combo.stringValue)
        return (v, sv)
