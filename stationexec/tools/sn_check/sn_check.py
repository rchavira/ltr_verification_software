# Copyright 2004-present Facebook. All Rights Reserved.

# @lint-ignore-every PYTHON3COMPATIMPORTS1

# @nolint
"""
Sn Check Tool
"""
from stationexec.logger import log
from stationexec.toolbox.tool import Tool

version = "0.1"
dependencies = []
default_configurations = {
}


class SnCheck(Tool):
    def __init__(self, **kwargs):
        """ Setup tool with configuration arguments """
        super(SnCheck, self).__init__(**kwargs)
        self.sn = ""

    def initialize(self):
        """ Prepare tool for operation """
        pass

    def verify_status(self):
        """ Check that tool is online; attempt to repair if not. Called every 5 seconds. """
        self.value_to_ui("serial_number", self.sn)
        pass

    def shutdown(self):
        """ Cleanup tool for program shutdown """
        pass

    def on_ui_command(self, command, **kwargs):
        """ Command received from UI """
        if command == "set_sn":
            sn = kwargs.get("sn","")
            self.set_sn(sn)
        elif command == "clear_sn":
            self.clear_sn()

    def set_sn(self, sn):
        self.sn = sn
        self.value_to_ui("serial_number", self.sn)

    def clear_sn(self):
        self.sn = ""
        self.value_to_ui("serial_number", self.sn)
