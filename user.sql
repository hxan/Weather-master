# Host: 127.0.0.1  (Version 5.7.16-log)
# Date: 2022-6-16 13:08:48
# Generator: MySQL-Front 5.7
# Internet: http://www.mysqlfront.de/
# 用户数据库
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `Username` varchar(255) NOT NULL,
    `Userid` varchar(255) NOT NULL,
    `Password` varchar(255),
    `RegisterTime` datetime,
    `Address` varchar(255)
) ENGINE=InnoDB AUTO_INCREMENT=414 DEFAULT CHARSET=utf8;