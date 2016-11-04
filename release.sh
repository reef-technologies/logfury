#!/bin/bash -eux
version="$1"
pkgname='logfury'

pip install -U "pip>=1.4" "setuptools>=0.9" "wheel>=0.21" twine
git tag "$version"
git push --tags origin master
python setup.py sdist bdist_wheel
#twine register -r pypi "dist/${pkgname}-${version}-py2.py3-none-any.whl"
twine upload -s -r pypi "dist/${pkgname}-${version}-py2.py3-none-any.whl" "dist/${pkgname}-${version}.tar.gz"

echo '-- all ok --'
