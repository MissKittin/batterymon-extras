#!/usr/bin/env python3

# A wrapper for logs2ram.py
# scans directories without specifying paths
# You can link this file to /usr/local/bin/verify-arch.py

import os
import sys

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.insert(1, batterymon_extras_config.BATTERYMON_DIR)
else:
    sys.path.insert(1, "/usr/local/share/batterymon")

from batterymon_lib import batterymon_common

args=["NULL", batterymon_common.ARCH_JOURNAL_DIR]

if batterymon_common.ARCH_MNT_BACKUP is not None:
    args.append(batterymon_common.ARCH_MNT_BACKUP+"/"+os.path.relpath(
        batterymon_common.ARCH_JOURNAL_DIR,
        batterymon_common.ARCH_MNT)
    )

do_exit=False

for i in args[1:]:
    if not os.path.isdir(i):
        print(i+" is not a directory")
        do_exit=True

if do_exit:
    print("Maybe you should mount something?")
    sys.exit(2)

os.execvp(
    os.path.dirname(os.path.realpath(sys.argv[0]))+"/verify-arch.py",
    args
)

sys.exit(1)
