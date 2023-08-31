#!/bin/env sh
ls -d -1 ../../plugins/*/data/ | sed 's|^''\(.*\)''$|\1|' | sed 's|^../../plugins/||' | sed 's|/data/$||' | sed '/^-/d' | sed '/ruin-the-fun/d' | sed '/lissas/d'
