#!/usr/bin/env python3

# BatteryMon add-on that allows you
# to quickly check the integrity of archived logs

import sys
import os

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.insert(1, batterymon_extras_config.BATTERYMON_DIR)
else:
    sys.path.insert(1, "/usr/local/share/batterymon")

from batterymon_lib import batterymon_helpers_extra

scanned_files=0
not_scanned_files=0
no_checksum_files=0
good_files=0
corrupted_files=0

if len(sys.argv) < 2:
    print("Usage: "+sys.argv[0]+" /media/batterymon/batterymon/journal [/media/batterymon-backup/batterymon/journal]")
    sys.exit(1)

for arg in sys.argv[1:]:
    if not os.path.isdir(arg):
        print("Error: "+arg+" is not a directory")
        sys.exit(1)

for arg in sys.argv[1:]:
    print("\nLocation: "+arg+"\n")

    for filename in os.listdir(arg):
        if not filename.endswith(".gz"):
            continue

        scanned_files+=1
        full_path=os.path.join(arg, filename)

        if not os.path.exists(full_path+".sha512"):
            print(" [NO-SHA] "+filename)
            no_checksum_files+=1

            continue

        try:
            with open(full_path+".sha512", "r") as f_sum:
                if batterymon_helpers_extra.sha512sum(full_path) == f_sum.read():
                    print(" [  OK  ] "+filename)
                    good_files+=1

                    continue
        except(Exception) as e:
            print(" [ FAIL ] "+filename+": "+str(e))
            not_scanned_files+=1

            continue

        print(" [ FAIL ] "+filename)
        corrupted_files+=1

if scanned_files != 0:
    print("")

print("Scanned files: "+str(scanned_files))
print("Not scanned files: "+str(not_scanned_files))
print("Good files: "+str(good_files))
print("Files without checksum: "+str(no_checksum_files))
print("Corrupted files: "+str(corrupted_files))

if corrupted_files != 0:
    sys.exit(2)

if no_checksum_files != 0:
    sys.exit(3)

if scanned_files == 0:
    sys.exit(4)
