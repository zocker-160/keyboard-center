-- this script toggles between two different keys for each keypress

KeyA = 30
KeyS = 31

local function keyToggle()
    local register = KC_getGlobalRegister(42)

    if register == 0 then
        KC_keyClick(KeyA)
        register = 1
    else
        KC_keyClick(KeyS)
        register = 0
    end

    KC_setGlobalRegister(42, register)
end

function Start()
	keyToggle()
	KC_sleepMS(100)
end

function End()
	-- prints value of global register 42 into stdout
	print(KC_getGlobalRegister(42))
end
