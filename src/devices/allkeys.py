import uinput

from enum import IntEnum, Enum, auto

class Numpad(IntEnum):
    KP0 = 82
    KP1 = 79
    KP2 = 80
    KP3 = 81
    KP4 = 75
    KP5 = 76
    KP6 = 77
    KP7 = 71
    KP8 = 72
    KP9 = 73

    NUMLOCK = 69
    DIVIDE = 98
    MULTIPLY = 55
    MINUS = 74
    PLUS = 78
    ENTER = 96
    COMMMA = 83

class Modifiers(IntEnum):
    L_CTRL = 29
    R_CTRL = 97
    L_SHIFT = 42
    R_SHIFT = 54
    L_ALT = 56
    R_ALT = 100
    L_META = 125
    R_META = 126
    CAPSLOCK = 58
    MENU = 127


class Mkey(IntEnum):
    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4

class Gkey(IntEnum):
    G1 = 1
    G2 = 2
    G3 = 3
    G4 = 4
    G5 = 5
    G6 = 6
    G7 = 7
    G8 = 8
    G9 = 9
    G10 = 10
    G11 = 11
    G12 = 12
    G13 = 13
    G14 = 14
    G15 = 15
    G16 = 16
    G17 = 17
    G18 = 18
    G19 = 19
    G20 = 20
    G21 = 21
    G22 = 22
    G23 = 23
    G24 = 24
    G25 = 25
    G26 = 26
    G27 = 27
    G28 = 28
    G29 = 29
    G30 = 30

class MediaKeys(Enum):
    MEMORY_RECORD = auto()

    MEDIA_PLAY_PAUSE = auto()
    MEDIA_PLAY = auto()
    MEDIA_STOP = auto()
    MEDIA_SELECT = auto()

    MEDIA_PREVIOUS = auto()
    MEDIA_NEXT = auto()

    MEDIA_REWIND = auto()
    MEDIA_FAST_FORWARD = auto()
    MEDIA_SEEK_BACK = auto()
    MEDIA_SEEK_FORWARD = auto()

    MEDIA_VOLUME_UP = auto()
    MEDIA_VOLUME_DOWN = auto()
    MEDIA_MUTE_UNMUTE = auto()
    MEDIA_MUTE = auto()
    MEDIA_UNMUTE = auto()

    MEDIA_STOP_RECORDING = auto()
    MEDIA_RECORD = auto()


ALL_UINPUT_KEYS = [(0x1, x) for x in range(0x00, uinput.KEY_MAX[1])]

ALL_KNOWN_KEYS = [
    uinput.KEY_RESERVED,
    uinput.KEY_ESC,
    uinput.KEY_1,
    uinput.KEY_2,
    uinput.KEY_3,
    uinput.KEY_4,
    uinput.KEY_5,
    uinput.KEY_6,
    uinput.KEY_7,
    uinput.KEY_8,
    uinput.KEY_9,
    uinput.KEY_0,
    uinput.KEY_MINUS,
    uinput.KEY_EQUAL,
    uinput.KEY_BACKSPACE,
    uinput.KEY_TAB,
    uinput.KEY_Q,
    uinput.KEY_W,
    uinput.KEY_E,
    uinput.KEY_R,
    uinput.KEY_T,
    uinput.KEY_Y,
    uinput.KEY_U,
    uinput.KEY_I,
    uinput.KEY_O,
    uinput.KEY_P,
    uinput.KEY_LEFTBRACE,
    uinput.KEY_RIGHTBRACE,
    uinput.KEY_ENTER,
    uinput.KEY_LEFTCTRL,
    uinput.KEY_A,
    uinput.KEY_S,
    uinput.KEY_D,
    uinput.KEY_F,
    uinput.KEY_G,
    uinput.KEY_H,
    uinput.KEY_J,
    uinput.KEY_K,
    uinput.KEY_L,
    uinput.KEY_SEMICOLON,
    uinput.KEY_APOSTROPHE,
    uinput.KEY_GRAVE,
    uinput.KEY_LEFTSHIFT,
    uinput.KEY_BACKSLASH,
    uinput.KEY_Z,
    uinput.KEY_X,
    uinput.KEY_C,
    uinput.KEY_V,
    uinput.KEY_B,
    uinput.KEY_N,
    uinput.KEY_M,
    uinput.KEY_COMMA,
    uinput.KEY_DOT,
    uinput.KEY_SLASH,
    uinput.KEY_RIGHTSHIFT,
    uinput.KEY_KPASTERISK,
    uinput.KEY_LEFTALT,
    uinput.KEY_SPACE,
    uinput.KEY_CAPSLOCK,
    uinput.KEY_F1,
    uinput.KEY_F2,
    uinput.KEY_F3,
    uinput.KEY_F4,
    uinput.KEY_F5,
    uinput.KEY_F6,
    uinput.KEY_F7,
    uinput.KEY_F8,
    uinput.KEY_F9,
    uinput.KEY_F10,
    uinput.KEY_NUMLOCK,
    uinput.KEY_SCROLLLOCK,
    uinput.KEY_KP7,
    uinput.KEY_KP8,
    uinput.KEY_KP9,
    uinput.KEY_KPMINUS,
    uinput.KEY_KP4,
    uinput.KEY_KP5,
    uinput.KEY_KP6,
    uinput.KEY_KPPLUS,
    uinput.KEY_KP1,
    uinput.KEY_KP2,
    uinput.KEY_KP3,
    uinput.KEY_KP0,
    uinput.KEY_KPDOT,
    uinput.KEY_ZENKAKUHANKAKU,
    uinput.KEY_102ND,
    uinput.KEY_F11,
    uinput.KEY_F12,
    uinput.KEY_RO,
    uinput.KEY_KATAKANA,
    uinput.KEY_HIRAGANA,
    uinput.KEY_HENKAN,
    uinput.KEY_KATAKANAHIRAGANA,
    uinput.KEY_MUHENKAN,
    uinput.KEY_KPJPCOMMA,
    uinput.KEY_KPENTER,
    uinput.KEY_RIGHTCTRL,
    uinput.KEY_KPSLASH,
    uinput.KEY_SYSRQ,
    uinput.KEY_RIGHTALT,
    uinput.KEY_LINEFEED,
    uinput.KEY_HOME,
    uinput.KEY_UP,
    uinput.KEY_PAGEUP,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT,
    uinput.KEY_END,
    uinput.KEY_DOWN,
    uinput.KEY_PAGEDOWN,
    uinput.KEY_INSERT,
    uinput.KEY_DELETE,
    uinput.KEY_MACRO,
    uinput.KEY_MUTE,
    uinput.KEY_VOLUMEDOWN,
    uinput.KEY_VOLUMEUP,
    uinput.KEY_POWER,
    uinput.KEY_KPEQUAL,
    uinput.KEY_KPPLUSMINUS,
    uinput.KEY_PAUSE,
    uinput.KEY_SCALE,
    uinput.KEY_KPCOMMA,
    uinput.KEY_HANGEUL,
    uinput.KEY_HANGUEL,
    uinput.KEY_HANJA,
    uinput.KEY_YEN,
    uinput.KEY_LEFTMETA,
    uinput.KEY_RIGHTMETA,
    uinput.KEY_COMPOSE,
    uinput.KEY_STOP,
    uinput.KEY_AGAIN,
    uinput.KEY_PROPS,
    uinput.KEY_UNDO,
    uinput.KEY_FRONT,
    uinput.KEY_COPY,
    uinput.KEY_OPEN,
    uinput.KEY_PASTE,
    uinput.KEY_FIND,
    uinput.KEY_CUT,
    uinput.KEY_HELP,
    uinput.KEY_MENU,
    uinput.KEY_CALC,
    uinput.KEY_SETUP,
    uinput.KEY_SLEEP,
    uinput.KEY_WAKEUP,
    uinput.KEY_FILE,
    uinput.KEY_SENDFILE,
    uinput.KEY_DELETEFILE,
    uinput.KEY_XFER,
    uinput.KEY_PROG1,
    uinput.KEY_PROG2,
    uinput.KEY_WWW,
    uinput.KEY_MSDOS,
    uinput.KEY_COFFEE,
    uinput.KEY_SCREENLOCK,
    uinput.KEY_ROTATE_DISPLAY,
    uinput.KEY_DIRECTION,
    uinput.KEY_CYCLEWINDOWS,
    uinput.KEY_MAIL,
    uinput.KEY_BOOKMARKS,
    uinput.KEY_COMPUTER,
    uinput.KEY_BACK,
    uinput.KEY_FORWARD,
    uinput.KEY_CLOSECD,
    uinput.KEY_EJECTCD,
    uinput.KEY_EJECTCLOSECD,
    uinput.KEY_NEXTSONG,
    uinput.KEY_PLAYPAUSE,
    uinput.KEY_PREVIOUSSONG,
    uinput.KEY_STOPCD,
    uinput.KEY_RECORD,
    uinput.KEY_REWIND,
    uinput.KEY_PHONE,
    uinput.KEY_ISO,
    uinput.KEY_CONFIG,
    uinput.KEY_HOMEPAGE,
    uinput.KEY_REFRESH,
    uinput.KEY_EXIT,
    uinput.KEY_MOVE,
    uinput.KEY_EDIT,
    uinput.KEY_SCROLLUP,
    uinput.KEY_SCROLLDOWN,
    uinput.KEY_KPLEFTPAREN,
    uinput.KEY_KPRIGHTPAREN,
    uinput.KEY_NEW,
    uinput.KEY_REDO,
    uinput.KEY_F13,
    uinput.KEY_F14,
    uinput.KEY_F15,
    uinput.KEY_F16,
    uinput.KEY_F17,
    uinput.KEY_F18,
    uinput.KEY_F19,
    uinput.KEY_F20,
    uinput.KEY_F21,
    uinput.KEY_F22,
    uinput.KEY_F23,
    uinput.KEY_F24,
    uinput.KEY_PLAYCD,
    uinput.KEY_PAUSECD,
    uinput.KEY_PROG3,
    uinput.KEY_PROG4,
    uinput.KEY_DASHBOARD,
    uinput.KEY_SUSPEND,
    uinput.KEY_CLOSE,
    uinput.KEY_PLAY,
    uinput.KEY_FASTFORWARD,
    uinput.KEY_BASSBOOST,
    uinput.KEY_PRINT,
    uinput.KEY_HP,
    uinput.KEY_CAMERA,
    uinput.KEY_SOUND,
    uinput.KEY_QUESTION,
    uinput.KEY_EMAIL,
    uinput.KEY_CHAT,
    uinput.KEY_SEARCH,
    uinput.KEY_CONNECT,
    uinput.KEY_FINANCE,
    uinput.KEY_SPORT,
    uinput.KEY_SHOP,
    uinput.KEY_ALTERASE,
    uinput.KEY_CANCEL,
    uinput.KEY_BRIGHTNESSDOWN,
    uinput.KEY_BRIGHTNESSUP,
    uinput.KEY_MEDIA,
    uinput.KEY_SWITCHVIDEOMODE,
    uinput.KEY_KBDILLUMTOGGLE,
    uinput.KEY_KBDILLUMDOWN,
    uinput.KEY_KBDILLUMUP,
    uinput.KEY_SEND,
    uinput.KEY_REPLY,
    uinput.KEY_FORWARDMAIL,
    uinput.KEY_SAVE,
    uinput.KEY_DOCUMENTS,
    uinput.KEY_BATTERY,
    uinput.KEY_BLUETOOTH,
    uinput.KEY_WLAN,
    uinput.KEY_UWB,
    uinput.KEY_UNKNOWN,
    uinput.KEY_VIDEO_NEXT,
    uinput.KEY_VIDEO_PREV,
    uinput.KEY_BRIGHTNESS_CYCLE,
    uinput.KEY_BRIGHTNESS_AUTO,
    uinput.KEY_BRIGHTNESS_ZERO,
    uinput.KEY_DISPLAY_OFF,
    uinput.KEY_WWAN,
    uinput.KEY_WIMAX,
    uinput.KEY_RFKILL,
    uinput.KEY_MICMUTE,
    uinput.KEY_OK,
    uinput.KEY_SELECT,
    uinput.KEY_GOTO,
    uinput.KEY_CLEAR,
    uinput.KEY_POWER2,
    uinput.KEY_OPTION,
    uinput.KEY_INFO,
    uinput.KEY_TIME,
    uinput.KEY_VENDOR,
    uinput.KEY_ARCHIVE,
    uinput.KEY_PROGRAM,
    uinput.KEY_CHANNEL,
    uinput.KEY_FAVORITES,
    uinput.KEY_EPG,
    uinput.KEY_PVR,
    uinput.KEY_MHP,
    uinput.KEY_LANGUAGE,
    uinput.KEY_TITLE,
    uinput.KEY_SUBTITLE,
    uinput.KEY_ANGLE,
    uinput.KEY_ZOOM,
    uinput.KEY_MODE,
    uinput.KEY_KEYBOARD,
    uinput.KEY_SCREEN,
    uinput.KEY_PC,
    uinput.KEY_TV,
    uinput.KEY_TV2,
    uinput.KEY_VCR,
    uinput.KEY_VCR2,
    uinput.KEY_SAT,
    uinput.KEY_SAT2,
    uinput.KEY_CD,
    uinput.KEY_TAPE,
    uinput.KEY_RADIO,
    uinput.KEY_TUNER,
    uinput.KEY_PLAYER,
    uinput.KEY_TEXT,
    uinput.KEY_DVD,
    uinput.KEY_AUX,
    uinput.KEY_MP3,
    uinput.KEY_AUDIO,
    uinput.KEY_VIDEO,
    uinput.KEY_DIRECTORY,
    uinput.KEY_LIST,
    uinput.KEY_MEMO,
    uinput.KEY_CALENDAR,
    uinput.KEY_RED,
    uinput.KEY_GREEN,
    uinput.KEY_YELLOW,
    uinput.KEY_BLUE,
    uinput.KEY_CHANNELUP,
    uinput.KEY_CHANNELDOWN,
    uinput.KEY_FIRST,
    uinput.KEY_LAST,
    uinput.KEY_AB,
    uinput.KEY_NEXT,
    uinput.KEY_RESTART,
    uinput.KEY_SLOW,
    uinput.KEY_SHUFFLE,
    uinput.KEY_BREAK,
    uinput.KEY_PREVIOUS,
    uinput.KEY_DIGITS,
    uinput.KEY_TEEN,
    uinput.KEY_TWEN,
    uinput.KEY_VIDEOPHONE,
    uinput.KEY_GAMES,
    uinput.KEY_ZOOMIN,
    uinput.KEY_ZOOMOUT,
    uinput.KEY_ZOOMRESET,
    uinput.KEY_WORDPROCESSOR,
    uinput.KEY_EDITOR,
    uinput.KEY_SPREADSHEET,
    uinput.KEY_GRAPHICSEDITOR,
    uinput.KEY_PRESENTATION,
    uinput.KEY_DATABASE,
    uinput.KEY_NEWS,
    uinput.KEY_VOICEMAIL,
    uinput.KEY_ADDRESSBOOK,
    uinput.KEY_MESSENGER,
    uinput.KEY_DISPLAYTOGGLE,
    uinput.KEY_BRIGHTNESS_TOGGLE,
    uinput.KEY_SPELLCHECK,
    uinput.KEY_LOGOFF,
    uinput.KEY_DOLLAR,
    uinput.KEY_EURO,
    uinput.KEY_FRAMEBACK,
    uinput.KEY_FRAMEFORWARD,
    uinput.KEY_CONTEXT_MENU,
    uinput.KEY_MEDIA_REPEAT,
    uinput.KEY_10CHANNELSUP,
    uinput.KEY_10CHANNELSDOWN,
    uinput.KEY_IMAGES,
    uinput.KEY_DEL_EOL,
    uinput.KEY_DEL_EOS,
    uinput.KEY_INS_LINE,
    uinput.KEY_DEL_LINE,
    uinput.KEY_FN,
    uinput.KEY_FN_ESC,
    uinput.KEY_FN_F1,
    uinput.KEY_FN_F2,
    uinput.KEY_FN_F3,
    uinput.KEY_FN_F4,
    uinput.KEY_FN_F5,
    uinput.KEY_FN_F6,
    uinput.KEY_FN_F7,
    uinput.KEY_FN_F8,
    uinput.KEY_FN_F9,
    uinput.KEY_FN_F10,
    uinput.KEY_FN_F11,
    uinput.KEY_FN_F12,
    uinput.KEY_FN_1,
    uinput.KEY_FN_2,
    uinput.KEY_FN_D,
    uinput.KEY_FN_E,
    uinput.KEY_FN_F,
    uinput.KEY_FN_S,
    uinput.KEY_FN_B,
    uinput.KEY_BRL_DOT1,
    uinput.KEY_BRL_DOT2,
    uinput.KEY_BRL_DOT3,
    uinput.KEY_BRL_DOT4,
    uinput.KEY_BRL_DOT5,
    uinput.KEY_BRL_DOT6,
    uinput.KEY_BRL_DOT7,
    uinput.KEY_BRL_DOT8,
    uinput.KEY_BRL_DOT9,
    uinput.KEY_BRL_DOT10,
    uinput.KEY_NUMERIC_0,
    uinput.KEY_NUMERIC_1,
    uinput.KEY_NUMERIC_2,
    uinput.KEY_NUMERIC_3,
    uinput.KEY_NUMERIC_4,
    uinput.KEY_NUMERIC_5,
    uinput.KEY_NUMERIC_6,
    uinput.KEY_NUMERIC_7,
    uinput.KEY_NUMERIC_8,
    uinput.KEY_NUMERIC_9,
    uinput.KEY_NUMERIC_STAR,
    uinput.KEY_NUMERIC_POUND,
    uinput.KEY_NUMERIC_A,
    uinput.KEY_NUMERIC_B,
    uinput.KEY_NUMERIC_C,
    uinput.KEY_NUMERIC_D,
    uinput.KEY_CAMERA_FOCUS,
    uinput.KEY_WPS_BUTTON,
    uinput.KEY_TOUCHPAD_TOGGLE,
    uinput.KEY_TOUCHPAD_ON,
    uinput.KEY_TOUCHPAD_OFF,
    uinput.KEY_CAMERA_ZOOMIN,
    uinput.KEY_CAMERA_ZOOMOUT,
    uinput.KEY_CAMERA_UP,
    uinput.KEY_CAMERA_DOWN,
    uinput.KEY_CAMERA_LEFT,
    uinput.KEY_CAMERA_RIGHT,
    uinput.KEY_ATTENDANT_ON,
    uinput.KEY_ATTENDANT_OFF,
    uinput.KEY_ATTENDANT_TOGGLE,
    uinput.KEY_LIGHTS_TOGGLE,
    uinput.KEY_ALS_TOGGLE,
    uinput.KEY_BUTTONCONFIG,
    uinput.KEY_TASKMANAGER,
    uinput.KEY_JOURNAL,
    uinput.KEY_CONTROLPANEL,
    uinput.KEY_APPSELECT,
    uinput.KEY_SCREENSAVER,
    uinput.KEY_VOICECOMMAND,
    uinput.KEY_BRIGHTNESS_MIN,
    uinput.KEY_BRIGHTNESS_MAX,
    uinput.KEY_KBDINPUTASSIST_PREV,
    uinput.KEY_KBDINPUTASSIST_NEXT,
    uinput.KEY_KBDINPUTASSIST_PREVGROUP,
    uinput.KEY_KBDINPUTASSIST_NEXTGROUP,
    uinput.KEY_KBDINPUTASSIST_ACCEPT,
    uinput.KEY_KBDINPUTASSIST_CANCEL,
    uinput.KEY_MIN_INTERESTING,
    uinput.KEY_MAX
]
