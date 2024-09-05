-- this script toggles a macro loop on and off every time key is pressed

function Start()

    local reg = KC_getGlobalRegister(42)

    if reg == 0 then
        os.execute('notify-send "loop start"')

        KC_setGlobalRegister(42, 1)

        -- enter loop until register is set back to 0
        while KC_getGlobalRegister(42) == 1 do
            KC_keyClick(KeyA)
            KC_sleepMS(100)
        end

    else
        os.execute('notify-send "loop end"')

        -- stop loop by setting register to 0
        KC_setGlobalRegister(42, 0)
    end
end

function End()
	-- prints value of global register 42 into stdout
	print(KC_getGlobalRegister(42))
end
