def read_voltage_log_params_index(LOG_PARAMS):
    global _read_voltage_log_params_index

    _read_voltage_log_params_index={name: LOG_PARAMS.index(name)+4 for name in (
        read_voltage_labels["voltage"],
        read_voltage_labels["celldiff"],
        read_voltage_labels["percentcapacity"],
        read_voltage_labels["current"]
    )}

def read_voltage_main(log, wrapper_function, prog):
    date=""

    if prog == "read-arch-voltage":
        date=log[0]+" "

    if log[2] == "RL":
        return wrapper_function(
            "rl", log, prog,
            date+log[1]+": Reading locked"
        )

    battery_label=read_voltage_battery_labels.get(log[3], log[3])

    if log[2] == "EX":
        return wrapper_function(
            "ex", log, prog,
            date+log[1]+" "+battery_label+": Exception"
        )

    if log[2] != "OK":
        return wrapper_function(
            "nok", log, prog,
            date+log[1]+" "+battery_label+": NOT OK"
        )

    try:
        voltage=float(log[_read_voltage_log_params_index[read_voltage_labels["voltage"]]])
        need_balance=""

        if float(log[_read_voltage_log_params_index[read_voltage_labels["celldiff"]]]) >= 0.05:
            need_balance=" [B]"

        return wrapper_function("ok", log, prog, date+log[1]+" "+battery_label+": " \
        +   str(round(float(log[_read_voltage_log_params_index[read_voltage_labels["percentcapacity"]]]), 3))+"% " \
        +   str(round(voltage, 3))+"V " \
        +   str(round(float(log[_read_voltage_log_params_index[read_voltage_labels["current"]]])*voltage, 3))+"W" \
        +   need_balance)
    except(ValueError):
        return wrapper_function(
            "ve", log, prog,
            date+log[1]+" "+battery_label+": float conversion error"
        )
    except(IndexError):
        return wrapper_function(
            "ie", log, prog,
            date+log[1]+" "+battery_label+": index error"
        )

_read_voltage_log_params_index={}
read_voltage_labels={
    "voltage": "Voltage",
    "celldiff": "CellDiff",
    "percentcapacity": "PercentCapacity",
    "current": "Current"
}
read_voltage_battery_labels={}
