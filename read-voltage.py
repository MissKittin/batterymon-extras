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

voltage_label="Voltage"
celldiff_label="CellDiff"
percentcapacity_label="PercentCapacity"
current_label="Current"

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.append(batterymon_extras_config.BATTERYMON_DIR)

    voltage_label=batterymon_extras_config.VOLTAGE_LABEL
    celldiff_label=batterymon_extras_config.CELLDIFF_LABEL
    percentcapacity_label=batterymon_extras_config.PERCENTCAPACITY_LABEL
    current_label=batterymon_extras_config.CURRENT_LABEL
else:
    sys.path.append("/usr/local/share/batterymon")

from lib import batterymon_helpers

batterymon_common=batterymon_helpers.common()

current_out=batterymon_common.CURRENT_OUT
print_json=True if len(sys.argv) > 1 and sys.argv[1] == "--print-json" else False
led_on=os.path.exists(batterymon_common.GPIO_LED_IND)
led_b_on=os.path.exists(batterymon_common.GPIO_LED_B_IND)

if os.path.exists(batterymon_common.LOCK_FILE):
    current_out=batterymon_common.BACKUP_OUT

if not print_json:
    if led_on:
        print("[LED] Archiving in progress...")

    if led_b_on:
        print("[LED] ALARM!!!")

if not os.path.exists(current_out):
    if print_json:
        print(json.dumps([[led_on, led_b_on], []]))
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

    print(json.dumps([[led_on, led_b_on], data_to_encode]))

    sys.exit(0)

log_params_index={name: batterymon_common.LOG_PARAMS.index(name)+4 for name in (
    voltage_label,
    celldiff_label,
    percentcapacity_label,
    current_label
)}

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

    if log[3] not in batterymon_common.DEVICES:
        continue

    index=batterymon_common.DEVICES.index(log[3])

    try:
        voltage=float(log[log_params_index[voltage_label]])
        need_balance=" [B]" if float(log[log_params_index[celldiff_label]]) >= 0.05 else ""

        data_to_encode[index]=log[1]+" "+log[3]+": " \
        +   str(round(float(log[log_params_index[percentcapacity_label]]), 3))+"% " \
        +   str(round(voltage, 3))+"V " \
        +   str(round(float(log[log_params_index[current_label]])*voltage, 3))+"W" \
        +   need_balance
    except(ValueError, IndexError):
        data_to_encode[index]=log[1]+" "+log[3]+": float conversion error"
        continue

for item in data_to_encode:
    if item is not None:
        print(item)
