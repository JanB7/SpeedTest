#!/bin/bash

/usr/local/bin/docker-entrypoint.sh mysqld &
python3 /usr/local/bin/main.py