#!/bin/bash

_file="$1"

if [[ ! -f "${_file}" ]]; then
    printf "File %s does not exist\n" "${_file}"
    exit 1
fi

for l in $(cat "${_file}" | tr -d ' '); do
    date=$(echo "${l}" | cut -d';' -f1)
    level=$(echo "${l}" | cut -d';' -f2)
    gender=$(echo "${l}" | cut -d';' -f3)

    ./tournament-generator.py --date "${date}" --level "${level}" --gender "${gender}"

done
