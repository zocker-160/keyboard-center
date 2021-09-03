# ![](images/g910-icon.png) G910-gui (WiP)

**(work in progress)**

G910-gui is an application attempting to create an easy way for users to map their macro keys of their >100$ keyboard to useful actions, because Logitech does not give a fuck.

![showcase](images/animation1.gif)

**NOTE:** This application is written for **Linux only**, on Windows use whatever bloatware the vendor wants you to use.

## Supported Keyboards

- Logitech G910 Orion Spectrum (046d:c335)
- Logitech G710+ (046d:c24d) (thanks to @nirenjan)

## Install

### Arch / Manjaro (soon)

Package will be available in the AUR: [g910-gui](https://aur.archlinux.org/packages/g910-gui/)

### Debian / Ubuntu

- Download `.deb` from [release page](https://github.com/zocker-160/G910-gui/releases)
- Install using package manager of your choice or in terminal: `gdebi <packagename>.deb`
- enable and start background service: (**do NOT run as root**)
  - `systemctl --user enable g910-gui.service`
  - `systemctl --user start g910-gui.service` 
  
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