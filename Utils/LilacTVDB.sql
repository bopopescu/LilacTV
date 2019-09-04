-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: LilacTVDB
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `answers`
--

DROP TABLE IF EXISTS `answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answers` (
  `replier_id` tinyint(4) unsigned NOT NULL DEFAULT '1',
  `question_id` tinyint(4) unsigned NOT NULL DEFAULT '1',
  `content` mediumtext,
  `create_date` datetime DEFAULT NULL,
  `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `replier_id` (`replier_id`),
  KEY `question_id` (`question_id`),
  KEY `id` (`id`),
  CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`replier_id`) REFERENCES `users` (`id`),
  CONSTRAINT `answers_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answers`
--

LOCK TABLES `answers` WRITE;
/*!40000 ALTER TABLE `answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hibernate_sequence`
--

DROP TABLE IF EXISTS `hibernate_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hibernate_sequence` (
  `next_val` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hibernate_sequence`
--

LOCK TABLES `hibernate_sequence` WRITE;
/*!40000 ALTER TABLE `hibernate_sequence` DISABLE KEYS */;
INSERT INTO `hibernate_sequence` VALUES (27);
/*!40000 ALTER TABLE `hibernate_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `macaddeth0` varchar(30) DEFAULT NULL,
  `macaddwlan` varchar(30) DEFAULT NULL,
  `ipadd` varchar(30) DEFAULT NULL,
  `online` tinyint(1) NOT NULL DEFAULT '0',
  `tvheadend` tinyint(1) NOT NULL DEFAULT '0',
  `seqindex` tinyint(4) DEFAULT NULL,
  `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
  `owner_id` tinyint(4) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `macaddeth0_2` (`macaddeth0`),
  KEY `macaddeth0` (`macaddeth0`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES ('00:1a:79:ff:00:da','00:e0:4c:81:89:56','194.193.60.92',1,0,NULL,1,2),('c4:4e:ac:11:55:11','54:c9:df:77:45:8d','194.193.60.92',1,0,NULL,2,3),('c4:4e:ac:11:9f:50','ec:3d:fd:01:17:b2','138.130.67.117',0,0,NULL,3,1),('c4:2f:ac:06:31:04','54:c9:df:af:57:0b','194.223.2.107',1,0,NULL,4,1),('c4:2f:ac:08:53:18','54:c9:df:e7:02:4c','125.254.19.151',1,0,NULL,5,9),('c4:4e:ac:0b:42:f5','44:33:4c:22:23:09','203.220.168.118',1,0,NULL,6,12),('c4:4e:ac:14:28:8b','10:a4:be:02:4e:b7','101.181.124.219',0,0,NULL,7,16),('c4:4e:ac:11:4f:93','54:c9:df:77:3d:94','203.220.14.100',1,0,NULL,8,19),('c4:4e:ac:14:9b:45','10:a4:be:dc:10:7a','110.32.189.100',1,0,NULL,9,7),('c4:2f:ac:08:53:52','54:c9:df:e7:01:f7','101.188.10.161',1,0,NULL,10,1),('c4:4e:ac:0b:42:fd','44:33:4c:22:1e:13','220.233.186.107',0,0,NULL,11,15),('c4:2f:ac:06:30:36','54:c9:df:af:57:29','203.219.192.153',0,0,NULL,12,8),('c4:4e:ac:11:9f:e8','ec:3d:fd:01:17:10','210.49.70.65',1,0,NULL,13,1),('c4:4e:ac:12:42:a9','54:c9:df:be:f6:34','124.188.151.36',1,0,NULL,14,1),('c4:2f:ac:03:48:17','54:c9:df:72:a5:2e','59.102.36.71',1,0,NULL,15,1),('c4:4e:ac:12:40:ef','54:c9:df:be:ae:7a','175.33.93.250',0,0,NULL,16,20),('c4:2f:ac:08:53:73','54:c9:df:e7:01:af','144.133.105.170',1,0,NULL,17,14),('c4:2f:ac:07:86:69','54:c9:df:e6:db:c3','112.141.246.91',0,0,NULL,18,1),('c4:4e:ac:11:9f:09','ec:3d:fd:01:1e:10','1.143.59.247',0,0,NULL,19,1),('c4:4e:ac:12:45:11','54:c9:df:be:af:8b','101.188.41.92',0,0,NULL,20,1),('c4:2f:ac:06:31:17','54:c9:df:af:55:21','101.169.5.117',1,0,NULL,21,10),('c4:4e:ac:12:3b:1b','54:c9:df:a7:8a:8e','59.102.61.167',1,0,NULL,22,18),('c4:4e:ac:12:48:05','54:c9:df:be:f6:63','116.35.105.77',0,0,NULL,23,1),('c4:4e:ac:11:9f:14','ec:3d:fd:05:4b:de','101.116.107.82',0,0,NULL,24,1),('c4:4e:ac:12:42:a7','54:c9:df:be:d9:26','120.158.34.114',0,0,NULL,25,1),('c4:4e:ac:14:e6:ce','88:83:5d:16:33:5a','101.116.71.187',0,0,NULL,26,1),('c4:4e:ac:0b:42:48','44:33:4c:22:22:b9','194.193.143.125',1,0,NULL,27,22),('c4:4e:ac:14:e6:15','88:83:5d:16:2a:41','144.132.40.91',1,0,NULL,28,1),('c4:4e:ac:14:9a:40','10:a4:be:dc:0e:25','122.107.147.7',0,0,NULL,29,1),('c4:2f:ac:07:87:35','54:c9:df:d3:76:62','203.63.9.92',0,0,NULL,30,1),('c4:4e:ac:12:45:46','54:c9:df:be:b0:0e','1.234.185.149',0,0,NULL,31,1),('00:0f:a3:45:a1:1e','00:e0:4c:81:88:51','123.200.166.54',0,0,NULL,32,5),('c4:4e:ac:14:9b:6b','10:a4:be:dc:0f:de','101.188.52.203',0,0,NULL,33,1),('c4:4e:ac:11:91:f1','54:c9:df:77:05:3a','123.243.113.109',0,0,NULL,34,1),('c4:2f:ac:07:89:21','54:c9:df:e6:db:af','14.202.30.214',1,0,NULL,35,11),('c4:2f:ac:03:48:24','54:c9:df:72:a5:22','27.33.88.40',0,0,NULL,36,1),('c4:4e:ac:14:29:19','10:a4:be:03:46:fa','149.167.81.168',0,0,NULL,37,1),('c4:4e:ac:11:8f:cb','54:c9:df:77:43:9d','1.143.59.109',0,0,NULL,38,1),('00:0f:a3:45:a1:20','44:33:4c:22:1f:d5','112.208.194.181',0,0,NULL,39,21),('f2:23:4f:b5:50:e4','a0:2c:36:ea:af:bd','123.200.166.54',1,0,NULL,40,4),('c4:4e:ac:0b:41:ec','44:33:4c:22:20:7d','14.202.30.6',0,0,NULL,41,1),('c4:2f:ac:08:53:64','54:c9:df:e7:01:ed','101.182.125.30',0,0,NULL,42,1),('c4:4e:ac:14:28:f8','10:a4:be:03:8c:50','175.32.105.3',0,0,NULL,43,1),('c4:4e:ac:12:81:76','08:ea:40:fd:19:c1','120.148.147.244',0,0,NULL,46,1);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questions` (
  `writer_id` tinyint(4) unsigned NOT NULL DEFAULT '1',
  `title` varchar(80) DEFAULT NULL,
  `content` mediumtext,
  `create_date` datetime DEFAULT NULL,
  `count_of_answers` tinyint(4) NOT NULL DEFAULT '0',
  `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `writer_id` (`writer_id`),
  KEY `id` (`id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`writer_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (2,'질문 답변 게시판 입니다. 궁금하신 사항은 여기에 질문을 올려주세요.','라일락TV에  관련한 궁금한 사항이나 질문이 있으시면 여기 게시판을 활용해 주세요. 최대한 신속하게 답변을 올리겠습니다. \r\n감사합니다 :)','2019-08-06 03:09:04',0,1);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `state` varchar(80) DEFAULT NULL,
  `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES ('Wait',1),('Activated',2),('Expired',3);
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscription`
--

DROP TABLE IF EXISTS `subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subscription` (
  `lilac_tv_id` tinyint(4) unsigned DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `status_id` tinyint(4) unsigned NOT NULL DEFAULT '1',
  `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `lilac_tv_id` (`lilac_tv_id`),
  KEY `status_id` (`status_id`),
  KEY `id` (`id`),
  CONSTRAINT `subscription_ibfk_1` FOREIGN KEY (`lilac_tv_id`) REFERENCES `items` (`id`),
  CONSTRAINT `subscription_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscription`
--

LOCK TABLES `subscription` WRITE;
/*!40000 ALTER TABLE `subscription` DISABLE KEYS */;
INSERT INTO `subscription` VALUES (2,'2019-08-12 04:14:13','2029-08-18 22:14:50',2,1),(32,'2019-08-13 04:43:00','2029-08-18 22:15:28',2,3),(1,'2019-08-15 02:41:16','2029-08-15 02:41:16',2,4),(9,'2019-09-02 06:03:32','2029-09-02 06:03:32',2,6),(12,'2019-09-02 08:33:00','2029-09-02 08:33:00',2,7),(5,'2019-09-02 09:55:01','2029-09-02 09:55:01',2,8),(21,'2019-09-02 11:41:26','2029-09-02 11:41:26',2,9),(35,'2019-09-02 21:44:25','2029-09-02 21:44:25',2,10),(6,'2019-09-02 23:18:46','2029-09-02 23:18:46',2,11),(17,'2019-09-03 04:28:34','2029-09-03 04:28:34',2,12),(11,'2019-09-03 08:23:05','2029-09-03 08:23:05',2,13),(7,'2019-09-03 10:34:25','2029-09-03 10:34:25',2,14),(22,'2019-09-03 10:48:13','2029-09-03 10:48:13',2,15),(8,'2019-09-03 11:20:50','2029-09-03 11:20:50',2,16),(16,'2019-09-03 11:40:06','2029-09-03 11:40:06',2,17),(39,'2019-09-03 13:02:57','2029-09-03 13:02:57',2,18),(27,'2019-09-03 13:03:44','2029-09-03 13:03:44',2,19),(40,'2019-09-04 01:36:49','2029-09-04 01:36:49',2,20);
/*!40000 ALTER TABLE `subscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `name` varchar(80) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `password` varchar(80) DEFAULT NULL,
  `id` tinyint(4) unsigned NOT NULL AUTO_INCREMENT,
  `reset_token` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('admin','admin@test.com','1234567890','171eca5f320a51d6e54d76979824c9475fb5831f72032d13c19be736223ba427',1,NULL),('LilacTV','railrac23@gmail.com','0404466342','171eca5f320a51d6e54d76979824c9475fb5831f72032d13c19be736223ba427',2,NULL),('LilacTV 1층','railrac@gmail.com','0450944762','171eca5f320a51d6e54d76979824c9475fb5831f72032d13c19be736223ba427',3,NULL),('SeeboTest','jin.kim@seebo.com.au','0404466342','171eca5f320a51d6e54d76979824c9475fb5831f72032d13c19be736223ba427',4,NULL),('SeeboTest1','test1@test1.com','0404466342','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',5,NULL),('Huijin Ra','jeenyra@gmail.com','0430730315','4c4baaa133ad502ad620e1ad28f541b74a106573c7990cce8d806b89141f224c',6,NULL),('강희균','khkau17214@gmail.com','0402361751','6e93041c349b94f3ac18002c1875917e0f3360346ac1f333bf59197ad4783bad',7,NULL),('조현수','hsjo0904@gmail.com','0481963062','f29ab8a8703d94cacb1215814e9dcadc9cdf59f897dd93f7ff0e1c2f52a30afb',8,NULL),('황성민','widehwideh7575@gmail.com','0426224169','077882e6f6f0ad8a976aeb6dae8d9e1c09a23b1fb75c123d08d3bb9dfead7dd6',9,NULL),('Irene Nam','junha104@gmail.com','0403532100','f1bf75da7f95e4563b02a7acd49a28e9a2387b277de0f4d6bf3373398a4b5add',10,NULL),('신창섭','louis.shin09@gmail.com ','0433473904','fc15cb4fda3fd6653fcc1189f2fc5a913a1c594adb69b508cb7263e98c8eef3b',11,NULL),('Terry Yun','lerins88@gmail.com','0425267805','257b136f644d4bad6a2bba4ba92a96c01a1429932daf9f3b35f19fab97321c2e',12,NULL),('Sujeong Lee ','sjlee-au@hotmail.com','0431569413','32e50e90d59d7f0e160e39ddc52e1a0741144fed98f5691714e826f26b70f068',13,NULL),('박시형','seehyung@hanmail.net','0401529456','d712f71b91d3e7ffdb4415db878d5713af255fa4cca65e235499e8f41da86db1',14,NULL),('장래혁 ','jrh123jang@gmail.com','0499772336','3b62c87ddb2f8da1a3db4332b12fb8d157d6ae2910be147fc03838abadd7623b',15,NULL),('김동철','donkim365@hotmail.com','0423261600','91fd14cb98d4ed15ad2c18e30373f16b5838657207dd67dafed145d1c259d291',16,NULL),('성정훈','ohayo777@gmail.com','0404564400','3e7e0e5f4023f1ec33cd66bc860c28c2db957b5d28ea5f21bac6f92058f233c1',17,NULL),('Sung Min JO','lovejesus75@gmail.com','0409987690','840e39d3f3559f43d00fc031aa1128fffacd1738acb9bfe487106437c9da62f9',18,NULL),('손수경','ssk1845@yahoo.co.kr','0430185067','67c18104c6b389e77cb1dc6cf48fcfe47299e00ce0f25354ece3484ac66aac34',19,NULL),('박희태','s13795s@nate.com','0404959416','01c8ca8989e9bdeb8e1ec6cc3509cbd94ab73f0c1a7cbb667c6fae590fcb0a0e',20,NULL),('김명수','sh5151@hanmail.net','0405054262','967630df571d4ee25bbf83d1c73ec3bb8a38bc413d6dc27ba0c8e707181b1686',21,NULL),('백연선','bysunny100@naver.com','0487438550','afac1bbae618ce6123f7fdae7ef97a5671132ecc471fe4c4fc5c2581dd8fd996',22,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-04 13:15:59
