# Copyright 2004-present Facebook. All Rights Reserved.

# @lint-ignore-every PYTHON3COMPATIMPORTS1
import webbrowser

from stationexec.logger import log
from stationexec.station.events import emit_event, InfoEvents
from stationexec.toolbox.toolbox import get_tools

version = "0.1"
dependencies = []

get_cfg = None


def initialize(register, _get_cfg):
    """ Setup station and register for events """
    global get_cfg
    get_cfg = _get_cfg
    register(InfoEvents.SERVER_STARTED, on_startup)


def on_ui_command(command, **data):
    if command == "set_sn":
        test_examples()


def on_startup(**data):
    webbrowser.open("http://localhost:8888", new=2)


@get_tools("sn")
def set_sn(tools, sn):
    tools.sn.set_sn(sn)
