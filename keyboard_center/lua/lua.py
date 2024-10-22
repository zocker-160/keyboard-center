import os
import time
import lupa
import logging

from typing import Callable
from threading import Thread, Event

from ..config import config
from ..devices import allkeys as keys


TEMPLATE = "template.lua"

def getTemplatePath() -> str:
    return os.path.join(os.path.dirname(__file__), TEMPLATE)

def getScriptName(mkey: keys.Mkey, gkey: keys.Gkey) -> str:
    return f"{mkey.name}{gkey.name}.lua"


class Runner(Thread):

    def __init__(self, keyReleased: Event,
                 scriptLocation: str,
                 mkey: keys.Mkey, gkey: keys.Gkey):
        super().__init__(daemon=True)

        sname = getScriptName(mkey, gkey)

        self.log = logging.getLogger(f"LuaRunner {sname}")
        self.lua = lupa.LuaRuntime()

        self.code: str = ""
        self.keyReleased = keyReleased
        self.script = os.path.join(scriptLocation, sname)

    def getScriptPath(self):
        return self.script

    def initScript(self):
        if not os.path.isfile(self.script):
            template = getTemplatePath()

            with open(template, "r") as src, open(self.script, "w") as dst:
                dst.write(src.read())

        with open(self.script, "r") as f:
            self.code = f.read()

    def validateScript(self):
        self.lua.execute(self.code)
        glob = self.lua.globals()

        assert glob.Start, "LUA script is missing Start() function"
        assert glob.End, "LUA script is missing End() function"

    def setCallbacks(self,
                     keyClick: Callable[[int], None],
                     keyEmit: Callable[[int, int], None],
                     keySyn: Callable[[], None],
                     setGlobalRegister: Callable[[int, int], None],
                     getGlobalRegister: Callable[[int], int],
                     clearGlobalRegister: Callable[[], None]):
        glob = self.lua.globals()

        glob.KC_sleep = time.sleep
        glob.KC_sleepMS = lambda x: time.sleep(x / 1000)

        glob.KC_isKeyDown = lambda: not self.keyReleased.is_set()
        glob.KC_keyClick = keyClick
        glob.KC_keyEmit = keyEmit
        glob.KC_keySyn = keySyn

        glob.KC_setGlobalRegister = setGlobalRegister
        glob.KC_getGlobalRegister = getGlobalRegister
        glob.KC_clearGlobalRegister = clearGlobalRegister

        glob.KC_logInfo = self.log.info
        glob.KC_logDebug = self.log.debug
        glob.KC_logError = self.log.error

    def run(self):
        try:
            self.lua.globals().Start()
            self.keyReleased.wait()
            self.lua.globals().End()

        except Exception as e:
            self.log.exception(e)
