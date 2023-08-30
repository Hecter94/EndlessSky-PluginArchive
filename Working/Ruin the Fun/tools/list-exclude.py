#!/bin/env python3
import os
import sys

l1 = sys.stdin.read().splitlines()
#l1 = [l.strip('\n\r') for l in temp]

l2 = []
with open(sys.argv[1]) as f:
	l2 = list(f.read().splitlines())

l3 = [x for x in l1 if x not in l2]

for l in l3:
	print(l)
