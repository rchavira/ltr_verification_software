# ltr_verification_software
Verification Test software for LTR Chassis
This software is built on the internally developed stationexec framework.

You can download and install the whl package from here

https://github.com/rchavira/stationexec

## software installation

This requires pymodbus and paramiko libraries to run.
    pip install pymodbus paramiko

Copy the contents of /stations and /tools to their respective folders in your stationexec installation.

you can check to make sure that you have coppied the files correctly by running...

    se-station

should list all stations found including "chassis_test"

    se-tool

should list all tools including "ip_tool", "ltr_modbus", "raspi_gpio", "remote_ssh", "sn_check"

## chassis_test station:
Launch software by running the following line

    se-launch chassis-test

This will automatically  open a web browser pointed to http://localhost:8888

To edit configurations of tools (ip address) you can modify the
stationexec/stations/chassis_test/tool_manifest.json file
