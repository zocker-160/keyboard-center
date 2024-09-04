maintainer="zocker_160 <zocker1600 at posteo dot net>"

name=keyboard-center
version=2.0.2
release=1
desc="Application to map G-keys on (some) Logitech Gaming Keyboards"
homepage="https://github.com/zocker-160/keyboard-center"
architectures=('amd64')
licenses=('GPLv3')
conflicts=('keyboard-center-git')

deps=(
  'python3.12'
  'python3-pyqt5'
  'python3-uinput'
  'python3-usb'
  'python3-setuptools'
  'python3-lupa'
  'libhidapi-hidraw0' 'udev' 'libnotify-bin'
)
#build_deps=('git')
opt_deps=(
  'openrgb: RGB control for your keyboard'
)

sources=("git+http://github.com/zocker-160/keyboard-center.git?~rev=$version")
checksums=('SKIP')

scripts=(
  ['postinstall']='postinst'
  ['postremove']='postrm'
  ['postupgrade']='postupgrade'
  ['preremove']='prerm'
)

package() {
  cd "$srcdir/keyboard-center"

  mkdir -p "$pkgdir/opt/$name/src"
  cp -r src "$pkgdir/opt/$name"

  install -D -m644 linux_packaging/60-keyboard-center.rules -t "$pkgdir/usr/lib/udev/rules.d"
  install -D -m644 linux_packaging/uinput-keyboard-center.conf "$pkgdir/usr/lib/modules-load.d/$name.conf"
  install -D -m644 linux_packaging/assets/keyboard-center.png -t "$pkgdir/usr/share/icons/hicolor/512x512/apps"

  install-binary linux_packaging/assets/keyboard-center.sh $name
  install-license LICENSE $name/LICENSE
  install-desktop linux_packaging/assets/keyboard-center.desktop
}
