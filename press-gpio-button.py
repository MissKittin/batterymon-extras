#!/usr/bin/env python3

# BatteryMon add-on that allows you to
# press a GPIO button programmatically

import sys
import os

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.append(batterymon_extras_config.BATTERYMON_DIR)
else:
    sys.path.append("/usr/local/share/batterymon")

from lib import batterymon_common

if os.path.exists(batterymon_common.GPIO_BUTT_SW):
    print("The button is already pressed")
    sys.exit(1)

open(batterymon_common.GPIO_BUTT_SW, "w").close()
os.chmod(batterymon_common.GPIO_BUTT_SW, 0o666)
