CREATE DATABASE IF NOT EXISTS `speedtest`;
USE `speedtest`;
CREATE TABLE IF NOT EXISTS `results` (id int NOT NULL DEFAULT 1, TimeStamp timestamp NULL DEFAULT NULL, PingJitter decimal(3,3) DEFAULT NULL, PingLatency decimal(5,5) DEFAULT NULL, DownloadBandwith int DEFAULT NULL, DownloadBytes int DEFAULT NULL, DownloadElapsed smallint DEFAULT NULL, UploadBandwith int DEFAULT NULL, UploadBytes int DEFAULT NULL, UploadElapsted smallint DEFAULT NULL, PacketLoss mediumint DEFAULT NULL, ISP varchar(45) DEFAULT NULL, InterfaceExternalIP varchar(15) DEFAULT NULL, ServerID smallint DEFAULT NULL, ServerName varchar(45) DEFAULT NULL, ServerIP varchar(15) DEFAULT NULL, DateTime datetime DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`), UNIQUE KEY `index_UNIQUE` (`id`));
DROP EVENT IF EXISTS `AutoDeleteOldData`; 
CREATE EVENT `AutoDeleteOldData` ON SCHEDULE EVERY 1 DAY STARTS '2021-03-25 03:00:00.000000' ON COMPLETION PRESERVE ENABLE DO DELETE FROM Speedtest.results where DateTime < DATE_SUB(NOW, INTERVAL 45 DAY)
CREATE USER IF NOT EXISTS `SpeedtestUser`@`%`;
ALTER USER `SpeedtestUser`@`%` IDENTIFIED WITH mysql_native_password BY "Sp33dt3stUs3rPW";
GRANT ALL ON speedtest.* TO `SpeedtestUser`@`%`;