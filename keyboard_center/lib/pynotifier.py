"""
py-notifier: Display desktop notifications on Windows, Linux and MacOS.

Copyright (c) 2018, 2021 Yuriy Lisovskiy

Distributed under the MIT licence,
see the accompanying file LICENSE.
"""

import platform
import shutil
import subprocess


class Notification:
    """Display desktop notifications on Windows, Linux and MacOS."""

    def __init__(
        self,
        title,
        description="",
        duration=5,
        urgency="low",
        icon_path=None,
        app_name=None,
    ):
        """
        Construct with notification properties.

        'title' - a title of notification.
        'description' - more info about the notification.
        'duration' - notification timeout in seconds.
        'urgency' - notification urgency level (ignored under Windows);
                                possible values: 'low', 'normal', 'critical'.
        'icon_path' - path to notification icon file.
        'app_name' - name of app sending notification (Linux only).
        """
        if title is None:
            raise ValueError("title with None value is not allowed")

        if title == "":
            raise ValueError("title must not be empty")

        system = platform.system().lower()

        platforms = ["windows", "linux", "darwin"]
        if system not in platforms:
            raise SystemError(
                "notifications are not supported for {} system".format(system)
            )

        if system == "linux" and urgency not in ["low", "normal", "critical", None]:
            raise ValueError("invalid urgency was given: {}".format(urgency))

        self.system = system
        self.__title = title
        self.__description = description
        self.__duration = duration
        self.__urgency = urgency
        self.__icon_path = icon_path
        self.__app_name = app_name

    def send(self):
        """Send the notification."""
        # https://stackoverflow.com/questions/3951840/how-to-invoke-a-function-on-an-object-dynamically-by-name
        getattr(self, f"send_{self.system}")()

    def send_linux(self):
        """Notify on linux with notify-send."""
        if shutil.which("notify-send") is None:
            raise SystemError(
                "Please install libnotify-bin\n\tsudo apt-get install libnotify-bin"
            )

        command = [
            "notify-send",
            "{}".format(self.__title),
            "{}".format(self.__description),
            "-t",
            "{}".format(self.__duration * 1000),
        ]
        if self.__urgency is not None:
            command += ["-u", self.__urgency]

        if self.__icon_path is not None:
            command += ["-i", self.__icon_path]

        if self.__app_name is not None:
            command += ["-a", self.__app_name]

        subprocess.Popen(command, shell=False)

    def send_windows(self):
        """Notify on windows with win10toast."""
        raise NotImplementedError

    def send_darwin(self):
        """Notify on macos with pync."""
        raise NotImplementedError
