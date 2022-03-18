#!/bin/bash

set -euo pipefail

plugin_name="Spacefarer plugin"

if [ ! -d .git ] || [ ! -f "${0##*/}" ]; then
  echo "ERROR: This script must be run from the ${plugin_name} git repository." >&2
  exit 1
fi

find "${PWD%/*}" -maxdepth 2 -type d -name data | grep -vF "${PWD##*/}" | \
  sed 's#/data$##' | \
  xargs -n1 -- ./generate-plugin-data.sh
