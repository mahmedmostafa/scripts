#!/bin/bash
# Find location of spam on cPanel/exim server

egrep -o "cwd=[^ ]*" /var/log/exim_mainlog  | awk -F'=' '{print $2}' | sort | uniq -c
