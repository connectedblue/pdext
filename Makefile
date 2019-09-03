PACKAGE := pdext

# Controlling whether to install an editable package or from a built tarball
EDIT := true
TARBALL :=


# Convenience shortcuts
PKG_LIB := pdext_tarballs
PY_SETUP := python setup.py
PIP_INSTALL := pip install
PIP_UNINSTALL := pip uninstall -y
FIND_LATEST_FILE := -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" "

CURRENT_VERSION := $(shell python -c 'from pdext._version import get_versions; v = get_versions();print(v.get("closest-tag", v["version"]))')
ifndef VERSION 
VERSION := $(CURRENT_VERSION)
endif
PKG_TARBALL := $(PKG_LIB)/$(PACKAGE)-$(VERSION).tar.gz

build: clean
	- $(PY_SETUP) sdist

# Allows for a separate directory of tarball history to be maintained
deploy: build
	-$(eval BUILT_GZ := $(shell find dist $(FIND_LATEST_FILE)))
	cp $(BUILT_GZ) $(PKG_LIB)

clean:
	-rm -rf dist pdext.egg-info  __pycache__



ifdef TARBALL
install: uninstall install_tarball
else
ifdef EDIT
install: uninstall install_editable
else
install: 
endif
endif

install_tarball:
	-$(PIP_INSTALL) $(PKG_TARBALL)

install_editable:
	-$(PIP_INSTALL) -e .

uninstall:
	-$(PIP_UNINSTALL) $(PACKAGE)

all: build