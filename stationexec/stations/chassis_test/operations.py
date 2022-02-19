
# Copyright 2004-present Meta. All Rights Reserved.

import time

from stationexec.sequencer.operation import Operation, require_tools, OperationState


version = "0.1"


@require_tools("sn")
class CheckSN(Operation):
    def operation_action(self):
        if self.sn.sn != "":
            self.save_result("sn", sn)
            self.save_result("sn_OK", True)
        else:
            self.save_result("sn_OK", False)


@require_tools("remote")
class SystemUpdate(Operation):
    def operation_action(self):
        if self.remote.connect():
            self.ui_log("Stopping Control Service")
            self.remote.send("sudo systemctl stop ltr_controller.service")
            self.remote.send("sudo fuser -k 502/tcp")
            self.ui_log("Preparing for software update")
            self.remote.change_dir(self.remote_location)
            self.remote.send("rm * -Y")
            self.remote.transfer_file(self.package, self.remote_location)
            self.ui_log("Updating software")
            self.remote.send(f"unzip {self.package} -Y")
            self.remote.send(f"echo {self.sn} > /boot/serial_number") # save serial number as file
            self.remote.send("sudo reboot")
            time.sleep(5)
            self.remote.wait_for_reconnect(5)
            self.save_result("update_result", True)
        else:
            self.save_result("update_result", False)


@require_tools("chassis")
class SystemTest(Operation):
    def operation_action(self):
        version = 3
        time.sleep(5)
        self.chassis.read_inputs()
        s1 = self.chassis.system_monitoring["s1_running_ttv"]
        s2 = self.chassis.system_monitoring["s2_system_stop"]
        s3 = self.chassis.system_monitoring["s3_leak_detected"]
        s4 = self.chassis.system_monitoring["s4_thermal_fault"]
        s5 = self.chassis.system_monitoring["s5_sensor_fault"]

        if "version" in self.chassis.system_monitoring.keys():
            version = self.chassis.system_monitoring["version"]
        self.save_result("version", version)
        self.save_result("s1_running_ttv", s1)
        self.save_result("s2_system_stop", s2)
        self.save_result("s3_leak_detected", s3)
        self.save_result("s4_thermal_fault", s4)
        self.save_result("s5_sensor_fault", s5)


@require_tools("chassis")
class SensorsTest(Operation):
    def operation_action(self):
        result = True
        # TODO: add other sensors and range groups to operations.json and here.
        for s in self.tlist:
            v = self.chassis.sensors[s]
            if v < self.trange[0] or v> self.trange[1]:
                result = False
            self.save_result(s, v)

        self.save_result("test_result", result)


""" @require_tools("chassis", "gpio")
class LeakPortTest(Operation):
    def operation_action(self):
        self.gpio.set(self.gpio_out, 0)
        time.sleep(3)
        self.chassis.read_inputs()

        s3 = self.chassis.system_monitoring["s3_leak_detected"]
        rpt = self.gpio.get(self.gpio_in)

        self.gpio.set(self.gpio_out, 1)
        self.chassis.read_inputs()
        self.save_result("s3_leak_detected", s3)
        self.save_result("leak_report", rpt) """


@require_tools("chassis")
class PowerTest(Operation):
    def operation_action(self):
        self.chassis_1.set_power(self.power_target)
        self.chassis_1.run_ttv(1)
        time.sleep(1)
        s1 = self.chassis.system_monitoring["s1_running_ttv"]

        start = time.time()
        while time.time() - start < self.run_time:
            # check temperature
            tavg = 0
            for s in self.tlist:
                tavg += self.chassis.sensors[s]

            tavg = tavg / 4

            if tavg > self.tmax:
                self.ui_log("Max Temperature exceeded, stopping test")
                break

        self.chassis_1.set_power(0)
        self.chassis_1.run_ttv(0)

        self.save_result("temp", s1)



@require_tools("remote", "ip_tool")
class Provision(Operation):
    def operation_action(self):
        self.remote.connect()
        ip = self.ip_data.get_ip(self.sn)  # implemented
        result = False
        if ip is not None:
            cfg_file = self.ip_data.update_dhcpcfg(ip)  # implemented
            self.remote.transfer_file(cfg_file, "/boot/network/dhcp.conf")
            self.remote.send("sudo reboot")
            self.disconnect()
            time.sleep(15)
            result = self.remote.test_connect(ip)
        else:
            ip = ""
        self.save_result("ip", ip)
        self.save_result("provision_result", result)
