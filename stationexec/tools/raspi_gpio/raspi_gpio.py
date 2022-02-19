# Copyright 2004-present Facebook. All Rights Reserved.

# @lint-ignore-every PYTHON3COMPATIMPORTS1

# @nolint
"""
Raspi Gpio Tool
"""
from stationexec.logger import log
from stationexec.toolbox.tool import Tool

import RPi.GPIO as GPIO

version = "0.1"
dependencies = []
default_configurations = {
    "input_pins": [1,2,3],
    "output_pins": [4,5,6]
}


class RaspiGpio(Tool):
    def __init__(self, **kwargs):
        """ Setup tool with configuration arguments """
        super(RaspiGpio, self).__init__(**kwargs)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for p in kwargs["input_pins"]:
            GPIO.setup(p, GPIO.IN)
        for p in kwargs["output_pins"]:
            GPIO.setup(p, GPIO.OUT)

    def initialize(self):
        """ Prepare tool for operation """
        pass

    def verify_status(self):
        """ Check that tool is online; attempt to repair if not. Called every 5 seconds. """
        pass

    def shutdown(self):
        """ Cleanup tool for program shutdown """
        pass

    def on_ui_command(self, command, **kwargs):
        """ Command received from UI """
        if command=="read_input":
            pin = kwargs["pin"]
            value = self.read_digital(pin)
            self.value_to_ui("pin_result", value)
        elif command=="set_output":
            pin = kwargs["pin"]
            value = kwargs["value"]
            self.set_digital(pin, value)
        elif command=="set_high":
            pin = kwargs["pin"]
            self.set_digital(pin, 1)
        elif command=="set_low":
            pin = kwargs["pin"]
            self.set_digital(pin, 0)

    def read_digital(self, pin):
        return GPIO.input(pin)

    def set_digital(self, pin, value):
        GPIO.output(pin, value)
