#!/usr/bin/env python3

# BatteryMon add-on that stops reading data from BMS
# Use with caution!

if os.path.exists(os.path.dirname(os.path.realpath(sys.argv[0]))+"/batterymon_extras_config.py"):
    import batterymon_extras_config
    sys.path.insert(1, batterymon_extras_config.BATTERYMON_DIR)
else:
    sys.path.insert(1, "/usr/local/share/batterymon")

from lib import batterymon_common

if len(sys.argv) < 2:
    print(sys.argv[0]+" lock|unlock")
    sys.exit(1)

if sys.argv[1] == "lock":
    if input("Are you sure (y/[N])? ").strip().lower() != "y":
        sys.exit(2)

    if os.path.exists(batterymon_common.READ_LOCK_FILE):
        print("Reading is already blocked")
        sys.exit(3)
    else:
        open(batterymon_common.READ_LOCK_FILE, "w").close()
        os.chmod(batterymon_common.READ_LOCK_FILE, 0o666)

if sys.argv[1] == "unlock":
    if os.path.exists(batterymon_common.READ_LOCK_FILE):
        os.remove(batterymon_common.READ_LOCK_FILE)
    else:
        print("Reading is not blocked")
        sys.exit(4)
