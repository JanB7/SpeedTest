CREATE DATABASE IF NOT EXISTS `speedtest` DEFAULT CHARACTER SET utf8mb4;
USE speedtest;
CREATE TABLE  IF NOT EXISTS  `results` (
  `index` int NOT NULL DEFAULT '1',
  `TimeStamp` timestamp NULL DEFAULT NULL,
  `Ping.Jitter` decimal(3,3) DEFAULT NULL,
  `Ping.Latency` decimal(5,5) DEFAULT NULL,
  `Download.Bandwith` int DEFAULT NULL,
  `Download.Bytes` int DEFAULT NULL,
  `Download.Elapsed` smallint DEFAULT NULL,
  `Upload.Bandwith` int DEFAULT NULL,
  `Upload.Bytes` int DEFAULT NULL,
  `Upload.Elapsted` smallint DEFAULT NULL,
  `PacketLoss` mediumint DEFAULT NULL,
  `ISP` varchar(45) DEFAULT NULL,
  `Interface.ExternalIP` varchar(15) DEFAULT NULL,
  `Server.ID` smallint DEFAULT NULL,
  `Server.Name` varchar(45) DEFAULT NULL,
  `Server.IP` varchar(15) DEFAULT NULL,
  `DateTime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`index`),
  UNIQUE KEY `index_UNIQUE` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE EVENT AutoDeleteOldData 
ON SCHEDULE AT CURRENT_TIMESTAMP + iNTERVAL 1 DAY
ON COMPLETION PRESERVE
DO
DELETE FROM speedtest.results where DateTime < DATE_SUB(NOW, INTERVAL 45 DAY);