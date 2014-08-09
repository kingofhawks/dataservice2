-- MySQL dump 10.13  Distrib 5.5.27, for Win32 (x86)
--
-- Host: localhost    Database: zx
-- ------------------------------------------------------
-- Server version	5.5.27

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` char(30) NOT NULL,
  `customerId` char(30) DEFAULT NULL,
  `payKey` char(10) DEFAULT NULL,
  `openDate` date DEFAULT NULL,
  `openInfo` varchar(300) DEFAULT NULL,
  `balance` int(11) DEFAULT NULL,
  `cancelDate` date DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES ('acc1000','cus1000','123456','2013-04-27','账户1',NULL,'2013-04-28','无'),('acc1001','cus1001','abcde','2013-04-27','账户2',NULL,'2013-05-06','客户2的帐号'),('acc1002','cus1000','89756','2013-04-27','帐户2',NULL,NULL,'客户1');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admingroup`
--

DROP TABLE IF EXISTS `admingroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admingroup` (
  `id` char(30) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admingroup`
--

LOCK TABLES `admingroup` WRITE;
/*!40000 ALTER TABLE `admingroup` DISABLE KEYS */;
INSERT INTO `admingroup` VALUES ('admin1000','一级管理员','comment01'),('admin1001','二级管理员','comment02comment02'),('superAdmin','超级管理员','超级管理员，拥有编辑所有信息的权限');
/*!40000 ALTER TABLE `admingroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `id` char(30) NOT NULL DEFAULT '',
  `name` varchar(100) DEFAULT NULL,
  `contactName` varchar(20) DEFAULT NULL,
  `identification` char(20) DEFAULT NULL,
  `tel` char(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `customerGroupId` char(30) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `post` int(6) DEFAULT NULL,
  `createDate` date DEFAULT NULL,
  `cancelDate` date DEFAULT NULL,
  `is_enterprise` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES ('cus1000','customer01','chen','431221199508092341','0510-12345678','chen@email.com','cuG1001','江苏南京',58971,'2013-03-11',NULL,'1'),('cus1001','customer02','wan','235421198312142341','0510-11111111','wang@email.com','cuG1002','南京',25890,'2013-03-11','2013-05-06','1'),('cus1002','customer03','xu','32165498712589','0510-22222222','xu@email.com','cuG1001','shanghai',89544,'2013-03-11',NULL,'0'),('cus1003','客户4','zhao','123465895125','0510-33333333','zhao@email.com','cuG1002','上海',89755,'2013-03-11',NULL,'1'),('cus1004','客户5','钱','125879769245','0510-44444444','qian@email.com','cuG1001','北京',444444,'2013-03-11',NULL,'0'),('cus1005','customer06','sun','12589758621','0510-55555555','sun@email.com','cuG1000','新疆',87888,'2013-03-11',NULL,'1'),('cus1006','customer07','li','2598746589','0510-66666666','li@email.com','cuG1001','西藏',39884,'2013-03-11',NULL,'0'),('cus1007','customer08','周','58975654231','0510-77777777','zhou@email.com','cuG1000','青海',34343,'2013-03-11',NULL,'1'),('cus1008','customer09','wang','589785462','025-111111111','wang09@email.com','cuG1001','甘肃',25890,'2013-03-11',NULL,'0'),('cus1009','customer10','customer张','1234567988552','12345655','customer_zhang@email.com','cuG1000','无锡',21400,'2013-03-11',NULL,'1'),('cus1010','cumtomer11','customer_wan','58974568977','12358794','customer_wan@email.com','cuG1001','镇江',43456,'2013-03-11',NULL,'0'),('cus1011','customer12','customer_杨','123465895125','0510-12345677','customer_yang@email.com','cuG1000','wuxi',21400,'2013-03-11','2013-05-27','1');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customergroup`
--

DROP TABLE IF EXISTS `customergroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customergroup` (
  `id` char(30) NOT NULL DEFAULT '',
  `name` varchar(100) DEFAULT NULL,
  `discountId` varchar(30) DEFAULT NULL,
  `productId` text,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customergroup`
--

LOCK TABLES `customergroup` WRITE;
/*!40000 ALTER TABLE `customergroup` DISABLE KEYS */;
INSERT INTO `customergroup` VALUES ('cuG1000','vip客户','dis1004','[u\'pro1005\', u\'pro1007\', u\'pro1004\', u\'pro1006\']','vip客户说明'),('cuG1001','普通客户','dis1005','[u\'pro1006\']','普通客户'),('cuG1002','一级客户','dis1004','[u\'pro1007\', u\'pro1004\', u\'pro1006\']',''),('cuG1003','二级客户','dis1004','[u\'pro1005\', u\'pro1004\']','二级客户说明'),('cuG1004','三级客户','dis1004','[u\'pro1004\', u\'pro1006\']','三级客户说明');
/*!40000 ALTER TABLE `customergroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discount`
--

DROP TABLE IF EXISTS `discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discount` (
  `id` char(30) NOT NULL,
  `discountValue` float(3,2) DEFAULT NULL,
  `isActive` char(1) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discount`
--

LOCK TABLES `discount` WRITE;
/*!40000 ALTER TABLE `discount` DISABLE KEYS */;
INSERT INTO `discount` VALUES ('dis1000',0.10,'1','无'),('dis1001',0.00,'1','无'),('dis1002',0.90,'1','无'),('dis1003',0.80,'0','无'),('dis1004',0.95,'0','无'),('dis1005',0.85,'0','无');
/*!40000 ALTER TABLE `discount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package`
--

DROP TABLE IF EXISTS `package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `package` (
  `id` char(30) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `packageDetail` text,
  `timeLimit` varchar(10) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `isActive` char(1) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package`
--

LOCK TABLES `package` WRITE;
/*!40000 ALTER TABLE `package` DISABLE KEYS */;
INSERT INTO `package` VALUES ('pac1000','套餐2','[u\'pro1001\']','50',20,'0','套餐2'),('pac1001','套餐1','[u\'pro1000\', u\'pro1003\']','40',20,'0','无'),('pac1002','套餐3','[u\'pro1001\']','40',10,'1','无'),('pac1003','套餐4','[u\'pro1002\', u\'pro1003\']','40',30,'1','无'),('pac1004','套餐5','[u\'pro1000\', u\'pro1003\', u\'pro1004\']','40',80,'1','无');
/*!40000 ALTER TABLE `package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` char(30) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `productCategoryId` char(30) DEFAULT NULL,
  `isActive` char(1) DEFAULT NULL,
  `path` varchar(200) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `unit` char(20) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('pro1000','m1型虚拟主机','prC1003','1','无',10,'个/天','1vcpu，512M内存,50G硬盘'),('pro1001','m2型虚拟主机','prC1003','1','无',20,'个/天','2vcpu,1G 内存'),('pro1002','m3型虚拟主机','prC1003','0','无',30,'个/天','4vcpu'),('pro1003','存储','prC1004','0','无',20,'/天','30G'),('pro1004','到期通知','prC1006','1','无',1,'/天','无'),('pro1005','邮件服务1','prC1005','1','无',2,'/天','无'),('pro1006','充值提醒','prC1006','1','无',1,'/天','无'),('pro1007','邮件服务2','prC1005','1','无',20,'/天','无');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productcategory`
--

DROP TABLE IF EXISTS `productcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `productcategory` (
  `id` char(30) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `serviceCategoryId` char(30) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productcategory`
--

LOCK TABLES `productcategory` WRITE;
/*!40000 ALTER TABLE `productcategory` DISABLE KEYS */;
INSERT INTO `productcategory` VALUES ('prC1003','云主机','seC1002','虚拟主机'),('prC1004','云存储','seC1002','存储'),('prC1005','套餐1','seC1001','无sfsdf'),('prC1006','短信服务','seC1001','无'),('prC1007','短信服务2','seC1001','无sfa');
/*!40000 ALTER TABLE `productcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchasepackage`
--

DROP TABLE IF EXISTS `purchasepackage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchasepackage` (
  `transactionId` char(30) NOT NULL,
  `customerId` char(30) DEFAULT NULL,
  `packageId` char(30) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `transactionDate` date DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`transactionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchasepackage`
--

LOCK TABLES `purchasepackage` WRITE;
/*!40000 ALTER TABLE `purchasepackage` DISABLE KEYS */;
INSERT INTO `purchasepackage` VALUES ('p1','cus1000','pac1002',30,1,'2012-03-20','comment1'),('p2','cus1001','pac1002',30,2,'2012-03-20','comment2'),('p3','cus1000','pac1001',40,2,'2013-03-23','comment3'),('p4','cus1001','pac1001',40,1,'2013-03-24','comment4');
/*!40000 ALTER TABLE `purchasepackage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchaseproduct`
--

DROP TABLE IF EXISTS `purchaseproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchaseproduct` (
  `transactionId` char(30) NOT NULL,
  `customerId` char(30) DEFAULT NULL,
  `productId` char(30) DEFAULT NULL,
  `discountValue` float(3,2) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `transactionDate` date DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`transactionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchaseproduct`
--

LOCK TABLES `purchaseproduct` WRITE;
/*!40000 ALTER TABLE `purchaseproduct` DISABLE KEYS */;
INSERT INTO `purchaseproduct` VALUES ('s1','cus1000','pro1000',0.50,30,1,'2013-04-22','comment'),('s2','cus1000','pro1001',0.90,30,1,'2013-04-22','comment2'),('s3','cus1001','pro1001',0.50,40,2,'2013-04-23','comment3'),('s4','cus1001','pro1000',0.90,30,1,'2013-03-23','comment4');
/*!40000 ALTER TABLE `purchaseproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicecategory`
--

DROP TABLE IF EXISTS `servicecategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicecategory` (
  `id` char(30) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicecategory`
--

LOCK TABLES `servicecategory` WRITE;
/*!40000 ALTER TABLE `servicecategory` DISABLE KEYS */;
INSERT INTO `servicecategory` VALUES ('seC1001','增值服务','提高服务质量的服务dsff'),('seC1002','云服务','云平台提供的云服务df');
/*!40000 ALTER TABLE `servicecategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sysadmin`
--

DROP TABLE IF EXISTS `sysadmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysadmin` (
  `id` char(30) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `adminGroupId` char(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sysadmin`
--

LOCK TABLES `sysadmin` WRITE;
/*!40000 ALTER TABLE `sysadmin` DISABLE KEYS */;
INSERT INTO `sysadmin` VALUES ('sys1000','admin01','827ccb0eea8a706c4c34a16891f84e7b','admin01@abc.com','admin1000'),('sys1001','root','adcaec3805aa912c0d0b14a81bedb6ff','root@abc.com','superAdmin');
/*!40000 ALTER TABLE `sysadmin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactionbill`
--

DROP TABLE IF EXISTS `transactionbill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transactionbill` (
  `transactionId` char(30) NOT NULL,
  `accountId` char(30) DEFAULT NULL,
  `item` varchar(300) DEFAULT NULL,
  `deposit` int(11) DEFAULT NULL,
  `expense` int(11) DEFAULT NULL,
  `transactionDate` date DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`transactionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactionbill`
--

LOCK TABLES `transactionbill` WRITE;
/*!40000 ALTER TABLE `transactionbill` DISABLE KEYS */;
INSERT INTO `transactionbill` VALUES ('d1','acc1000','item01',100,NULL,'2013-04-20','comment01'),('d2','acc1001','item04',300,NULL,'2013-03-22','comment02'),('d3','acc1002','item06',400,NULL,'2012-03-04','comment06'),('p3','acc1001','item05',NULL,40,'2013-03-23','comment05'),('s1','acc1000','item01',NULL,30,'2013-04-22','comment02'),('s2','acc1001','item03',NULL,20,'2013-04-22','comment02');
/*!40000 ALTER TABLE `transactionbill` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-06-05 17:47:18
