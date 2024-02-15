#! /usr/bin/env python3

import sys
import logging

from lib.QSingleApplication import QSingleApplication, QSingleApplicationTCP

from mainUi import MainWindow
from constants import *
from lib.configparser import Configparser


if __name__ == "__main__":

    if "--version" in sys.argv or "-v" in sys.argv:
        print("version:", VERSION)
        sys.exit()

    app = QSingleApplicationTCP(APPUUID, sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setApplicationVersion(VERSION)

    if app.isRunning:
        print("Other instance already running - exiting")
        sys.exit()

    logHandlers = [
        logging.FileHandler(Configparser.getLogfile(), "w"),
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
    if devmode: logging.info("Entered DEVMODE")

    # CLI option to disable tray icon (aka background mode)
    bgmode = "--background-mode" in sys.argv
    if bgmode: logging.info("Running in background mode")

    logging.info("------------ starting -------------")

    try:
        window = MainWindow(app, devmode, not bgmode)
    except Exception as e:
        logging.exception(e)
        raise

    sys.exit(app.exec_())
