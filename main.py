# Import required
import subprocess
import json
import os
import mysql.connector
import time
import datetime as dt


def setEnvVariables():
    os.environ['MYSQL_ROOT_PASSWORD'] = 'Sp33dt3stR00tPW'
    os.environ['MYSQL_USER'] = 'SpeedtestUser'
    os.environ['MYSQL_PASSWORD'] = 'Sp33dt3stUs3rPW'
    os.environ['DATABASE'] = 'Speedtest'
    os.environ['SQLHOST'] = 'dockerdev.boerhuis.ca'
    return


'''
def processData(data):
    result = {}
    result['TimeStamp'] = data['timestamp'].replace("T", " ").replace("Z", "")
    result['PingJitter'] = float("{:.3f}".format(data['ping']['jitter']))
    result['PingLatency'] = float("{:.5f}".format(data['ping']['latency']))
    result['DownloadBandwith'] = data['download']['bandwidth']
    result['DownloadBytes'] = data['download']['bytes']
    result['DownloadElapsed'] = data['download']['elapsed']
    result['UploadBandwith'] = data['upload']['bandwidth']
    result['UploadBytes'] = data['upload']['bytes']
    result['UploadElapsed'] = data['upload']['elapsed']
    try:
        result['PacketLoss'] = data['packetLoss']
    except:
        result['PacketLoss'] = 0
    result['ISP'] = data['isp']
    result['InterfaceExternalIP'] = data['interface']['externalIp']
    result['ServerID'] = data['server']['id']
    result['ServerName'] = data['server']['name']
    result['ServerIP'] = data['server']['ip']
    result = json.dumps(result)

    return result
'''


def processData(data):
    result = [data['timestamp'].replace("T", " ").replace("Z", ""), float("{:.3f}".format(data['ping']['jitter'])),
              float("{:.5f}".format(data['ping']['latency'])), data['download']['bandwidth'], data['download']['bytes'],
              data['download']['elapsed'], data['upload']['bandwidth'], data['upload']['bytes'],
              data['upload']['elapsed'], data['isp'], data['interface']['externalIp'], data['server']['id'],
              data['server']['name'], data['server']['ip']]
    try:
        result.append(data['packetLoss'])
    except:
        result.append(0)

    return result


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

    mysqldb = mysql.connector.connect(
        host=sql_host,
        user=sql_username,
        password=sql_password
    )

    # Setup SQL db and tables if not exsistent
    mysqldb.connect()
    mysql_com = mysqldb.cursor()
    try:  # default file
        for line in open("/docker-entrypoint-initdb.d/initdb.sql"):
            mysql_com.execute(line)
    except:  # default settings if file not found
        mysql_com.execute("CREATE DATABASE IF NOT EXISTS `Speedtest`;")
        mysql_com.execute("USE `Speedtest`;")
        mysql_com.execute("CREATE TABLE IF NOT EXISTS `results` \
                         (id int NOT NULL AUTO_INCREMENT, \
                         TimeStamp timestamp DEFAULT NULL, \
                         PingJitter decimal(3,3) DEFAULT NULL, \
                         PingLatency decimal(5,5) DEFAULT NULL, \
                         DownloadBandwith int DEFAULT NULL, \
                         DownloadBytes int DEFAULT NULL, \
                         DownloadElapsed smallint DEFAULT NULL, \
                         UploadBandwith int DEFAULT NULL, \
                         UploadBytes int DEFAULT NULL, \
                         UploadElapsed smallint DEFAULT NULL, \
                         PacketLoss mediumint DEFAULT NULL, \
                         ISP varchar(45) DEFAULT NULL, \
                         InterfaceExternalIP varchar(15) DEFAULT NULL, \
                         ServerID smallint DEFAULT NULL, \
                         ServerName varchar(45) DEFAULT NULL, \
                         ServerIP varchar(15) DEFAULT NULL, \
                         DateTime datetime DEFAULT CURRENT_TIMESTAMP, \
                         PRIMARY KEY (`id`), UNIQUE KEY `index_UNIQUE` (`id`));")

        mysql_com.execute("DROP EVENT IF EXISTS `AutoDeleteOldData`;")
        mysql_com.execute("CREATE EVENT `AutoDeleteOldData` ON SCHEDULE EVERY 1 DAY STARTS \
                          '2021-03-25 00:00:00.000000' ON COMPLETION PRESERVE ENABLE \
                          DO DELETE FROM Speedtest.results where DateTime < DATE_SUB(NOW, INTERVAL 45 DAY);")
        mysql_com.execute("CREATE USER IF NOT EXISTS `SpeedtestUser`@`%`;")
        mysql_com.execute(
            "ALTER USER `SpeedtestUser`@`%` IDENTIFIED WITH mysql_native_password BY \"Sp33dt3stUs3rPW\";")
        mysql_com.execute("GRANT ALL ON Speedtest.* TO `SpeedtestUser`@`%`;")

        os.environ['MYSQL_ROOT_PASSWORD'] = 'Sp33dt3stR00tPW'
        os.environ['MYSQL_USER'] = 'SpeedtestUser'
        os.environ['MYSQL_PASSWORD'] = 'Sp33dt3stUs3rPW'
        os.environ['DATABASE'] = 'Speedtest'
    return


def sqlCommit(data):
    data = processData(data)
    print(data)
    # add_data = """INSERT INTO `results`(`TimeStamp`,`PingJitter`, `PingLatency`, `DownloadBandwith`, \
    #            `DownloadBytes`, `DownloadElapsed`, `UploadBandwith`, `UploadBytes`, `UploadElapsed`, \
    #            `ISP`, `InterfaceExternalIP`, `ServerID`, `ServerName`, `ServerIP`,`PacketLoss`) \
    #            VALUES ('{TimeStamp}','{PingJitter}','{PingLatency}','{DownloadBandwith}',\
    #            '{DownloadBytes}','{DownloadElapsed}','{UploadBandwith}','{UploadBytes}','{UploadElapsed}',\
    #            '{PacketLoss}','{ISP}','{InterfaceExternalIP}','{ServerID}','{ServerName}','{ServerIP})')""".format(data)
    add_data = """INSERT INTO `results`(`TimeStamp`,`PingJitter`, `PingLatency`, `DownloadBandwith`, \
                `DownloadBytes`, `DownloadElapsed`, `UploadBandwith`, `UploadBytes`, `UploadElapsed`, \
                `ISP`, `InterfaceExternalIP`, `ServerID`, `ServerName`, `ServerIP`,`PacketLoss`) \
                VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}')""".format(data)
    print(add_data)
    connection = getSqlConnection()
    mysql_com = connection.cursor(prepared=True)
    mysql_com.execute(add_data)
    mysql_com.commit()

    return


def main():
    setEnvVariables()
    print()
    print(os.environ['MYSQL_ROOT_PASSWORD'])
    createDbTables()

    while True:

        response = subprocess.run('speedtest -f json', shell=True, stdout=subprocess.PIPE, text=True)
        response = response.stdout
        print(response)
        response = json.JSONDecoder().decode(response)

        if response['type'] == "result":
            sqlCommit(response)
        else:
            print(response)

        time.sleep(os.environ['INTERVAL'])
    mysql_com.close()
    return


if __name__ == '__main__':
    main()
