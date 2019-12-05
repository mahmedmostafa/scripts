#!/bin/sh

docker run -tdi --name blog -v /usr/src/pelican_docker/blog:/srv/blog:rw -v /usr/src/pelican_docker/blog/output/:/usr/share/nginx/html:ro  -p 0.0.0.0:80:80/tcp pelicanv6

