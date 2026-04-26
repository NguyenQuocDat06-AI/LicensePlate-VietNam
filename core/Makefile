SHELL := /bin/bash

init:
	git submodule update --init --recursive
	python3 -m venv venv
	source venv/bin/activate ; pip install -r requirements.txt ; pip install -r ./LicensePlate/yolov5/requirements.txt

test:
	source venv/bin/activate ; python test.py

run:
	source venv/bin/activate ; python .
