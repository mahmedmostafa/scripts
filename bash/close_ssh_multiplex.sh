#!/bin/sh
for i in $(ls ~/.ssh/tmp);do
        resource=(${i//_/ })
        eval $(echo "ssh -O exit -p ${resource[1]} ${resource[2]}@${resource[0]}")
done
