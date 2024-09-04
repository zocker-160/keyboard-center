function Start()
	os.execute('notify-send "keydown"')
end

function End()
	os.execute('notify-send "keyup"')
end
