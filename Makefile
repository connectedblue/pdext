# get the name of the package to build
PACKAGE := $(shell python -c 'from src.pdext.symbols import __pdext__;print(__pdext__)')

# Controlling whether to install an editable package or from a built tarball
EDIT := true
TARBALL :=

# check if all tests should be run
ifdef TESTALL
PYTEST_SKIP := 
else
PYTEST_SKIP := --skip_this
endif
ifdef TESTSUB
PYTEST_SUBSET := -k $(TESTSUB)
else
PYTEST_SUBSET :=
endif
# allow the tests to support breakpoints

ifdef DEBUG
PYTEST_DEBUG := -s
else
PYTEST_DEBUG :=
endif

PYTEST_FLAGS := $(PYTEST_SKIP) $(PYTEST_DEBUG) $(PYTEST_SUBSET)
# Convenience shortcuts
MAKEFILE_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

PKG_LIB := pdext_tarballs
PY_SETUP := python setup.py
PIP_INSTALL := pip install
PIP_UNINSTALL := pip uninstall -y
FIND_LATEST_FILE := -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" "
TEST_SUITE := $(MAKEFILE_DIR)/tests

CURRENT_VERSION := $(shell python -c 'import versioneer; print(versioneer.get_version())')
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
	-rm -rf dist src/pdext.egg-info  __pycache__ .pytest_cache src/pdext/installed_extensions/*.py
	-cp src/pdext/installed_extensions/locations.yml.save src/pdext/installed_extensions/locations.yml

test: clean install
	-cd /tmp && pytest $(PYTEST_FLAGS) $(TEST_SUITE)

ifdef TARBALL
install: deploy install_tarball
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

all: build doc

doc:
	-rm -rf docs/_build
	-cd docs && make html