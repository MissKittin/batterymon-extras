def read_voltage_log_params_index(LOG_PARAMS):
    global _read_voltage_log_params_index

    _read_voltage_log_params_index={name: LOG_PARAMS.index(name)+4 for name in (
        read_voltage_labels["voltage"],
        read_voltage_labels["celldiff"],
        read_voltage_labels["percentcapacity"],
        read_voltage_labels["current"]
    )}

def read_voltage_main(log, prog):
    date=""

    if prog == "read-arch-voltage":
        date=log[0]+" "

    if log[2] == "EX":
        return date+log[1]+" "+log[3]+": Exception"

    if log[2] == "RL":
        return date+log[1]+": Reading locked"

    if log[2] != "OK":
        return date+log[1]+" "+log[3]+": NOT OK"

    try:
        voltage=float(log[_read_voltage_log_params_index[read_voltage_labels["voltage"]]])
        need_balance=""

        if float(log[_read_voltage_log_params_index[read_voltage_labels["celldiff"]]]) >= 0.05:
            need_balance=" [B]"

        return date+log[1]+" "+log[3]+": " \
        +   str(round(float(log[_read_voltage_log_params_index[read_voltage_labels["percentcapacity"]]]), 3))+"% " \
        +   str(round(voltage, 3))+"V " \
        +   str(round(float(log[_read_voltage_log_params_index[read_voltage_labels["current"]]])*voltage, 3))+"W" \
        +   need_balance
    except(ValueError):
        return date+log[1]+" "+log[3]+": float conversion error"
    except(IndexError):
        return date+log[1]+" "+log[3]+": index error"

_read_voltage_log_params_index={}
read_voltage_labels={
    "voltage": "Voltage",
    "celldiff": "CellDiff",
    "percentcapacity": "PercentCapacity",
    "current": "Current"
}
