## LUA script examples

Required and available functions are documented in the lua template.

For emitting keys the keycodes from the Linux uinput kernel module are used.
A list of all available keycodes and their meaning can be found [here](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h#L76).

Note that only keycodes starting with `KEY_` can be used.
