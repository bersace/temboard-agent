all:

VERSION=$(shell python setup.py --version)

release:
ifneq ($(shell git diff --quiet $(VERSION) HEAD; echo $$?), 1)
	$(error Working directory is not at version $(VERSION))
endif
	python setup.py sdist bdist_wheel upload
