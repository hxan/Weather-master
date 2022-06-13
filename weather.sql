# Host: 127.0.0.1  (Version 5.7.16-log)
# Date: 2021-10-28 16:24:48
# Generator: MySQL-Front 5.4  (Build 3.52)
# Internet: http://www.mysqlfront.de/

/*!40101 SET NAMES utf8 */;

#
# Structure for table "weather"
#

DROP TABLE IF EXISTS `weather`;
CREATE TABLE `weather` (
  `Id` int(12) NOT NULL AUTO_INCREMENT,
  `Station_Id_C` int(6) NOT NULL,
  `city` VARCHAR(255),
  `Day` int(3) DEFAULT NULL,
  `Hour` int(3) DEFAULT NULL,
  `PRS` float(6) DEFAULT NULL,
  `PRS_Max` float(6) DEFAULT NULL,
  `PRS_Min` float(6) DEFAULT NULL,
  `TEM` float(6) DEFAULT NULL,
  `TEM_Max` float(6) DEFAULT NULL,
  `TEM_Min` float(6) DEFAULT NULL,
  `RHU` int(4) DEFAULT NULL,
  `VAP` float(6) DEFAULT NULL,
  `PRE_1h` float(6) DEFAULT NULL,
  `WIN_S_Max` float(6) DEFAULT NULL,
  `WIN_D_S_Max` int(6) DEFAULT NULL,
  `WIN_D_INST_Max` int(6) DEFAULT NULL,
  `WIN_S_Inst_Max` float(6) DEFAULT NULL,
  `RHU_Min` int(3) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=414 DEFAULT CHARSET=utf8;

