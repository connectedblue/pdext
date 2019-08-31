build:
	-python setup.py sdist

clean:
	-rm dist/*0+*.gz

all: build