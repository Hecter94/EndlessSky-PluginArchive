#!/bin/env sh
while read line
do
  # remove trailing spaces + remove quotes
  echo "$line" | sed 's|^%s*||' | sed 's|%s*$||' | sed 's|^"\(.*\)"$|\1|' | sed 's|^`\(.*\)`$|\1|'
done
