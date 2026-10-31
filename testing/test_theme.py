"""Run without keyboard hardware or changes to desktop settings:

dbus-run-session -- env QT_QPA_PLATFORM=offscreen \
    python -m unittest testing.test_theme
"""

import json
import os
import tempfile
import time
import unittest
from unittest.mock import patch

from PyQt5.QtCore import QObject, Q_CLASSINFO, QCoreApplication, QEvent, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtDBus import QDBusConnection, QDBusVariant
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QPushButton

from keyboard_center.config.config import ConfigLoader, KeyValue, DelayValue, CommandValue
from keyboard_center.gui.settingswindow import SettingsWindow
from keyboard_center.gui.theme import SystemTheme
from keyboard_center.gui.Ui_mainwindow import Ui_MainWindow


class SettingsPortal(QObject):
    Q_CLASSINFO("D-Bus Interface", SystemTheme.INTERFACE)
    SettingChanged = pyqtSignal(str, str, QDBusVariant)

    preference = 1
    changeDuringRead = None

    @pyqtSlot(str, str, result=QDBusVariant)
    def Read(self, namespace, key):
        if self.changeDuringRead is not None:
            self.change(self.changeDuringRead)
        return QDBusVariant(QDBusVariant(self.preference))

    def change(self, value, namespace=SystemTheme.NAMESPACE, key=SystemTheme.KEY):
        self.SettingChanged.emit(namespace, key, QDBusVariant(value))


class SystemThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.app.setStyle("Fusion")
        cls.bus = QDBusConnection.sessionBus()
        # A private service name prevents accidental access to the real portal,
        # even when these tests are run on an existing desktop session bus.
        cls.service = patch.object(SystemTheme, "SERVICE",
                                   f"org.keyboardcenter.ThemeTest.p{os.getpid()}")
        cls.service.start()
        cls.portal = SettingsPortal()
        if not cls.bus.registerService(SystemTheme.SERVICE):
            raise RuntimeError("Run the tests under dbus-run-session")
        if not cls.bus.registerObject(
                SystemTheme.PATH, cls.portal,
                QDBusConnection.ExportAllSlots | QDBusConnection.ExportAllSignals):
            raise RuntimeError("Could not register the test Settings portal")

    @classmethod
    def tearDownClass(cls):
        cls.bus.unregisterObject(SystemTheme.PATH)
        cls.bus.unregisterService(SystemTheme.SERVICE)
        cls.service.stop()

    def setUp(self):
        self.environment = patch.dict(os.environ)
        self.environment.start()
        for key in ("QT_QPA_PLATFORMTHEME", "QT_STYLE_OVERRIDE"):
            os.environ.pop(key, None)
        self.app.setStyle("Fusion")
        self.app.setPalette(QPalette())
        self.light = self.app.palette()
        self.portal.preference = 1
        self.portal.changeDuringRead = None
        self.controllers = []

    def tearDown(self):
        for controller in self.controllers:
            if hasattr(controller, "bus"):
                controller.bus.disconnect(
                    controller.SERVICE, controller.PATH, controller.INTERFACE,
                    "SettingChanged", controller._settingChanged,
                )
            controller.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        self.app.setPalette(self.light)
        self.environment.stop()

    def controller(self, mode="auto"):
        controller = SystemTheme(self.app, mode)
        self.controllers.append(controller)
        return controller

    def waitFor(self, predicate):
        deadline = time.monotonic() + 2
        while not predicate() and time.monotonic() < deadline:
            QTest.qWait(10)
        self.assertTrue(predicate())

    def isDark(self):
        palette = self.app.palette()
        return (palette.color(QPalette.Window).lightness()
                < palette.color(QPalette.WindowText).lightness())

    def test_text_contrast_for_dark_palette(self):
        def luminance(color):
            channels = [color.redF(), color.greenF(), color.blueF()]
            linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
                      for v in channels]
            return sum(v * weight for v, weight in zip(linear, (0.2126, 0.7152, 0.0722)))

        self.controller()
        self.waitFor(self.isDark)
        palette = self.app.palette()
        pairs = [(QPalette.WindowText, QPalette.Window),
                 (QPalette.Text, QPalette.Base),
                 (QPalette.ButtonText, QPalette.Button),
                 (QPalette.ToolTipText, QPalette.ToolTipBase),
                 (QPalette.HighlightedText, QPalette.Highlight)]
        for group in (QPalette.Active, QPalette.Inactive, QPalette.Disabled):
            for foreground, background in pairs:
                with self.subTest(group=group, foreground=foreground):
                    values = sorted(luminance(palette.color(group, role))
                                    for role in (foreground, background))
                    contrast = (values[1] + 0.05) / (values[0] + 0.05)
                    self.assertGreaterEqual(contrast, 3 if group == QPalette.Disabled else 4.5)

    def test_explicit_qt_theme_takes_priority_in_auto(self):
        with patch.dict(os.environ, {"QT_QPA_PLATFORMTHEME": "qt5ct"}):
            controller = self.controller()
            self.portal.change(1)
            QTest.qWait(30)
            self.assertEqual(self.app.palette(), self.light)
            controller.setMode("dark")
            self.assertTrue(self.isDark())
            controller.setMode("auto")
            self.assertEqual(self.app.palette(), self.light)

    def test_newer_signal_wins_over_pending_startup_read(self):
        self.portal.changeDuringRead = 2
        controller = self.controller()
        self.waitFor(lambda: not controller.children())
        self.assertEqual(self.app.palette(), self.light)

    def test_manual_selection_overrides_portal_until_auto_is_selected(self):
        controller = self.controller("light")
        self.waitFor(lambda: not controller.children())
        self.assertEqual(self.app.palette(), self.light)
        controller.setMode("dark")
        self.assertTrue(self.isDark())
        self.portal.change(2)
        self.waitFor(lambda: controller.preference == 2)
        self.assertTrue(self.isDark())
        controller.setMode("auto")
        self.assertEqual(self.app.palette(), self.light)
        for value in (0, 99):
            self.portal.change(1)
            self.waitFor(self.isDark)
            self.portal.change(value)
            self.waitFor(lambda: self.app.palette() == self.light)
            self.assertFalse(self.app.testAttribute(Qt.AA_SetPalette))

    def test_missing_portal_preserves_native_palette_and_allows_manual_modes(self):
        with patch.object(SystemTheme, "SERVICE", "org.example.MissingSettingsPortal"):
            controller = self.controller()
            self.waitFor(lambda: not controller.children())
        self.assertEqual(self.app.palette(), self.light)
        self.assertFalse(self.app.testAttribute(Qt.AA_SetPalette))
        controller.setMode("dark")
        self.assertTrue(self.isDark())
        controller.setMode("light")
        self.assertEqual(self.app.palette(), self.light)

    def test_auto_restores_native_colors_after_manual_selection(self):
        native = QPalette(self.light)
        native.setColor(QPalette.Window, QColor("#123456"))
        self.app.setPalette(native)
        controller = self.controller()
        # Native integration may update the palette while the app is running.
        native.setColor(QPalette.Window, QColor("#345678"))
        self.app.setPalette(native)
        controller.setMode("light")
        self.assertEqual(self.app.palette(), self.light)
        controller.setMode("auto")
        self.assertEqual(self.app.palette(), native)
        self.assertEqual(self.app.palette().resolve(), native.resolve())

    def test_existing_designer_forms_refresh_all_text_and_button_colors(self):
        window = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)
        ui.keyListWidgetContents.setData([KeyValue(), DelayValue(), CommandValue()])
        controller = self.controller()
        self.waitFor(self.isDark)
        for mode in ("dark", "light", "dark"):
            controller.setMode(mode)
            self.app.processEvents()
            palette = self.app.palette()
            for widget in window.findChildren((QPushButton, QLabel, QLineEdit)):
                for role in (QPalette.Button, QPalette.ButtonText,
                             QPalette.WindowText, QPalette.Text, QPalette.Base):
                    with self.subTest(mode=mode, widget=widget.objectName(), role=role):
                        self.assertEqual(widget.palette().color(QPalette.Active, role),
                                         palette.color(QPalette.Active, role))
        window.deleteLater()

    def test_settings_default_save_reload_and_cancel(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.dict(os.environ, {"XDG_CONFIG_HOME": directory}):
            config = ConfigLoader()
            # Simulate a config created before the appearance setting existed.
            with open(config.configFile) as file:
                data = json.load(file)
            del data["settings"]["appearance"]
            with open(config.configFile, "w") as file:
                json.dump(data, file)
            config.load()
            self.assertEqual(config.data.settings.appearance, "auto")
            dialog = SettingsWindow(None, config)
            self.assertEqual([dialog.appearance.itemText(i) for i in range(3)],
                             ["auto (default)", "light", "dark"])
            dialog.appearance.setCurrentIndex(2)
            dialog.accept()
            config.save()
            config.load()
            self.assertEqual(config.data.settings.appearance, "dark")
            reopened = SettingsWindow(None, config)
            self.assertEqual(reopened.appearance.currentData(), "dark")
            reopened.appearance.setCurrentIndex(1)
            reopened.reject()
            self.assertEqual(config.data.settings.appearance, "dark")
            dialog.deleteLater()
            reopened.deleteLater()


if __name__ == "__main__":
    unittest.main()
