i#!/bin/sh

oIFS=$IFS;

IFS=$'\n';

for i in $(vzlist -aH -octid,hostname);do

CTID=$(echo $i | awk '{print $1}');

HOSTNAME=$(echo $i| awk '{print $2}');



if [ -f /etc/vz/conf/${CTID}.mount ];then

continue;

fi

echo "Applying bind mount for $HOSTNAME"



if [ ! -d /backup/mount/$HOSTNAME ];then



mkdir -p /backup/mount/$HOSTNAME


fi



cat <<EOF > /etc/vz/conf/${CTID}.mount

#!/bin/bash

. /etc/vz/vz.conf

. \${VE_CONFFILE}

SRC=/backup/mount/$HOSTNAME

DST=/backup

if [ ! -e \${VE_ROOT}\${DST} ]; then mkdir -p 
\${VE_ROOT}\${DST}; fi

mount -n -t simfs \${SRC} \${VE_ROOT}\${DST} -o 
\${SRC}

EOF

chmod +x /etc/vz/conf/${CTID}.mount

done

IFS=$oIFS;
