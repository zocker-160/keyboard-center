#! /usr/bin/env python3

import sys
import logging

from PyQt5.QtWidgets import QApplication

from mainUi import MainWindow
from constants import *
from lib.configparser import Configparser


if __name__ == "__main__":
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

    if "--version" in sys.argv or "-v" in sys.argv:
        print("version:", VERSION)
        sys.exit()

    logging.info("------------ starting -------------")

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setApplicationVersion(VERSION)

    try:
        window = MainWindow(app, devmode)
        window.center()
    except Exception as e:
        logging.exception(e)
        raise

    sys.exit(app.exec_())
