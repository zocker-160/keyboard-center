function Start()

	-- loops while the key is down
    while KC_isKeyDown() do
		KC_keyClick(30) -- clicks A-key
		KC_keyClick(31) -- clicks S-key

        KC_sleepMS(100) -- sleeps for 100ms
        -- KC_sleep(1) -- sleeps for 1s
    end


end

function End()
	-- runs after the while loop in Start() has terminated
	KC_logDebug("macro finished")
end
