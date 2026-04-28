#!/usr/bin/env python3

# BatteryMon add-on that prints the last saved
# voltage and current measurement for all batteries
#
# Usage:
#  read-voltage.py [--print-json]
#
# JSON format:
#  [
#   [bool_archive_led, bool_alarm_led],
#   [
#    [log from first device],
#    [log from second device],
#     ... ... ...
#    [log from last device]
#   ]
#  ]

import sys
import os
import json
from collections import deque
import batterymon_extras_lib

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.insert(1, batterymon_extras_config.BATTERYMON_DIR)

    batterymon_extras_lib.read_voltage_labels={
        "voltage": batterymon_extras_config.VOLTAGE_LABEL,
        "celldiff": batterymon_extras_config.CELLDIFF_LABEL,
        "percentcapacity": batterymon_extras_config.PERCENTCAPACITY_LABEL,
        "current": batterymon_extras_config.CURRENT_LABEL
    }
else:
    sys.path.insert(1, "/usr/local/share/batterymon")

from lib import batterymon_helpers
from lib import batterymon_gpio_files

batterymon_common=batterymon_helpers.common()

current_out=batterymon_common.CURRENT_OUT
print_json=True if len(sys.argv) > 1 and sys.argv[1] == "--print-json" else False
led_on=batterymon_gpio_files.is_led_on()
led_b_on=batterymon_gpio_files.is_led_b_on()

if os.path.exists(batterymon_common.LOCK_FILE):
    current_out=batterymon_common.BACKUP_OUT

if not print_json:
    if led_on:
        print("[LED] Archiving in progress...")

    if led_b_on:
        print("[LED] ALARM!!!")

if not os.path.exists(current_out):
    if print_json:
        print(json.dumps([[led_on, led_b_on], []]), end="")
    else:
        print("[ERR] "+current_out+" does not exist")

    sys.exit(1)

with open(current_out, "r") as f:
    logs=list(deque(f, maxlen=len(batterymon_common.DEVICES)))

data_to_encode=[None]*len(batterymon_common.DEVICES)

if print_json:
    for log in logs:
        log=batterymon_helpers.parse_log_line(log)

        if log[2] != "OK":
            continue

        if log[3] not in batterymon_common.DEVICES:
            continue

        data_to_encode[batterymon_common.DEVICES.index(log[3])]=log

    print(json.dumps([[led_on, led_b_on], data_to_encode]), end="")

    sys.exit(0)

batterymon_extras_lib.read_voltage_log_params_index(
    batterymon_common.LOG_PARAMS
)

for log in logs:
    log=batterymon_helpers.parse_log_line(log)

    if log[3] not in batterymon_common.DEVICES:
        continue

    data_to_encode[batterymon_common.DEVICES.index(log[3])]=batterymon_extras_lib.read_voltage_main(
        log, "read-voltage"
    )

for item in data_to_encode:
    if item is not None:
        print(item)
