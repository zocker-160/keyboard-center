"""Select light, dark or the desktop's native Qt appearance."""

import os
import sys

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtDBus import (
    QDBusConnection,
    QDBusMessage,
    QDBusPendingCallWatcher,
    QDBusPendingReply,
    QDBusVariant,
)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QStyleFactory


def darkPalette(lightPalette: QPalette) -> QPalette:
    palette = QPalette(lightPalette)
    colors = {
        QPalette.Window: "#2b2b2b",
        QPalette.WindowText: "#f0f0f0",
        QPalette.Base: "#202020",
        QPalette.AlternateBase: "#303030",
        QPalette.Text: "#f0f0f0",
        QPalette.Button: "#353535",
        QPalette.ButtonText: "#f0f0f0",
        QPalette.ToolTipBase: "#353535",
        QPalette.ToolTipText: "#f0f0f0",
        QPalette.BrightText: "#ffffff",
        QPalette.Highlight: "#2b66a3",
        QPalette.HighlightedText: "#ffffff",
        QPalette.Link: "#80bfff",
        QPalette.LinkVisited: "#c4a5ff",
        QPalette.PlaceholderText: "#a0a0a0",
        QPalette.Light: "#606060",
        QPalette.Midlight: "#454545",
        QPalette.Mid: "#2b2b2b",
        QPalette.Dark: "#1c1c1c",
        QPalette.Shadow: "#101010",
    }
    for role, color in colors.items():
        palette.setColor(role, QColor(color))

    for role in (QPalette.WindowText, QPalette.Text, QPalette.ButtonText,
                 QPalette.HighlightedText, QPalette.PlaceholderText):
        palette.setColor(QPalette.Disabled, role, QColor("#909090"))
    palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor("#454545"))
    return palette


class SystemTheme(QObject):
    """Manage the application palette and the desktop's appearance preference.

    Auto leaves native/custom Qt themes in control. With Qt's default Fusion
    appearance, it uses the XDG Settings portal to fill Qt 5's missing GTK color
    integration. Portal requests are asynchronous and independent of X11/Wayland.
    """

    SERVICE = "org.freedesktop.portal.Desktop"
    PATH = "/org/freedesktop/portal/desktop"
    INTERFACE = "org.freedesktop.portal.Settings"
    NAMESPACE = "org.freedesktop.appearance"
    KEY = "color-scheme"

    def __init__(self, app: QApplication, mode: str = "auto"):
        super().__init__(app)
        self.app = app
        self.nativePalette = app.palette()
        self.nativeStyle = app.style().objectName()
        self.lightPalette = QStyleFactory.create("Fusion").standardPalette()
        # Include every role so a dark native theme cannot supply light-mode
        # colors that Fusion leaves unspecified (such as links).
        self.lightPalette.resolve((1 << QPalette.NColorRoles) - 1)
        self.preference = 0
        self.receivedChange = False

        # Respect desktop integration plugins, user overrides and custom colors.
        platformTheme = os.environ.get("QT_QPA_PLATFORMTHEME", "")
        explicitStyle = any(
            arg.split("=", 1)[0] in (
                "-style", "--style", "-stylesheet", "--stylesheet",
                "-platformtheme", "--platformtheme",
            )
            for arg in sys.argv[1:]
        )
        self.preferNative = bool(
            platformTheme not in ("", "gtk3")
            or os.environ.get("QT_STYLE_OVERRIDE")
            or explicitStyle
            or app.styleSheet()
            or self.nativeStyle.lower() != "fusion"
            or self.nativePalette != app.style().standardPalette()
        )
        self.setMode(mode)
        if self.preferNative:
            return

        self.bus = QDBusConnection.sessionBus()
        if not self.bus.isConnected():
            return

        self.bus.connect(
            self.SERVICE, self.PATH, self.INTERFACE, "SettingChanged",
            self._settingChanged,
        )
        # Read is supported by both versions of the Settings portal interface.
        message = QDBusMessage.createMethodCall(
            self.SERVICE, self.PATH, self.INTERFACE, "Read",
        )
        message.setArguments([self.NAMESPACE, self.KEY])
        watcher = QDBusPendingCallWatcher(self.bus.asyncCall(message, 1000), self)
        watcher.finished.connect(self._readFinished)

    @pyqtSlot(QDBusPendingCallWatcher)
    def _readFinished(self, watcher):
        reply = QDBusPendingReply(watcher)
        # A signal received while Read was in flight is newer than its reply.
        if not reply.isError() and not self.receivedChange:
            self._applyPreference(reply.value())
        watcher.deleteLater()

    @pyqtSlot(str, str, QDBusVariant)
    def _settingChanged(self, namespace, key, value):
        if namespace == self.NAMESPACE and key == self.KEY:
            self.receivedChange = True
            self._applyPreference(value)

    def _applyPreference(self, value):
        # Older portals return a variant inside another variant for Read.
        while isinstance(value, QDBusVariant):
            value = value.variant()
        # 1 = dark, 2 = light; 0 and unknown values mean no preference.
        self.preference = value
        self._applyAppearance()

    def setMode(self, mode: str):
        if getattr(self, "mode", None) == "auto" and self.preferNative:
            # The desktop can change its theme while Auto is active. Preserve
            # its latest style and explicit palette overrides, not startup colors.
            self.nativeStyle = self.app.style().objectName()
            self.nativePalette = self.app.palette()
        self.mode = mode if mode in ("auto", "light", "dark") else "auto"
        self._applyAppearance()

    def _applyAppearance(self):
        if self.mode == "auto" and (self.preferNative or self.preference not in (1, 2)):
            style, palette = self.nativeStyle, self.nativePalette
        else:
            useDark = self.mode == "dark" or (self.mode == "auto" and self.preference == 1)
            style = "Fusion"
            palette = darkPalette(self.lightPalette) if useDark else self.lightPalette
        if self.app.style().objectName().lower() != style.lower():
            self.app.setStyle(style)
        current = self.app.palette()
        # Equal colors can still have different overrides. Restoring the native
        # resolve mask lets Qt follow future desktop palette changes again.
        if current == palette and current.resolve() == palette.resolve():
            return
        self.app.setPalette(palette)
        # Qt 5 caches inherited palettes in styled widgets, even when their CSS
        # does not set colors. Repolish the existing forms after a palette change.
        for widget in self.app.allWidgets():
            if widget.styleSheet():
                widget.setStyleSheet(widget.styleSheet())
