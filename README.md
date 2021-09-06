# ![](images/g910-icon.png) Keyboard Center (WiP)

**(work in progress)**

[![DEB builder git](https://github.com/zocker-160/keyboard-center/actions/workflows/debbuilder-git.yml/badge.svg)](https://github.com/zocker-160/keyboard-center/actions/workflows/debbuilder-git.yml)

Keyboard Center is an application attempting to create an easy way for users to map their macro keys of their >100$ keyboard to useful actions, because Logitech does not give a fuck.

![showcase](images/animation1.gif)

**NOTE:** This application is written for **Linux only**, on Windows use whatever bloatware the vendor wants you to use.

## Supported Keyboards

- Logitech G910 Orion Spectrum (046d:c335)
- Logitech G710+ (046d:c24d) (thanks to [@nirenjan](https://github.com/nirenjan))

## Install

### Arch / Manjaro (soon)

Package will be available in the AUR: [keyboard-center](https://aur.archlinux.org/packages/keyboard-center/)

### Debian / Ubuntu

- Download `.deb` from [release page](https://github.com/zocker-160/keyboard-center/releases)
- Install using package manager of your choice or in terminal: `gdebi <packagename>.deb`
- enable and start background service: (**do NOT run as root**)
  - `systemctl --user enable keyboard-center.service`
  - `systemctl --user start keyboard-center.service` 
  
if you are upgrading, please run instead: `systemctl --user daemon-reload`

## Dependencies

### Debian / Ubuntu

- python3
- python3-pip
- python3-pyqt5
- python3-usb
- python3-uinput
- python3-ruamel.yaml
- libnotify-bin
