#!/bin/bash

DATABASE= sed "s/'//g" <<< sed 's/"//g'  <<< $DATABASE
EXPORT $DATABASE

MYSQL_USER = sed "s/'//g" <<< sed 's/"//g'  <<< $MYSQL_USER
EXPORT $MYSQL_USER

MYSQL_PASSWORD = sed "s/'//g" <<< sed 's/"//g'  <<< $MYSQL_PASSWORD
EXPORT MYSQL_PASSWORD

SQLHOST= sed "s/'//g" <<< sed 's/"//g'  <<< $SQLHOST
EXPORT $SQLHOST

sed -i -e "s/speedtest/$DATABASE/g" /docker-entrypoint-initdb.d/initdb.sql
sed -i -e "s/SpeedtestUser/$MYSQL_USER/g" /docker-entrypoint-initdb.d/initdb.sql
sed -i -e "s/Sp33dt3stUs3rPW/$MYSQL_PASSWORD/g" /docker-entrypoint-initdb.d/initdb.sql

cat /docker-entrypoint-initdb.d/initdb.sql
python3 /usr/local/bin/main.py