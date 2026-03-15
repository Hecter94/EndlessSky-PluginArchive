#!/bin/bash

set -eo pipefail

if [ ! -f "${0##*/}" ]; then
  echo 'ERROR: this must be run from the plugin root.' >&2
  exit 1
fi

persons_file="../endless-sky/data/persons.txt"
if [ ! -s "${persons_file}" ]; then
  echo 'Please enter the full path to Endless Sky on your system. Do not use a relative path. If you are on macOS, it may contain spaces. Example entry: /Users/samrocketman/Library/Application Support/ESLauncher2/instances/Main/Endless Sky.app/Contents/Resources'
  read -p 'Enter path: ' persons_dir
  if [ -s "${persons_dir}/data/persons.txt" ]; then
    persons_file="${persons_dir}/data/persons.txt"
  else
    echo 'ERROR: could not find data/persons.txt in your entered path.' >&2
    exit 1
  fi
fi

rm -rf data
mkdir data
grep ^person "${persons_file}" | \
  awk '{ print $0; printf "\tfrequency 0\n\n"}' \
  > data/remove-persons.txt
