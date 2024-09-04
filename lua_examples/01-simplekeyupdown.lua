function Start()
	KC_logDebug("Start()") -- prints into keyboard-center log

    KC_keyEmit(56, 1) -- ALT keydown
    KC_keyEmit(15, 1) -- TAB keydown
    KC_keySyn() -- sync with system, will be seen as ALT + TAB pressed at the same time

	KC_logDebug("Start() done")
end

function End()
	KC_logDebug("End()")

    KC_keyEmit(56, 0) -- ALT keyup
    KC_keyEmit(15, 0) -- TAB keyup
    KC_keySyn() -- sync with system, will be seen as ALT + TAB released at the same time

	KC_logDebug("Start() done")
end
