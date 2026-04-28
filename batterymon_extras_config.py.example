# This file contains settings for Python programs
# Rename this file to batterymon_extras_config.py and edit it

BATTERYMON_DIR="/usr/local/share/batterymon" # if batterymon is installed in a different path than /usr/local/share/batterymon

# logs2xlsx-wrapper.py
XLSX_TEMPLATE="/home/pi/logs2xlsx.xlsx" # can be None
XLSX_NO_CONVERT=["Balance"] # from the LOG_PARAMS array from the lib/batterymon_common.py file, can be None

# read-voltage.py and read-arch-voltage.py
VOLTAGE_LABEL="Voltage"
CELLDIFF_LABEL="CellDiff"
PERCENTCAPACITY_LABEL="PercentCapacity"
CURRENT_LABEL="Current"
BATTERY_LABELS={
    "bt:00:11:22:33:44:55": "Battery #1",
    "bt:01:23:45:67:89:AB": "Battery #2"
}
def read_voltage_wrapper(status, full_log, prog, message):
    # a function that modifies the program output

    # the full_log argument contains the parsed log line (array) that can be analyzed
    # the prog argument (string) tells which program calls this function: it can be read-voltage or read-arch-voltage
    # the message argument is the program output string that can be modified
    # the status argument (string) takes the following values:
    #  led - archiving in progress (full_log will be None, only in prog=read-voltage)
    #  led_b - alarm (full_log will be None, only in prog=read-voltage)
    #  ok - normal reading
    #  nok - not ok
    #  rl - reading locked
    #  err - read-voltage current_out does not exist/read-arch-voltage Exception message (full_log will be None)
    #  ex - Exception
    #  ve - ValueError
    #  ie - IndexError
    #  ude - UnicodeDecodeError (full_log will be None, only in prog=read-arch-voltage)

    # if you don't use this function
    # just return the unmodified output
    return message
