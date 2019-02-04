#!/usr/bin/make

.PHONY: robot-server
robot-server:
	bin/robot-server -v collective.contact.core.testing.ACCEPTANCE

.PHONY: robot-test
robot-test:
	# can be run by example with: make robot-test opt='-t "Directory *"'
	bin/robot $(opt) src/collective/contact/core/tests/robot/test_contacts.robot
