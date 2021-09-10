SERVICE_NAME = "keyboard-center.service"

import sys
import subprocess

def isServiceEnabled() -> bool:
    ret = subprocess.call(f"systemctl --user is-enabled --quiet {SERVICE_NAME}".split())
    if ret == 0:
        return True
    else:
        return False

def isServiceRunning() -> bool:
    ret = subprocess.call(f"systemctl --user is-active --quiet {SERVICE_NAME}".split())
    if ret == 0:
        return True
    else:
        return False

def needsReload() -> bool:
    out: str = subprocess.check_output(
        ["/bin/sh", "-c", f"systemctl --user status {SERVICE_NAME}; exit 0"],
        stderr=subprocess.STDOUT
        ).decode()

    if out.find(f"{SERVICE_NAME} changed on disk") != -1:
        return True
    else:
        return False

def startService():
    ret = subprocess.call(f"systemctl --user start {SERVICE_NAME}".split())
    if ret == 0:
        return True
    else:
        return False

def stopService():
    ret = subprocess.call(f"systemctl --user stop {SERVICE_NAME}".split())
    if ret == 0:
        return True
    else:
        return False

def reloadService():
    ret = subprocess.call("systemctl --user daemon-reload".split())
    if ret == 0:
        return True
    else:
        return False

def enableService():
    ret = subprocess.call(f"systemctl --user enable {SERVICE_NAME}".split())
    if ret == 0:
        return True
    else:
        return False

def disableService():
    ret = subprocess.call(f"systemctl --user disable {SERVICE_NAME}".split())
    if ret == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    commands = {
        "start": startService,
        "stop": stopService,
        "reload": reloadService,
        "enable": enableService,
        "disable": disableService,
        "needsReload": needsReload
    }
    arg = sys.argv[1]

    try:
        print( commands[arg]() )
    except KeyError:
        print(f'Unknown option: "{arg}"')
