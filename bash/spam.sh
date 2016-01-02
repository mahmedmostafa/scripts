#!/bin/bash
# Find location of spam on cPanel/exim server

grep cwd /var/log/exim_mainlog | egrep -o "cwd=[^ ]*"  | awk -F'=' '{print $2}' | sort | uniq -c
