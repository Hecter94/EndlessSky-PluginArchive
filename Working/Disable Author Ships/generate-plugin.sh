#!/bin/bash

set -eo pipefail

if [ ! -f "${0##*/}" ]; then
  echo 'ERROR: this must be run from the plugin root.' >&2
  exit 1
fi

rm -rf data
mkdir data
grep ^person ../endless-sky/data/persons.txt | \
  awk '{ print $0; printf "\tfrequency 0\n\n"}' \
  > data/remove-persons.txt
