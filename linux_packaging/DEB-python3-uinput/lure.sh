# Maintainer: johnjq <dev [at] johnjq (dot) com>
# Co-maintainer: Ewout van Mansom <ewout@vanmansom.name>
## shamelessly stolen from AUR

maintainer="zocker_160 <zocker1600 at posteo dot net>"

name=python3-uinput
_version=0.11.2
version=${_version}~zocker1
release=1
desc="Pythonic API to Linux uinput kernel module (patched for Python 3.11)"
homepage="https://github.com/tuomasjjrasanen/python-uinput"
architectures=('all')
licenses=('GPLv3')

deps=('python3')
build_deps=('python3-setuptools' 'python3-setuptools-whl' 'python3-build' 'python3-installer')

sources=(
    "git+https://github.com/tuomasjjrasanen/python-uinput.git?~rev=$_version"
    "https://patch-diff.githubusercontent.com/raw/tuomasjjrasanen/python-uinput/pull/41.patch"
)
checksums=(
    'SKIP'
    "sha512:a53b925d1314e24a13703f598eec4774452bfa33046d0d15a04aa70d2ddfe77ab08c6fb46e8b947adce9f3a9e8d27d0e923233e8cac66f6ab46a0d9e9a5d02ec"
)

prepare() {
    cd "$srcdir/python-uinput"
    patch --forward --strip=1 --input="$srcdir/41.patch"
}

build() {
    cd "$srcdir/python-uinput"
    python3 -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/python-uinput"
    python3 -m installer --destdir="$pkgdir" dist/*.whl
    install-license COPYING $name/LICENSE
}
