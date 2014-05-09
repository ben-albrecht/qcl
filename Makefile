all: help

help:
	@echo "TARGETS                          "
	@echo "  build   : build python projects"
	@echo "  install : install for system   "
	@echo "  user    : install for user     "
	@echo "  clean   : clean up build files "
	@echo "  help    : print help message   "

build:
	python setup.py build

install:
	python setup.py install

user:
	python setup.py install --user

clean:
	-find . -name \*.pyc | xargs rm
	-rm -rf ./build
