 #!/bin/env sh
while read line
do
  # remove trailing spaces + remove base ship + remove quotes
  echo "$line" | sed 's|^%s*||' | sed 's|%s*$||' | sed 's| ".*"$||' | sed 's| `.*`$||' | sed 's|^"\(.*\)"$|\1|' | sed 's|^`\(.*\)`$|\1|'
done
