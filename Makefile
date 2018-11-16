VERSION=`cat okp/version.py | sed 's/__version__=//;s/"//g'`

package:
				python setup.py sdist build
				cp dist/okp-${VERSION}.tar.gz dist/okp-current.tar.gz

install:
				pip install dist/okp-current.tar.gz
