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

voltage_label="Voltage"
celldiff_label="CellDiff"
percentcapacity_label="PercentCapacity"
current_label="Current"

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
    sys.path.append(batterymon_extras_config.BATTERYMON_DIR)

    voltage_label=batterymon_extras_config.VOLTAGE_LABEL
    celldiff_label=batterymon_extras_config.CELLDIFF_LABEL
    percentcapacity_label=batterymon_extras_config.PERCENTCAPACITY_LABEL
    current_label=batterymon_extras_config.CURRENT_LABEL
else:
    sys.path.append("/usr/local/share/batterymon")

from lib import batterymon_helpers

if len(sys.argv) < 2:
    print("Usage: "+sys.argv[0]+" /media/batterymon/batterymon/journal/file1.txt.gz [/media/batterymon/batterymon/journal/file2.txt.gz] [/media/batterymon/batterymon/journal/file3.txt.gz]")
    sys.exit(1)

batterymon_common=batterymon_helpers.common()
log_params_index={name: batterymon_common.LOG_PARAMS.index(name)+4 for name in (
    voltage_label,
    celldiff_label,
    percentcapacity_label,
    current_label
)}

for arg in glob_path(sys.argv[1:]):
    try:
        with open_log_file(arg) as file:
            current_line=1

            for line in file:
                log=batterymon_helpers.parse_log_line(line.decode("utf-8"))

                if log[2] == "EX":
                    print(log[0]+" "+log[1]+" "+log[3]+": Exception")
                    continue

                if log[2] == "RL":
                    print(log[0]+" "+log[1]+": Reading locked")
                    continue

                if log[2] != "OK":
                    print(log[0]+" "+log[1]+" "+log[3]+": NOT OK")
                    continue

                try:
                    voltage=float(log[log_params_index[voltage_label]])
                    need_balance=" [B]" if float(log[log_params_index[celldiff_label]]) >= 0.05 else ""

                    print(log[0]+" "+log[1]+" "+log[3]+": " \
                    +   str(round(float(log[log_params_index[percentcapacity_label]]), 3))+"% " \
                    +   str(round(voltage, 3))+"V " \
                    +   str(round(float(log[log_params_index[current_label]])*voltage, 3))+"W" \
                    +   need_balance)
                except(ValueError):
                    print(log[1]+" "+log[3]+": float conversion error")
                except(IndexError):
                    print(log[1]+" "+log[3]+": index error")
                except(UnicodeDecodeError):
                    print(arg+": line "+str(current_line)+": unicode decode error")

                current_line+=1
    except(Exception) as e:
        print("[ERR] "+arg+": "+str(e))
