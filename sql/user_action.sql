# Host: 127.0.0.1  (Version 5.7.16-log)
# Date: 2022-6-16 11:14:48
# Generator: MySQL-Front 5.7
# Internet: http://www.mysqlfront.de/
# 记录用户的搜索记录和点击城市记录


DROP TABLE IF EXISTS `user_action`;
CREATE TABLE `user_action` (
    `Username` varchar(255) NOT NULL,
    `Userid` varchar(255) NOT NULL,
    `SearchKey` varchar(255),
    `ActionTime` datetime
) ENGINE=InnoDB AUTO_INCREMENT=414 DEFAULT CHARSET=utf8;