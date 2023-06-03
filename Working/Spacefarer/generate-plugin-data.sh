#!/bin/bash

set -euo pipefail

plugin_name="Spacefarer plugin"
data_sub_folder="${1%/}"
data_sub_folder="${data_sub_folder##*/}"

#
# Initial environment checking
#
if [ -z "${data_sub_folder:-}" ]; then
  echo 'ERROR: could not determine subfolder.  Try to use full path to directory.' >&2
  exit 1
fi
if [ ! -d "${1%/}"/data ]; then
  echo 'ERROR: first argument must be a local Endless Sky git repo or plugin directory.' >&2
  exit 1
fi
if [ ! -d .git ] || [ ! -f "${0##*/}" ]; then
  echo "ERROR: This script must be run from the ${plugin_name} git repository." >&2
  exit 1
fi

pushd "$1" &> /dev/null

#
# Automaically generate outfit constraints
#
echo 'Creating outfit constraints:'
(
  grep -rl -- '^outfit ' data || echo
) | while read data_file; do
  if [ -z "${data_file:-}" ]; then
    continue
  fi
  plugin_dest=data/"${data_sub_folder}"/"${data_file#data/}"
  # add data to named sub-directory
  mkdir -p ~1/"${plugin_dest%/*}"
  grep -ro '^outfit .*' "${data_file}" | \
  grep -vFf ~1/metadata/skip-outfits.txt | (
      while read line; do
        #if ! grep -F "${line}" ~1/"${data_file}" &> /dev/null; then
        #more IO intensive but avoids duplicates across files
        if ! grep -xrFl -- "${line}" ~1/data &> /dev/null; then
          echo "${line}"
        fi
      done
    ) | \
    tr '\n' '\0' | \
    xargs -0 -n1 -I{} -- echo -e '{}\n\t"unplunderable" 1' >> ~1/"${plugin_dest}"
  echo "    Created '${plugin_dest}'."
done

#
# Automaically generate ship constraints
#
echo 'Creating ship constraints:'
(
  grep -rl -- '^ship ' data || echo
) | while read data_file; do
  if [ -z "${data_file:-}" ]; then
    continue
  fi
  plugin_dest=data/"${data_sub_folder}"/"${data_file#data/}"
  # add data to named sub-directory
  mkdir -p ~1/"${plugin_dest%/*}"
  (
    grep -ro '^ship .*' "${data_file}" | \
    grep -vFf ~1/metadata/skip-ships.txt | (
        while read line; do
          #if ! grep -F "${line}" ~1/"${data_file}" &> /dev/null; then
          #more IO intensive but avoids duplicates across files
          if ! grep -xrFl -- "${line}" ~1/data &> /dev/null; then
            echo "${line}"
          fi
        done
      ) | \
      tr '\n' '\0' | \
      xargs -0 -n1 -I{} -- echo -e '{}\n\t"uncapturable"' >> ~1/"${plugin_dest}"
    echo "    Created '${plugin_dest}'."
  ) || rm -f ~1/"${data_file}"
done

if [ -d .git ]; then
  git rev-parse HEAD > ~1/metadata/"${data_sub_folder}"-commit
fi

#
# Copy over any custom missions
#
function custom_data_exists() {
  [ -d "metadata/${data_sub_folder}" ] && \
  [ -n "$(find "metadata/${data_sub_folder}" -maxdepth 1 -type f | head -n1)" ]
}
popd &> /dev/null
if custom_data_exists; then
  echo 'Adding custom missions for '"${data_sub_folder}"
  cp "metadata/${data_sub_folder}"/* "data/${data_sub_folder}"/
fi
