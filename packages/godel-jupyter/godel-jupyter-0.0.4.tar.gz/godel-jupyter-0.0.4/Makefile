# Note: This is meant for godel-jupyter developer use only
.PHONY: all clean test

export NAME=`python3 setup.py --name 2>/dev/null`
export VERSION=`python3 setup.py --version 2>/dev/null`

all: clean
	python3 setup.py install

clean:
	rm -rf build
	rm -rf dist

test: clean
	pip3 install jupyter_kernel_test nbconvert
	python3 -V 2>&1 | grep "Python 3" && python3 test_kernel.py || echo "Skipping unit test"
	jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=godel-jupyter --ExecutePreprocessor.timeout=60 --stdout godel.ipynb > /dev/null;
	make clean

release: clean
	pip3 install wheel twine
	rm -rf dist build
	python3 setup.py bdist_wheel --universal
	python3 setup.py sdist
	twine check dist/*
	twine upload dist/*