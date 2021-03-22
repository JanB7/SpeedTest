#Import required
import subprocess
import json
import os
import mysql.connector
import time


def getSqlConnection():
    sql_username = os.environ['SQLUSER']
    sql_password = os.environ['SQLPASS']
    sql_host = os.environ['SQLHOST']
    sql_db = os.environ['DATABASE']

    mysql_con = mysql.connector.connect(
        host=sql_host,
        user=sql_username,
        password=sql_password,
        database=sql_db
    )

    return mysql_con


def createDbTables():
    sql_username = os.environ['SQLUSER']
    sql_password = os.environ['SQLPASS']
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

    exits = False
    databases = mysql_com.execute("SHOW DATABASES")
    for database in databases:
        if database == sql_db:
            exits = True

    if not exits:
        mysql_com.execute("CREATE DATABASE %s", sql_db)
    tables = mysql_com.execute("SHOW TABLES")

    exits = False
    for table in tables:
        if table == 'results':
            exits = True
    if not exits:
        mysql_com.execute("CREATE TABLE results")

    return


def sqlCommit(data):
    connection = getSqlConnection()
    connection.connect()

    mysql_com = connection.cursor()

    return


def main():
    print(os.environ['SQLPASS'])
    createDbTables()

    while True:

        result = subprocess.run('speedtest -f json -u kbps', stdout=subprocess.PIPE, text=True)
        result = json.JSONDecoder().decode(result.stdout)

        if result['type'] == 'result':
            sqlCommit(result)
        else:
            print(result)

        time.sleep(os.environ['INTERVAL'])
    return


if __name__ == '__main__':
    main()
