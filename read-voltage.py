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
#
# Importing (first method):
#  import sys
#  import importlib.util
#
#  sys.path.insert(1, "/path/to")
#  _read_voltage_spec=importlib.util.spec_from_file_location(
#      "read_voltage",
#      "/path/to/read-voltage.py"
#  )
#  read_voltage=importlib.util.module_from_spec(_read_voltage_spec)
#  _read_voltage_spec.loader.exec_module(read_voltage)
#  context=read_voltage.get_context()
#
#  json_data=read_voltage.get_voltage_data(context)
#  raw_data=read_voltage.get_voltage_data(context, False)
#
# Importing (second method):
#  create a symlink with a valid Python module name
#   ln -s read-voltage.py read_voltage.py
#  then add the directory to sys.path and import normally
#   import sys
#   sys.path.insert(1, "/path/to/batterymon-extras")
#   import read_voltage
#
#   context=read_voltage.get_context()
#
#   json_data=read_voltage.get_voltage_data(context)
#   raw_data=read_voltage.get_voltage_data(context, False)

import sys
import os
import json
from collections import deque
import batterymon_extras_lib

def _get_current_out(context):
    batterymon_common=context[2]
    current_out=batterymon_common.CURRENT_OUT

    if os.path.exists(batterymon_common.LOCK_FILE):
        current_out=batterymon_common.BACKUP_OUT

    return current_out

def output_wrapper(status, full_log, prog, message):
    return message

def get_context(path_insert_index=1):
    global output_wrapper

    if os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/batterymon_extras_config.py"):
        import batterymon_extras_config
        sys.path.insert(path_insert_index, batterymon_extras_config.BATTERYMON_DIR)

        batterymon_extras_lib.read_voltage_labels={
            "voltage": batterymon_extras_config.VOLTAGE_LABEL,
            "celldiff": batterymon_extras_config.CELLDIFF_LABEL,
            "percentcapacity": batterymon_extras_config.PERCENTCAPACITY_LABEL,
            "current": batterymon_extras_config.CURRENT_LABEL
        }
        batterymon_extras_lib.read_voltage_battery_labels=batterymon_extras_config.BATTERY_LABELS
        output_wrapper=batterymon_extras_config.read_voltage_wrapper
    else:
        sys.path.insert(path_insert_index, "/usr/local/share/batterymon")

    from lib import batterymon_helpers as helpers
    from lib import batterymon_gpio_files as gpio

    common=helpers.common()

    return [
        helpers,
        gpio,
        common,
        {name: i for i, name in enumerate(common.DEVICES)} # device_index
    ]

def get_voltage_data(context, as_json=True):
    batterymon_helpers=context[0]
    batterymon_gpio_files=context[1]
    batterymon_common=context[2]
    device_index=context[3]

    current_out=_get_current_out(context)
    led_on=batterymon_gpio_files.is_led_on()
    led_b_on=batterymon_gpio_files.is_led_b_on()

    if not os.path.exists(current_out):
        result=[[led_on, led_b_on], []]
        return json.dumps(result) if as_json else result

    with open(current_out, "r") as f:
        logs=list(deque(f, maxlen=len(batterymon_common.DEVICES)))

    data_to_encode=[None]*len(batterymon_common.DEVICES)

    for log in logs:
        log=batterymon_helpers.parse_log_line(log)

        if log[2] != "OK":
            continue

        idx=device_index.get(log[3])

        if idx is None:
            continue

        data_to_encode[idx]=log

    result=[[led_on, led_b_on], data_to_encode]

    return json.dumps(result) if as_json else result

def print_voltage_data(context, data):
    batterymon_common=context[2]
    device_index=context[3]

    if data[0][0]:
        print(output_wrapper(
            "led", None, "read-voltage",
            "[LED] Archiving in progress..."
        ))

    if data[0][1]:
        print(output_wrapper(
            "led_b", None, "read-voltage",
            "[LED] ALARM!!!"
        ))

    if not data[1]:
        current_out=_get_current_out(context)

        if not os.path.exists(current_out):
            print(output_wrapper(
                "err", None, "read-voltage",
                "[ERR] "+current_out+" does not exist"
            ))
        else:
            print(output_wrapper(
                "err", None, "read-voltage",
                "[ERR] No valid data"
            ))

        return 1

    batterymon_extras_lib.read_voltage_log_params_index(
        batterymon_common.LOG_PARAMS
    )

    data_to_encode=[None]*len(batterymon_common.DEVICES)

    for log in data[1]:
        if log is None:
            continue

        idx=device_index.get(log[3])

        if idx is None:
            continue

        data_to_encode[idx]=batterymon_extras_lib.read_voltage_main(
            log, output_wrapper, "read-voltage"
        )

    for item in data_to_encode:
        if item is not None:
            print(item)

    return 0

if __name__ == "__main__":
    context=get_context()
    print_json=True if len(sys.argv) > 1 and sys.argv[1] == "--print-json" else False
    data=get_voltage_data(context, print_json)

    if print_json:
        print(data, end="")
    else:
        sys.exit(
            print_voltage_data(context, data)
        )
