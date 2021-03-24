#!/bin/bash

DATABASE= echo $DATABASE | sed "s/'//g" | sed 's/"//g' 
echo "EXPORT $DATABASE"

MYSQL_USER = echo $MYSQL_USER | sed "s/'//g" | sed 's/"//g'
echo "EXPORT $MYSQL_USER"

MYSQL_PASSWORD = echo $MYSQL_PASSWORD | sed "s/'//g" | sed 's/"//g' 
echo "EXPORT $MYSQL_PASSWORD"

SQLHOST= sed "s/'//g" <<< sed 's/"//g'  <<< $SQLHOST
echo "EXPORT $SQLHOST"

sed -i -e "s/speedtest/$DATABASE/g" /docker-entrypoint-initdb.d/initdb.sql
sed -i -e "s/SpeedtestUser/$MYSQL_USER/g" /docker-entrypoint-initdb.d/initdb.sql
sed -i -e "s/Sp33dt3stUs3rPW/$MYSQL_PASSWORD/g" /docker-entrypoint-initdb.d/initdb.sql

cat /docker-entrypoint-initdb.d/initdb.sql
python3 /usr/local/bin/main.py
