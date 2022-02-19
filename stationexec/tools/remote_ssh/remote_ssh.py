# Copyright 2004-present Facebook. All Rights Reserved.

# @lint-ignore-every PYTHON3COMPATIMPORTS1

# @nolint
"""
Remote Ssh Tool
"""
from stationexec.logger import log
from stationexec.toolbox.tool import Tool
import paramiko

version = "0.1"
dependencies = ["paramiko"]
default_configurations = {
    "host" : "10.230.70.10",
    "port" : 22,
    "username" : "pi",
    "password" : "raspberry"
}


class RemoteSsh(Tool):
    def __init__(self, **kwargs):
        """ Setup tool with configuration arguments """
        super(RemoteSsh, self).__init__(**kwargs)
        self.host = kwargs["host"]
        self.port = kwargs["port"]
        self.username = kwargs["username"]
        self.password = kwargs["password"]

    def initialize(self):
        """ Prepare tool for operation """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def verify_status(self):
        """ Check that tool is online; attempt to repair if not. Called every 5 seconds. """
        self.is_connected()
        return True

    def shutdown(self):
        """ Cleanup tool for program shutdown """
        pass

    def on_ui_command(self, command, **kwargs):
        """ Command received from UI """
        if command=="connect":
            self.connect()
        elif command == "disconnect":
            self.disconnect()
        elif command == "test_connection":
            ip = kwargs["ip"]
            self.test_connection(ip)
        elif command == "send_command":
            cmd = kwargs["send_command"]
            self.send(cmd)
        elif command == "transfer_file":
            source = kwargs["source"]
            dest = kwargs["dest"]
            self.transfer_file(source, dest)
        elif command == "start_service":
            self.start_ltr_service()
        elif command == "stop_service":
            self.stop_ltr_service()
        elif command == "get_service":
            self.get_ltr_service_status()
        elif command == "set_fan":
            dc = int(kwargs["dc"])
            self.set_ltr_fan(dc)
        elif command == "set_ttv":
            dc = int(kwargs["dc"])
            self.set_ltr_ttv(dc)

    def connect(self):
        self.ssh.connect(self.host, self.port, self.username, self.password)
        return self.is_connected()

    def is_connected(self):
        result = False
        if self.ssh.get_transport() is not None:
            result = self.ssh.get_transport().is_active()
        self.value_to_ui(f"{self.tool_id}_client_connected", result)
        return result

    def disconnect(self):
        self.ssh.close()

    def test_connection(self, ip):
        with paramiko.SSHClient() as st:
            st.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            st.connect(ip, self.port, self.username, self.password)
            if st.get_transport() is not None:
                result = st.get_transport().is_active()
            else:
                result = False
            st.close()
        self.value_to_ui(f"{self.tool_id}_test_connection_result", result)
        return result

    def send(self, cmd):
        if not self.is_connected():
            self.connect()
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        output = stdout.readlines()
        self.value_to_ui(f"{self.tool_id}_cmd_stdout", output)
        if stderr:
            err = stderr.readlines()
            self.value_to_ui(f"{self.tool_id}_cmd_stderr", err)

    def transfer_file(self, source, destination):
        if not self.is_connected():
            self.connect()
        with self.ssh.open_sftp() as ftp:
            ftp.put(source, destination)
            ftp.close()

    def wait_for_reconnect(self, timeout):
        t = 0
        while not self.is_connected():
            time.sleep(1)
            t += 1
            if t > timeout:
                break

        return self.is_connected()

    def stop_ltr_service(self):
        self.send("sudo systemctl stop ltr_controller.service")
        self.send("sudo fuser -k 502/tcp")

    def start_ltr_service(self):
        self.send("sudo systemctl start ltr_controller.service")

    def get_ltr_service_status(self):
        self.send("systemctl status ltr_controller.service")

    def set_ltr_fan(self, dc):
        self.send(f"python /home/pi/ltr_interface/fan_control.py {dc}")

    def set_ltr_ttv(self, dc):
        self.send(f"python /home/pi/ltr_interface/ttv_control.py {dc}")
