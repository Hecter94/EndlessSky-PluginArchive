#!/bin/bash
# Created by Sam Gleske
# Fri Jun 24 19:14:08 EDT 2022
# DEVELOPMENT ENVIRONMENT
#     Pop!_OS 18.04 LTS
#     Linux 5.4.0-113-generic x86_64
#     GNU bash, version 4.4.20(1)-release (x86_64-pc-linux-gnu)
#     ffmpeg version 3.4.8-0ubuntu0.2 Copyright (c) 2000-2020 the FFmpeg developers
#     GNU Awk 4.1.4, API: 1.1 (GNU MPFR 4.0.1, GNU MP 6.1.2)
#     head (GNU coreutils) 8.28
#     wc (GNU coreutils) 8.28
#     xargs (GNU findutils) 4.7.0-git
#     yes (GNU coreutils) 8.28

# DESCRIPTION
#     Print the loudnorm for all input files.

# Example usage
#     loudnorm.sh *.wav *.mp3

# Single file; you can get the loudnorm of a single file the following way.
#     ffmpeg -i example.wav -filter:a ebur128 -map 0:a -f null -

FIRST_COLUMN="$(for x in "$@"; do echo -n "$x" | wc -c;done | sort -nr | head -n1)"
SECOND_COLUMN=13

function dashes() {
  yes - | head -n"$1" | xargs | sed 's/ //g'
}

function soundlevel() {
  echo -n '| '
  printf "%*s" "${FIRST_COLUMN}" "${1}"
  echo -n ' | '
  ffmpeg -i "${1}" -filter:a ebur128 -map 0:a -f null - 2>&1 | \
    awk '$1 == "I:" { print $2 }' | \
    xargs -n1 -I{} -- /bin/bash -c "printf '%*s\\n' '${SECOND_COLUMN}' '{}'" | \
    sed 's/$/ |/'
}

# first row
echo -n '| '
printf "%*s" "$FIRST_COLUMN" File
echo ' | Loudnorm (dB) |'

# second row
echo "| $(dashes "${FIRST_COLUMN}") | $(dashes "$(( SECOND_COLUMN - 1 ))"): |"

# following rows
for x in "$@"; do soundlevel "$x";done
