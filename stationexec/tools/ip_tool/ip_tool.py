# Copyright 2004-present Facebook. All Rights Reserved.

# @lint-ignore-every PYTHON3COMPATIMPORTS1

# @nolint
"""
Ip Tool Tool
"""
from stationexec.logger import log
from stationexec.toolbox.tool import Tool
import json
import os


version = "0.1"
dependencies = []
default_configurations = {
    "iplist_location": "c:\\stationexec\\tools\\ip_tool\\iplist.json",
    "dhcp_conf_location": "c:\\stationexec\\tools\\ip_tool\\dhcpcd.conf",
    "dhcp_template_location": "c:\\stationexec\\tools\\ip_tool\\dhcpcd.template",
}


class IpTool(Tool):
    def __init__(self, **kwargs):
        """ Setup tool with configuration arguments """
        super(IpTool, self).__init__(**kwargs)
        self.iplist_file = kwargs["iplist_location"]
        self.dhcp_file = kwargs["dhcp_conf_location"]
        self.dhcp_template_file = kwargs["dhcp_template_location"]
        self.iplist = {}
        self.last_ip = ""

    def initialize(self):
        """ Prepare tool for operation """
        self._read_iplist()

    def verify_status(self):
        """ Check that tool is online; attempt to repair if not. Called every 5 seconds. """
        pass

    def shutdown(self):
        """ Cleanup tool for program shutdown """
        pass

    def on_ui_command(self, command, **kwargs):
        """ Command received from UI """
        if command == "get_ip":
            sn = kwargs["sn"]
            self.get_ip(sn)
        elif command == "add_ip_range":
            start = kwargs["start"]
            end = kwargs["end"]
            self.add_ip_range(start, end)
        elif command == "update_dhcp_cfg":
            ip = kwargs["ip"]
            self.update_dhcpcfg(ip)
        elif command == "read_ip_list":
            self._read_iplist()

    def _read_iplist(self):
        with open(self.iplist_file) as json_file:
            self.iplist = json.load(json_file)

        self.value_to_ui("ip_list", json.dumps(self.iplist))

    def _save_iplist(self):
        with open(self.iplist_file, 'w') as outfile:
            json.dump(self.iplist, outfile)

        self.value_to_ui("ip_list", json.dumps(self.iplist))

    def add_ip_range(self, start, end):
        self._read_iplist()
        ip = start.split('.')
        for i in range(int(ip[3]), int(end.split('.')[3])+1):
            ipsub = ".".join(ip[0:3])
            ipstr = f"{ipsub}.{i}"
            if ipstr not in self.iplist.keys():
                self.iplist[ipstr] = "Available"
        self._save_iplist()

    def get_ip(self, sn):
        self._read_iplist()
        for ip in self.iplist.keys():
            if self.iplist[ip] == "Available":
                self.iplist[ip] = sn
                self.value_to_ui("get_ip_request", ip)
                self.last_ip = ip
                self._save_iplist()
                return ip
        self.value_to_ui("get_ip_request", "N/A")
        return None

    def update_dhcpcfg(self, ip):
        with open(self.dhcp_template_file) as tempfile:
            dhcp_cfg = tempfile.read()

        dhcp_cfg = dhcp_cfg.replace("{IP_ADDRESS}", ip)

        if os.path.exists(self.dhcp_file):
            os.remove(self.dhcp_file)

        with open(self.dhcp_file, "w") as outfile:
            outfile.write(dhcp_cfg)

        return self.dhcp_file
