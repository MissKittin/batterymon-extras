def read_voltage_main(log, wrapper_function, prog):
    date=""

    if prog == "read-arch-voltage":
        date=log["_bm_date"]+" "

    if log["_bm_status"] == "RL":
        return wrapper_function(
            "rl", log, prog,
            date+log["_bm_time"]+": Reading locked"
        )

    battery_label=read_voltage_battery_labels.get(log["_bm_device"], log["_bm_device"])

    if log["_bm_status"] == "EX":
        return wrapper_function(
            "ex", log, prog,
            date+log["_bm_time"]+" "+battery_label+": Exception"
        )

    if log["_bm_status"] != "OK":
        return wrapper_function(
            "nok", log, prog,
            date+log["_bm_time"]+" "+battery_label+": NOT OK"
        )

    try:
        voltage=float(log[read_voltage_labels["voltage"]])
        need_balance=""

        if float(log[read_voltage_labels["celldiff"]]) >= 0.05:
            need_balance=" [B]"

        return wrapper_function("ok", log, prog, date+log["_bm_time"]+" "+battery_label+": " \
        +   str(round(float(log[read_voltage_labels["percentcapacity"]]), 3))+"% " \
        +   str(round(voltage, 3))+"V " \
        +   str(round(float(log[read_voltage_labels["current"]])*voltage, 3))+"W" \
        +   need_balance)
    except(ValueError):
        return wrapper_function(
            "ve", log, prog,
            date+log["_bm_time"]+" "+battery_label+": float conversion error"
        )
    except(IndexError):
        return wrapper_function(
            "ie", log, prog,
            date+log["_bm_time"]+" "+battery_label+": index error"
        )

read_voltage_labels={
    "voltage": "Voltage",
    "celldiff": "CellDiff",
    "percentcapacity": "PercentCapacity",
    "current": "Current"
}
read_voltage_battery_labels={}
