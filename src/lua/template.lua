--[[
Template lua script for Keyboard-Center

Functions Start() and End() are mandatory, validation will fail otherwise!

Internal functions:

KC_Sleep(seconds): sleeps for given amount of seconds
KC_SleemMS(milliseconds): sleeps for given amount of milliseconds
KC_isKeyDown(): returns boolean if key is pressed down or not (can be used in while loops)
KC_keyClick(keycode): uinput keycode to simulator key click
KC_keyEmit(keycode, value): uinput keycode to emit; value 1: keydown and 0: keyup
KC_keySyn(): sync specified keys with uinput (see example scripts)
KC_logInfo(message): log message on info level
KC_logDebug(message): log message on debug level
KC_logError(message): log message on error level

]]


function Start()
    -- called when macro key is pressed down
end

function End()
    -- called when macro key is released
    -- IMPORTANT: End() will only get called after Start() has terminated
end
