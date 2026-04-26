SHELL := /bin/bash

init:
	${MAKE} -C core init

test:
	${MAKE} -C core test

run:
	${MAKE} -C core run
