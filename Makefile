# get the name of the package to build
PACKAGE := $(shell python -c 'from src.pandex.symbols import __pdext__;print(__pdext__)')

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

PKG_LIB := pandex_tarballs
PY_SETUP := python setup.py
PIP_INSTALL := pip install
PIP_UNINSTALL := pip uninstall -y
FIND_LATEST_FILE := -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" "
TEST_SUITE := $(MAKEFILE_DIR)/tests

CURRENT_VERSION := $(shell python -c 'from src.pandex._build_info import __version__;print(__version__)')
ifndef VERSION 
VERSION := $(CURRENT_VERSION)
endif
PKG_TARBALL := $(shell find $(PKG_LIB)/*whl $(FIND_LATEST_FILE))  

build: clean
	- $(PY_SETUP) sdist bdist_wheel

# Allows for a separate directory of tarball history to be maintained
deploy: build
	-$(eval BUILT_GZ := $(shell find dist/*whl $(FIND_LATEST_FILE)))
	cp $(BUILT_GZ) $(PKG_LIB)

clean:
	-rm -rf dist src/$(PACKAGE).egg-info  __pycache__ .pytest_cache src/$(PACKAGE)/installed_extensions/*.py
	-cp src/$(PACKAGE)/installed_extensions/locations.yml.save src/$(PACKAGE)/installed_extensions/locations.yml

test: clean install
	-cd /tmp && pytest $(PYTEST_FLAGS) $(TEST_SUITE)

ifdef TARBALL
INSTALL_FLAGS=
INSTALL_PKG=$(PKG_TARBALL)
install: deploy install_pkg
else
ifdef EDIT
INSTALL_FLAGS=-e
INSTALL_PKG=.
install: uninstall install_pkg
ifdef PYPI
INSTALL_FLAGS=
INSTALL_PKG=$(PKG_TARBALL)
install: install_pkg
else
install: 
endif
endif
endif

ifdef LIVE
TWINE_FLAGS=
else
TWINE_FLAGS=--repository-url https://test.pypi.org/legacy/
endif

upload:
	- python -m twine upload $(TWINE_FLAGS) dist/*

install_pkg: build
	-$(PIP_INSTALL) $(INSTALL_FLAGS) $(INSTALL_PKG)

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