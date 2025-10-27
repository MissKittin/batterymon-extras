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

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.append(batterymon_extras_config.BATTERYMON_DIR)
else:
    sys.path.append("/usr/local/share/batterymon")

from lib import batterymon_helpers

batterymon_common=batterymon_helpers.common()

logs=[]
current_out=batterymon_common.CURRENT_OUT
print_json=True if len(sys.argv) > 1 and sys.argv[1] == "--print-json" else False
led_on=False
led_b_on=False

if os.path.exists(batterymon_common.LOCK_FILE):
    current_out=batterymon_common.BACKUP_OUT

if not print_json and os.path.exists(batterymon_common.GPIO_LED_IND):
    led_on=True
    print("[LED] Archiving in progress...")

if not print_json and os.path.exists(batterymon_common.GPIO_LED_B_IND):
    led_b_on=True
    print("[LED] ALARM!!!")

if not os.path.exists(current_out):
    if print_json:
        print(json.dumps([[led_on, led_b_on], []]))
    else:
        print("[ERR] "+current_out+" does not exist")

    sys.exit(1)

with open(current_out, "r") as f:
    logs.extend(deque(f, maxlen=len(batterymon_common.DEVICES)))

if print_json:
    data_to_encode=[]

    for log in logs:
        log=batterymon_helpers.parse_log_line(log)

        if log[2] != "OK":
            continue

        data_to_encode.append(log)

    print(json.dumps([[led_on, led_b_on], data_to_encode]))
    sys.exit(0)

for log in logs:
    log=batterymon_helpers.parse_log_line(log)

    if log[2] == "VE":
        print(log[1]+" "+log[3]+": ValueError")
        continue

    if log[2] == "EX":
        print(log[1]+" "+log[3]+": Exception")
        continue

    if log[2] == "RL":
        print(log[1]+": Reading locked")
        continue

    if log[2] != "OK":
        print(log[1]+" "+log[3]+": NOT OK")
        continue

    try:
        voltage=float(log[batterymon_common.LOG_PARAMS.index("Voltage")+4])
        need_balance=""

        if float(log[batterymon_common.LOG_PARAMS.index("CellDiff")+4]) >= 0.05:
            need_balance=" [B]"

        print(log[1]+" "+log[3]+": "
        +   str(round(float(log[batterymon_common.LOG_PARAMS.index("PercentCapacity")+4]), 3))+"% "
        +   str(round(voltage, 3))+"V "
        +   str(round(float(log[batterymon_common.LOG_PARAMS.index("Current")+4])*voltage, 3))+"W"
        +   need_balance
        )
    except (ValueError, IndexError):
        print(log[1]+" "+log[3]+": float conversion error")
        continue
