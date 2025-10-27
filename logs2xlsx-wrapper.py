#!/usr/bin/env python3

# A wrapper for logs2ram.py
# with a defined data source and xlsx template
# You can link this file to /usr/local/bin/logs2xlsx.py

import os
import sys

xlsx_template=None
no_convert=None
no_convert_indexes=[]

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.append(batterymon_extras_config.BATTERYMON_DIR)

    xlsx_template=batterymon_extras_config.XLSX_TEMPLATE
    no_convert=batterymon_extras_config.XLSX_NO_CONVERT
else:
    sys.path.append("/usr/local/share/batterymon")

from lib import batterymon_common

if len(sys.argv) > 2 and sys.argv[1] == "--sheet-name":
    os.execvp(
        os.path.dirname(os.path.realpath(sys.argv[0]))+"/logs2xlsx.py",
        sys.argv
    )
    sys.exit(1)

args=["NULL", batterymon_common.ARCH_MNT]

if xlsx_template is not None:
    args.append(xlsx_template)

if no_convert is not None:
    for index, element in enumerate(batterymon_common.LOG_PARAMS):
        if element in no_convert:
            no_convert_indexes.append(str(index))

    if no_convert_indexes:
        args.append("--no-convert="+",".join(no_convert_indexes))

os.execvp(
    os.path.dirname(os.path.realpath(sys.argv[0]))+"/logs2xlsx.py",
    args+sys.argv[1:]
)

sys.exit(1)
