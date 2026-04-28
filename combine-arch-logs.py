#!/usr/bin/env python3

# BatteryMon tool that allows you to
# combine multiple logs into one

import os
import gzip
import sys

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.insert(1, batterymon_extras_config.BATTERYMON_DIR)
else:
    sys.path.insert(1, "/usr/local/share/batterymon")

from batterymon_lib import batterymon_helpers

if len(sys.argv) != 3:
    print("Usage: "+sys.argv[0]+" /media/batterymon/batterymon/journal /media/batterymon/$(date '+%Y-%m-%d_%H-%M-%S').txt.gz")
    sys.exit(1)

if not os.path.isdir(sys.argv[1]):
    print(sys.argv[1]+" does not exist")
    sys.exit(1)

if os.path.exists(sys.argv[2]):
    print(sys.argv[2]+" already exists")
    sys.exit(1)

with gzip.open(sys.argv[2], "wb", compresslevel=9) as output_file:
    for fname in sorted(f for f in os.listdir(sys.argv[1]) if f.endswith(".gz")):
        print(fname)

        with gzip.open(os.path.join(sys.argv[1], fname), "rb") as input_file:
            output_file.write(input_file.read())

print("Calculating checksum...")
with open(sys.argv[2]+".sha512", "w") as output_file_sum:
    output_file_sum.write(batterymon_helpers.sha512sum(sys.argv[2]))
