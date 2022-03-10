# Copyright 2004-present Facebook. All Rights Reserved.

import time

from stationexec.sequencer.operation import Operation, require_tools, OperationState


version = "0.1"


@require_tools("chassis_1")
class PowerTest(Operation):
    def operation_action(self):
        self.chassis_1.set_power(200)
        self.chassis_1.run_ttv(1)
        time.sleep(5)
        self.chassis_1.run_ttv(0)
