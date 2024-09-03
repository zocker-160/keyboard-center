import os
import shlex
import logging
import subprocess

from enum import Enum

logger = logging.getLogger("Utils")

def executeCommand(command: str):
    if not command: return

    try:
        subprocess.Popen(
            shlex.split(command), shell=False, start_new_session=True)
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


def valueInEnum(value: object, enum: Enum) -> bool:
    """
    hacky workaround for missing "in" keyword in Enums for older Python <3.12

    TODO: replace with "in" for Python >=3.12
    see: https://docs.python.org/3/library/enum.html#enum.EnumType.__contains__
    """
    return value in [x.value for x in enum]
