#!/bin/sh

# A bridge that hides multiple programs under one command
# Just link this file to /usr/local/bin/batterymon
#
# Usage:
#  batterymon.sh program-without-py arg_a arg_b arg_n
# eg:
#  batterymon.sh logs2xlsx /path/to/arch-journal ./template.xlsx > ./output.xlsx

batterymon_extras="$(readlink -f "${0}")"
batterymon_extras="${batterymon_extras%/*}"
program="${1}"

[ ! "${program}" = '' ] && shift

USE_LOGS2XLSX_WRAPPER='false'

[ -e "${batterymon_extras}/batterymon_extras_config.rc" ] && . "${batterymon_extras}/batterymon_extras_config.rc"

if [ ! -e "${batterymon_extras}/${program}.py" ] || [ "${program}" = 'batterymon_extras_config' ]; then
	[ ! "${program}" = '' ] && echo "${program} is unknown"
	[ ! "${program}" = '' ] && echo ''
	echo 'Available programs:'

	for i in ${batterymon_extras}/*; do
		[ "${i}" = "${batterymon_extras}/*" ] && echo " failed to list programs" && break
		i="${i##*/}"

		[ "${i}" = 'batterymon_extras_config.py' ] && continue
		[ "${i}" = 'logs2xlsx-wrapper.py' ] && "${USE_LOGS2XLSX_WRAPPER}" && continue
		[ "${i##*.}" = 'py' ] && echo " ${i%.*}"
	done

	exit 1
fi

[ "${program}" = "logs2xlsx" ] && "${USE_LOGS2XLSX_WRAPPER}" && \
	exec "${batterymon_extras}/logs2xlsx-wrapper.py" $@

exec "${batterymon_extras}/${program}.py" $@
