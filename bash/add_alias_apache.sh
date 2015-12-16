#!/bin/bash
 if [ "$#" -ne 1 ];then
        echo "Usage : $0 username"
        exit
fi
username=$1
echo "Adding configuration for $username"
cat <<EOF >/usr/local/apache/conf/userdata/std/2_4/demomhgo/demo.mhgoz.com/$username.conf
Alias /$username /home/$username/public_html
<Location /$username>
    <IfModule mod_suphp.c>
        suPHP_UserGroup $username $username
    </IfModule>
</Location>
EOF

/scripts/verify_vhost_includes

if [ $? -eq 0 ];then
        echo "Added an alias"
        echo "Restarting apache"
        service httpd restart
        echo "Content can be accessed now via http://demo.mhgoz.com/$username"
else
        echo "Something went wrong , please check vhost configuration"
fi
