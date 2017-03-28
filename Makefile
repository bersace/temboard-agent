VERSION=$(shell python setup.py --version)

release:
ifneq ($(shell git log $(VERSION)..HEAD), '')
	$(error Working directory is not at version $(VERSION))
endif
	python setup.py sdist bdist_wheel upload
