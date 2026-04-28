#!/usr/bin/env python3

# BatteryMon add-on that prints data
# from archived logs in a simple form
# (equivalent to read-voltage.py)
#
# Usage:
#  read-arch-voltage.py /media/batterymon/batterymon/archive/file1.txt.gz [/media/batterymon/batterymon/archive/file2.txt.gz] [/media/batterymon/batterymon/archive/file3.txt.gz]
#  read-arch-voltage.py /media/batterymon/batterymon/archive/*.txt.gz

import sys
import os
import platform
import gzip
import batterymon_extras_lib

if platform.system() == "Windows":
    import glob

    def glob_path(array):
        files=[]

        for arg in array:
            matched=glob.glob(arg)

            if matched:
                files.extend(matched)

        if not files:
            print("Arguments did not match any files")
            sys.exit(1)

        return files
else:
    def glob_path(array):
        for arg in array:
            if not os.path.isfile(arg):
                print(arg+" is not a file")
                sys.exit(1)

        return array

def open_log_file(path):
    try:
        f=gzip.open(path, "rb")
        f.peek(1)

        return f
    except(gzip.BadGzipFile):
        return open(path, "rb")

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.insert(1, batterymon_extras_config.BATTERYMON_DIR)

    batterymon_extras_lib.read_voltage_labels={
        "voltage": batterymon_extras_config.VOLTAGE_LABEL,
        "celldiff": batterymon_extras_config.CELLDIFF_LABEL,
        "percentcapacity": batterymon_extras_config.PERCENTCAPACITY_LABEL,
        "current": batterymon_extras_config.CURRENT_LABEL
    }
    batterymon_extras_lib.read_voltage_battery_labels=batterymon_extras_config.BATTERY_LABELS
    output_wrapper=batterymon_extras_config.read_voltage_wrapper
else:
    sys.path.insert(1, "/usr/local/share/batterymon")

    def output_wrapper(status, full_log, prog, message):
        return message

from batterymon_lib import batterymon_helpers

if len(sys.argv) < 2:
    print("Usage: "+sys.argv[0]+" /media/batterymon/batterymon/journal/file1.txt.gz [/media/batterymon/batterymon/journal/file2.txt.gz] [/media/batterymon/batterymon/journal/file3.txt.gz]")
    sys.exit(1)

batterymon_common=batterymon_helpers.common()
batterymon_extras_lib.read_voltage_log_params_index(
    batterymon_common.LOG_PARAMS
)

for arg in glob_path(sys.argv[1:]):
    try:
        with open_log_file(arg) as file:
            current_line=1

            for line in file:
                try:
                    print(batterymon_extras_lib.read_voltage_main(
                        batterymon_helpers.parse_log_line(line.decode("utf-8")),
                        output_wrapper, "read-arch-voltage"
                    ))
                except(UnicodeDecodeError):
                    print(output_wrapper(
                        "ude", None, "read-arch-voltage",
                        arg+": line "+str(current_line)+": unicode decode error"
                    ))

                current_line+=1
    except(Exception) as e:
        print(output_wrapper(
            "err", None, "read-arch-voltage",
            "[ERR] "+arg+": "+str(e)
        ))
