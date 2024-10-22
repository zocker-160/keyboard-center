import os
import shlex
import logging
import subprocess

from enum import Enum

logger = logging.getLogger("Utils")

def executeCommand(command: str | list[str]):
    if not command: return

    if isinstance(command, str):
        command = shlex.split(command)

    try:
        subprocess.Popen(
            command, shell=False, start_new_session=True)
    except Exception as e:
        logger.exception(e)

def openUrl(url: str):
    subprocess.Popen(["xdg-open", url], shell=False)


def getPrivatePath(path: str) -> str:
    return path.replace(os.environ["USER"], "XXXX")

def getLogFile() -> str:
    folder = getLogFolder()
    return os.path.join(folder, "keyboardCenter.log")

def getLogFolder() -> str:
    folder = os.path.join(os.environ["HOME"], ".var", "log")

    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    return folder
