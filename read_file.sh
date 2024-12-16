#!/bin/bash

# Wrapper script that handles cell copy from Google doc to a text file
# and transforms the text to be able to feed it into image generator

_file="$1"

if [[ ! -f "${_file}" ]]; then
    printf "File %s does not exist\n" "${_file}"
    exit 1
fi

for l in $(cat "${_file}" | tr '\t' ';' | tr ',' ';' | tr -d ' '); do
    date=$(echo "${l}" | cut -d';' -f1)
    level=$(echo "${l}" | cut -d';' -f3 | grep -Eo '[[:digit:]]')
    gender=$(echo "${l}" | cut -d';' -f4 | tr '[[:upper:]]' '[[:lower:]]')

    ./tournament-generator.py --date "${date}" --level "${level}" --gender "${gender}"

done
