# BatteryMon extras
Additional scripts for BatteryMon  
More information on how to use scripts can be found in their headers

### Software requirements
* BatteryMon v1.0
* python
* openpyxl (for `logs2xlsx.py`)

### Setup
If the main program is not in `/usr/local/share/batterymon`,  
rename `batterymon_extras_config.py.example` to `batterymon_extras_config.py`  
and edit it (do this if you want to change other settings).  
You can do the same with `batterymon_extras_config.rc.example` - it contains settings for shell scripts.  
You can link the scripts to the `/usr/local/bin` directory.  
Alternatively, you can link only the `batterymon.sh` file to `/usr/local/bin/batterymon` - this will make all programs visible under one command.  
To install the necessary packages, use pip:
```
pip install openpyxl -t .
```

### Tools
* `batterymon.sh` - a bridge that hides multiple programs under one command
* `combine-logs.py` - combine multiple logs into one
* `logs2xlsx.py` - insert archived data into a spreadsheet
* `logs2xlsx-wrapper.py` - a wrapper for `logs2ram.py` with a defined data source and xlsx template
* `press-gpio-button.py` - press the GPIO button from the terminal
* `read-voltage.py` - read the last recorded values from the log
* `verify-archive.py` - Check the integrity of archived logs
