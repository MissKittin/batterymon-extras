# BatteryMon extras
Additional scripts for BatteryMon  
More information on how to use scripts can be found in their headers

### Software requirements
* BatteryMon v1.0
* python
* openpyxl (for `logs2xlsx.py`)

### Setup
If the main program is not in `/usr/local/share/batterymon`,  
rename `batterymon_extras_config_example.py` to `batterymon_extras_config.py`  
and edit it (do this if you want to change other settings).  
You can do the same with `batterymon_extras_config_example.rc` - it contains settings for shell scripts.  
Instead of copying and editing the mentioned files, you can patch them, entering only the options you want to change: create the files `batterymon_extras_config.py` and `batterymon_extras_config.rc` and enter the settings like this:  
for `batterymon_extras_config.py`:
```
# import sample configuration
from batterymon_extras_config_example import *

# enter your own settings
XLSX_TEMPLATE="/home/username/logs2xlsx.xlsx"
VOLTAGE_LABEL="Volts"

# overwrite function
def read_voltage_wrapper(status, full_log, prog, message):
    # do something with message
	return message
```
for `batterymon_extras_config.rc`:
```
# import sample configuration
. "${batterymon_extras}/batterymon_extras_config_example.rc"

# enter your own settings
USE_LOGS2XLSX_WRAPPER='true'
```
You can link the `.py` scripts to the `/usr/local/bin` directory.  
Alternatively, you can link only the `batterymon.sh` file to `/usr/local/bin/batterymon` - this will make all programs visible under one command. Run:
```
ln -s /usr/local/share/batterymon/batterymon.sh /usr/local/bin/batterymon
```
To install the necessary packages, use pip:
```
cd /usr/local/share/batterymon
pip install openpyxl -t .
```

### Tools
* `batterymon.sh` - a bridge that hides multiple programs under one command
* `bms-read-lock.py` - stop reading data from BMS (use with caution!)
* `combine-arch-logs.py` - combine multiple logs into one
* `logs2xlsx.py` - insert archived data into a spreadsheet
* `logs2xlsx-wrapper.py` - a wrapper for `logs2xlsx.py` with a defined data source and xlsx template
* `press-button.py` - press the GPIO button from the terminal
* `read-arch-voltage.py` - get data from archived logs in a simple form
* `read-voltage.py` - read the last recorded values from the log
* `verify-arch.py` - check the integrity of archived logs
* `verify-arch-wrapper.py` - a wrapper for `verify-arch.py` which automatically recognizes log directories

### Bash completion
If you only linked the `batterymon.sh` script to `/usr/local/bin/batterymon`, you can add command autocompletion. Execute:
```
ln -s /usr/local/share/batterymon-extras/batterymon.completion /etc/bash_completion.d/batterymon
```
