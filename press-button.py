#!/usr/bin/env python3

# BatteryMon add-on that allows you to
# press a GPIO button programmatically

import sys
import os

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.insert(1, batterymon_extras_config.BATTERYMON_DIR)
else:
    sys.path.insert(1, "/usr/local/share/batterymon")

from lib import batterymon_gpio_files

if batterymon_gpio_files.is_butt_pressed():
    print("The button is already pressed")
    sys.exit(1)

batterymon_gpio_files.butt_press()
