# Copyright 2004-present Facebook. All Rights Reserved.

# @lint-ignore-every PYTHON3COMPATIMPORTS1

# @nolint
"""
Ltr Modbus Tool
"""
from stationexec.logger import log
from stationexec.toolbox.tool import Tool

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import logging

logging.getLogger("pymodbus").setLevel(logging.CRITICAL)

version = "0.1"
dependencies = ["pymodbus"]
default_configurations = {
    "target_address": '10.230.70.10',
    "target_port": 502,
    "control_registers": {
        "c1_run_ttv": 0,
        "c2_target_power": 10,
        "c3_shutdown": 1
    },
    "system_registers":{
        "s1_running_ttv": 0,
        "s2_system_stop": 1,
        "s3_leak_detected": 2,
        "s4_thermal_fault": 3,
        "s5_sensor_fault": 4,
        "s6_duty_cycle_ttv_bus1": 10,
        "s7_duty_cycle_ttv_bus2": 11,
        "s8_duty_cycle_ttv_bus3": 12,
        "s9_duty_cycle_ttv_bus4": 13,
        "s10_duty_cycle_fan_bus1": 14,
        "s11_duty_cycle_fan_bus2": 15,
        "version": 16
    },
    "sensor_registers": {
        "t1_thermo" : { "register": 20, "decimals": 2, "units": "°C"},
        "t2_thermo" : { "register": 21, "decimals": 2, "units": "°C"},
        "t3_thermo" : { "register": 22, "decimals": 2, "units": "°C"},
        "t4_thermo" : { "register": 23, "decimals": 2, "units": "°C"},
        "t5_thermo" : { "register": 24, "decimals": 2, "units": "°C"},
        "t6_thermo" : { "register": 25, "decimals": 2, "units": "°C"},
        "t7_thermo" : { "register": 26, "decimals": 2, "units": "°C"},
        "t8_thermo" : { "register": 27, "decimals": 2, "units": "°C"},
        "t9_inlet_thermo_1" : { "register": 28, "decimals": 2, "units": "°C"},
        "t10_inlet_thermo_2" : { "register": 29, "decimals": 2, "units": "°C"},
        "i1_current_ttv_bus_1" : { "register": 30, "decimals": 2, "units": "amps"},
        "i2_current_ttv_bus_2" : { "register": 31, "decimals": 2, "units": "amps"},
        "i3_current_ttv_bus_3" : { "register": 32, "decimals": 2, "units": "amps"},
        "i4_current_ttv_bus_4" : { "register": 33, "decimals": 2, "units": "amps"},
        "v1_current_ttv_bus_1" : { "register": 34, "decimals": 2, "units": "volts"},
        "v2_current_ttv_bus_2" : { "register": 35, "decimals": 2, "units": "volts"},
        "v3_current_ttv_bus_3" : { "register": 36, "decimals": 2, "units": "volts"},
        "v4_current_ttv_bus_4" : { "register": 37, "decimals": 2, "units": "volts"},
        "t11_outlet_temp_1" : { "register": 38, "decimals": 1, "units": "°C"},
        "t12_outlet_temp_2" : { "register": 39, "decimals": 1, "units": "°C"},
        "a1_external_pot_1" : { "register": 40, "decimals": 0, "units": "raw"},
        "a2_leak_sensor" : { "register": 41, "decimals": 0, "units": "raw"},
        "t13_outlet_temp_3" : { "register": 42, "decimals": 1, "units": "°C"},
        "t14_outlet_temp_4" : { "register": 43, "decimals": 1, "units": "°C"},
        "i5_system_current" : { "register": 44, "decimals": 1, "units": "amps"},
        "d1_toggle_switch" : { "register": 45, "decimals": 0, "units": "raw"},
        "d2_external_leak" : { "register": 46, "decimals": 0, "units": "raw"},
        "f1_rpm_fan1" : { "register": 47, "decimals": 0, "units": "RPM"},
        "f2_rpm_fan2" : { "register": 48, "decimals": 0, "units": "RPM"},
        "f3_rpm_fan3" : { "register": 49, "decimals": 0, "units": "RPM"},
        "f4_rpm_fan4" : { "register": 50, "decimals": 0, "units": "RPM"},
        "f5_rpm_fan5" : { "register": 51, "decimals": 0, "units": "RPM"},
        "f6_rpm_fan6" : { "register": 52, "decimals": 0, "units": "RPM"},
        "f7_rpm_fan7" : { "register": 53, "decimals": 0, "units": "RPM"},
        "f8_rpm_fan8" : { "register": 54, "decimals": 0, "units": "RPM"},
        "fT_fanboard_temperature" : { "register": 55, "decimals": 2, "units": "°C"}
    },
    "emulation_registers": {
        "t1_thermo" : { "register": 120, "decimals": 2, "units": "°C"},
        "t2_thermo" : { "register": 121, "decimals": 2, "units": "°C"},
        "t3_thermo" : { "register": 122, "decimals": 2, "units": "°C"},
        "t4_thermo" : { "register": 123, "decimals": 2, "units": "°C"},
        "t5_thermo" : { "register": 124, "decimals": 2, "units": "°C"},
        "t6_thermo" : { "register": 125, "decimals": 2, "units": "°C"},
        "t7_thermo" : { "register": 126, "decimals": 2, "units": "°C"},
        "t8_thermo" : { "register": 127, "decimals": 2, "units": "°C"},
        "t9_inlet_thermo_1" : { "register": 128, "decimals": 2, "units": "°C"},
        "t10_inlet_thermo_2" : { "register": 129, "decimals": 2, "units": "°C"},
        "i1_current_ttv_bus_1" : { "register": 130, "decimals": 2, "units": "amps"},
        "i2_current_ttv_bus_2" : { "register": 131, "decimals": 2, "units": "amps"},
        "i3_current_ttv_bus_3" : { "register": 132, "decimals": 2, "units": "amps"},
        "i4_current_ttv_bus_4" : { "register": 133, "decimals": 2, "units": "amps"},
        "v1_current_ttv_bus_1" : { "register": 134, "decimals": 2, "units": "volts"},
        "v2_current_ttv_bus_2" : { "register": 135, "decimals": 2, "units": "volts"},
        "v3_current_ttv_bus_3" : { "register": 136, "decimals": 2, "units": "volts"},
        "v4_current_ttv_bus_4" : { "register": 137, "decimals": 2, "units": "volts"},
        "t11_outlet_temp_1" : { "register": 138, "decimals": 1, "units": "°C"},
        "t12_outlet_temp_2" : { "register": 139, "decimals": 1, "units": "°C"},
        "a1_external_pot_1" : { "register": 140, "decimals": 0, "units": "raw"},
        "a2_leak_sensor" : { "register": 141, "decimals": 0, "units": "raw"},
        "t13_outlet_temp_3" : { "register": 142, "decimals": 1, "units": "°C"},
        "t14_outlet_temp_4" : { "register": 143, "decimals": 1, "units": "°C"},
        "i5_system_current" : { "register": 144, "decimals": 1, "units": "amps"},
        "d1_toggle_switch" : { "register": 145, "decimals": 0, "units": "raw"},
        "d2_external_leak" : { "register": 146, "decimals": 0, "units": "raw"},
        "f1_rpm_fan1" : { "register": 147, "decimals": 0, "units": "RPM"},
        "f2_rpm_fan2" : { "register": 148, "decimals": 0, "units": "RPM"},
        "f3_rpm_fan3" : { "register": 149, "decimals": 0, "units": "RPM"},
        "f4_rpm_fan4" : { "register": 150, "decimals": 0, "units": "RPM"},
        "f5_rpm_fan5" : { "register": 151, "decimals": 0, "units": "RPM"},
        "f6_rpm_fan6" : { "register": 152, "decimals": 0, "units": "RPM"},
        "f7_rpm_fan7" : { "register": 153, "decimals": 0, "units": "RPM"},
        "f8_rpm_fan8" : { "register": 154, "decimals": 0, "units": "RPM"},
        "fT_fanboard_temperature" : { "register": 55, "decimals": 2, "units": "°C"}
    },
    "temp_control_group" : ["t9_inlet_thermo_1", "t10_inlet_thermo_2"]
}


class LtrModbus(Tool):
    def __init__(self, **kwargs):
        """ Setup tool with configuration arguments """
        super(LtrModbus, self).__init__(**kwargs)
        self.client = ModbusClient(kwargs['target_address'], port=kwargs['target_port'], timeout=0.5)
        self.control_registers = kwargs["control_registers"]
        self.system_registers = kwargs["system_registers"]
        self.sensor_registers = kwargs["sensor_registers"]
        self.emulation_registers = kwargs["emulation_registers"]

        self.system_monitoring = {}
        self.sensors = {}

        self.temp_control = kwargs["temp_control_group"]

    def initialize(self):
        """ Prepare tool for operation """
        self.client.connect()

    def verify_status(self):
        """ Check that tool is online; attempt to repair if not. Called every 5 seconds. """
        if self.client.is_socket_open():
            self.read_inputs()
            return True
        else:
            return self.client.connect()

    def read_input_register(self, address, decimals):
        val = 0
        try:
            rr = self.client.read_input_registers(address=address, count=1, unit=0x01)
        except Exception:
            rr = None

        if rr is not None:
            if not rr.isError():
                val = rr.registers[0]
                if decimals > 0:
                    val = val / (10 ** decimals)

        return val

    def read_inputs(self):
        for ireg in self.system_registers:
            addr = self.system_registers[ireg]
            self.system_monitoring[ireg] = self.read_input_register(addr, 0)
            self.value_to_ui(f"{self.tool_id}_{ireg}", self.system_monitoring[ireg])

        for ireg in self.sensor_registers:
            addr = self.sensor_registers[ireg]["register"]
            decp = self.sensor_registers[ireg]["decimals"]
            self.sensors[ireg] = self.read_input_register(addr, decp)
            self.value_to_ui(f"{self.tool_id}_{ireg}", self.sensors[ireg])

    def shutdown(self):
        """ Cleanup tool for program shutdown """
        self.client.close()

    def on_ui_command(self, command, **kwargs):
        """ Command received from UI """
        print(f"{command} - {kwargs}")
        if command == "run_ttv":
            self.run_ttv(1)
        elif command == "stop_ttv":
            self.run_ttv(0)
        elif command == "set_power":
            value = int(kwargs.get("value", 0))
            self.set_power(value)
        elif command == "set_temp":
            value = float(kwargs.get("value", 0))
            self.set_temp(value)
        elif command == "shutdown":
            self.shutdown()

    def shutdown(self):
        if self.client.is_socket_open():
            v = 0xdead
            self.client.write_register(self.control_registers["c3_shutdown"], v, unit=0x01)

    def set_temp(self, value):
        if self.client.is_socket_open():
            for ireg in self.temp_control:
                decp = self.emulation_registers[ireg]["decimals"]
                v = int(value * (10 ** decp))
                addr = self.emulation_registers[ireg]["register"]
                print(f"{ireg} - {decp} ({addr}): {v}")
                self.client.write_register(addr, v, unit=0x01)
        self.read_inputs()

    def run_ttv(self, value):
        if self.client.is_socket_open():
            v = int(value)
            self.client.write_register(self.control_registers["c1_run_ttv"], v, unit=0x01)
        self.read_inputs()

    def set_power(self, value):
        if self.client.is_socket_open():
            v = int(value)
            self.client.write_register(self.control_registers["c2_target_power"], v, unit=0x01)
        self.read_inputs()
