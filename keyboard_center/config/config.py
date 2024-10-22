import os
import shlex
import json
import logging

from enum import StrEnum, IntFlag, auto
from dataclasses import dataclass, asdict, field, fields

from ..lib import utils
from ..devices import allkeys

class Modifiers(IntFlag):
    NONE = 0 # kinda a hack, not sure if this is intended by Python
    CTRL = auto()
    SHIFT = auto()
    ALT = auto()
    ALTGR = auto()
    META = auto()
    CUSTOM = auto()

    def isSet(self) -> bool:
        return self > 0

class ValueType(StrEnum):
    KEY = "key"
    DELAY = "delay"
    COMMAND = "command"

@dataclass
class Value:
    type: ValueType

@dataclass
class KeyValue(Value):
    type: ValueType = ValueType.KEY
    modFlags: Modifiers = Modifiers.NONE
    keycode: int = 0
    string: str = ""
    customKeycode: int = 0
    customString: str = ""

@dataclass
class DelayValue(Value):
    type: ValueType = ValueType.DELAY
    delay: int = 50

@dataclass
class CommandValue(Value):
    type: ValueType = ValueType.COMMAND
    command: list[str] = field(default_factory=list)

    def getCommand(self) -> str:
        return shlex.join(self.command)

    def setCommand(self, command: str):
        self.command = shlex.split(command)

class EntryType(StrEnum):
    UI = "ui"
    SCRIPT = "script"

@dataclass
class Entry:
    name: str
    type: EntryType
    gamemode: int
    values: list[Value] | str

    @staticmethod
    def fromDict(data: dict):
        return Entry(**data)

    def asDict(self):
        return asdict(self)


@dataclass
class Settings:
    minimizeOnStart: bool = False
    showNotifications: bool = False
    useOpenRGB: bool = True

    usbTimeout: int = 1 # in s
    usbSendDelay: int = 0.2 # in s

    retryCount: int = 5
    retryTimeout: int = 5 # in s

    usbDeviceID: int = 0

@dataclass
class Config:
    mappings: dict[allkeys.Mkey, dict[allkeys.Gkey, Entry]] = field(default_factory=dict)
    openRGBprofiles: dict[allkeys.Mkey, str] = field(default_factory=dict)
    settings: Settings = field(default_factory=Settings)

    def getEntry(self, mkey: allkeys.Mkey, gkey: allkeys.Gkey) -> Entry | None:
        mprofile = self.mappings.get(mkey.name)
        if mprofile:
            return mprofile.get(gkey.name)
        else:
            return None

    def setEntry(self, mkey: allkeys.Mkey, gkey: allkeys.Gkey, entry: Entry):
        mprofile = self.mappings.get(mkey.name)
        if not mprofile:
            self.mappings[mkey.name] = dict()
        
        self.mappings[mkey.name][gkey.name] = entry

    def getRGBprofile(self, mkey: allkeys.Mkey) -> str:
        if p := self.openRGBprofiles.get(mkey.name):
            return p
        else:
            return ""

    def setRGBprofile(self, mkey: allkeys.Mkey, profile: str):
        self.openRGBprofiles[mkey.name] = profile

class ConfigKeys(StrEnum):
    MAPPINGS = "mappings"
    OPENRGBPROFILES = "openRGBprofiles"
    SETTINGS = "settings"


class ConfigLoader:

    def __init__(self):
        self.log = logging.getLogger("ConfigLoader")
        self.data: Config = Config()

        self._initConfigLocation()

    def _initConfigLocation(self):
        xdgHome = os.environ.get("XDG_CONFIG_HOME")

        if not xdgHome:
            xdgHome = os.path.join(os.environ["HOME"], ".config")

        self.configFolder = os.path.join(xdgHome, "keyboard-center")
        self.configFile = os.path.join(self.configFolder, "settings.json")

        self.log.debug(
            f"config file location: {utils.getPrivatePath(self.configFile)}")

        os.makedirs(self.configFolder, exist_ok=True)

        if not os.path.isfile(self.configFile):
            self.log.debug("config file not found - creating default")
            self.saveInit()

    def load(self):
        try:
            self.log.debug(
                f"loading config file: {utils.getPrivatePath(self.configFile)}")
            with open(self.configFile, "r") as f:
                data: dict = json.load(f)

            self._validateConfig(data)

            rgbProfiles = data.get(ConfigKeys.OPENRGBPROFILES)
            settings = Settings(**data.get(ConfigKeys.SETTINGS))
            
            config = Config(
                mappings=dict(),
                openRGBprofiles=rgbProfiles,
                settings=settings
            )
            
            mappings_raw: dict = data.get(ConfigKeys.MAPPINGS)
            for mkey in allkeys.Mkey:
                mk: dict = mappings_raw.get(mkey.name)
                if not mk or not isinstance(mk, dict):
                    continue

                for gkey in allkeys.Gkey:
                    gk: dict = mk.get(gkey.name)
                    if not gk or not isinstance(gk, dict):
                        continue

                    entry = self._loadEntry(Entry(**gk))
                    config.setEntry(mkey, gkey, entry)

            print(config)
            self.data = config

            self.log.info("config loaded")

        except FileNotFoundError:
            self.log.critical("config file not found", stack_info=True, exc_info=1)
            raise
        except AssertionError:
            self.log.critical("config file integrity check failed", stack_info=True)
            raise
        except Exception as e:
            self.log.exception(e)
            raise

    def _loadEntry(self, entry: Entry) -> Entry:
        if entry.type == EntryType.SCRIPT:
            return entry
        
        vals = list()

        for value in entry.values:
            fn = fields(Value)[0].name # meh kinda a hack
            vt = ValueType(value[fn])

            if vt == ValueType.KEY:
                vals.append(KeyValue(**value))
            
            elif vt == ValueType.DELAY:
                vals.append(DelayValue(**value))
            
            elif vt == ValueType.COMMAND:
                vals.append(CommandValue(**value))

        entry.values = vals
        return entry

    def _validateConfig(self, data: dict):
        mappings = data.get(ConfigKeys.MAPPINGS)
        openRGBProfiles = data.get(ConfigKeys.OPENRGBPROFILES)
        settings = data.get(ConfigKeys.SETTINGS)

        assert type(mappings) == dict
        assert type(openRGBProfiles) == dict
        assert type(settings) == dict

    def save(self):
        with open(self.configFile, "r") as f:
            backupData: dict = json.load(f)

        data = asdict(self.data)

        with open(self.configFile, "w") as f:
            try:
                json.dump(data, f, indent=4)
            except Exception as e:
                self.log.critical("saving failed, attempting to save backup config")
                self.log.exception(e)

                f.seek(0)
                json.dump(backupData, f, indent=4)
                raise

    def saveInit(self):
        data = asdict(self.data)

        try:
            with open(self.configFile, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.log.critical("init of config file failed - bailing out!")
            self.log.exception(e)
            raise
