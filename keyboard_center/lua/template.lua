--[[
Template lua script for Keyboard Center

Functions Start() and End() are mandatory, validation will fail otherwise!

Internal functions:

KC_sleep(seconds):        sleeps for given amount of seconds
KC_sleepMS(milliseconds): sleeps for given amount of milliseconds

KC_isKeyDown():             returns boolean if key is pressed down or not (can be used in while loops)
KC_keyClick(keycode):       uinput keycode to emit key click
KC_keyEmit(keycode, value): uinput keycode to emit; value 1: keydown and 0: keyup
KC_keySyn():                sync specified keys with uinput (see example scripts)

KC_setGlobalRegister(regsiter, value): sets "register" to "value" (register has to be integer)
KC_getGlobalRegister(register):        returns value of "register" or 0 if not set
KC_clearGlobalRegister():              clears all registers

KC_logInfo(message):  log message on info level
KC_logDebug(message): log message on debug level
KC_logError(message): log message on error level

-- see repository for some script examples
]]


function Start()
    -- called when macro key is pressed down
end

function End()
    -- called when macro key is released
    -- IMPORTANT: End() will only get called after Start() has terminated
end
