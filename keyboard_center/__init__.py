#! /usr/bin/env python3

import sys
import signal
import logging

from .lib.QSingleApplication import QSingleApplicationTCP

from .mainwindow import MainWindow

from .lib import utils
from .config.constants import *

def main():

    if "--version" in sys.argv or "-v" in sys.argv:
        print("version:", VERSION)
        sys.exit()

    app = QSingleApplicationTCP(APPUUID, sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setApplicationVersion(VERSION)

    if app.isRunning:
        print("other instance already running - exiting")
        sys.exit()

    logHandlers = [
        logging.FileHandler(utils.getLogFile(), "w"),
        logging.StreamHandler(sys.stdout)
    ]

    logging.basicConfig(
        handlers=logHandlers,
        #format='[%(name)s/%(funcName)s] %(levelname)s: %(asctime)s %(message)s',
        format='[%(name)s] %(levelname)s: %(asctime)s %(message)s',
        datefmt='%d.%m.%Y %I:%M:%S %p',
        level=logging.DEBUG
    )

    # devmode disables openRGB integration
    devmode = "--dev" in sys.argv
    if devmode: logging.info("entered DEVMODE")

    # CLI option to disable tray icon (aka background mode)
    notray = "--notray" in sys.argv
    if notray: logging.info("disabled tray icon")

    logging.info(f"------------ {APP_NAME} {VERSION} -------------")

    try:
        window = MainWindow(app, devmode, trayVisible=not notray)
    except Exception as e:
        logging.exception(e)
        raise

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
