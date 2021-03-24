#Import required
import subprocess
import json
import os
import mysql.connector
import time


def getSqlConnection():
    sql_username = os.environ['MYSQL_USER']
    sql_password = os.environ['MYSQL_PASSWORD']
    sql_host = os.environ['SQLHOST']
    sql_db = os.environ['DATABASE']

    mysql_con = mysql.connector.connect(
        host=sql_host,
        user=sql_username,
        password=sql_password,
        database=sql_db
    )

    mysql_con.autocommit = True
    return mysql_con


def createDbTables():
    sql_username = "root"
    sql_password = os.environ['MYSQL_ROOT_PASSWORD']
    sql_host = os.environ['SQLHOST']
    sql_db = os.environ['DATABASE']

    mysqldb = mysql.connector.connect(
        host=sql_host,
        user=sql_username,
        password=sql_password
    )

    # Setup SQL db and tables if not exsistent
    mysqldb.connect()
    mysql_com = mysqldb.cursor()
    for line in open("/docker-entrypoint-initdb.d/initdb.sql"):
        mysql_com.execute(line)

    return


def sqlCommit(data):

    connection = getSqlConnection()
    mysql_com = connection.cursor()
    mysql_com.execute(data)
    return


def main():
    print()
    print(os.environ['MYSQL_ROOT_PASSWORD'])
    createDbTables()

    while True:

        result = subprocess.run('/usr/bin/speedtest -f json',shell=True, stdout=subprocess.PIPE, text=True)

        print(result)
        result = json.JSONDecoder().decode(result.stdout)

        if result['type'] == 'result':
            sqlCommit(result)
        else:
            print(result)

        time.sleep(os.environ['INTERVAL'])
    return


if __name__ == '__main__':
    main()
