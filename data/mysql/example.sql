-- MySQL dump 10.11
--
-- Host: 127.0.0.1    Database: example
-- ------------------------------------------------------
-- Server version	5.0.41
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO,ANSI' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table "user"
--

DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "id" int(11) NOT NULL auto_increment,
  "email" varchar(255) default NULL,
  "username" varchar(255) default NULL,
  "password" varchar(255) default NULL,
  "name" varchar(100) default NULL,
  "gender" char(1) default NULL,
  "updated_at" datetime NOT NULL,
  "created_at" datetime NOT NULL,
  PRIMARY KEY  ("id"),
  UNIQUE KEY "username" ("username"),
  UNIQUE KEY "email" ("email")
);

--
-- Dumping data for table "user"
--

/*!40000 ALTER TABLE "user" DISABLE KEYS */;
INSERT INTO "user" VALUES (1,'matt@email.com','matt',NULL,'Matt','m','2011-08-16 23:41:55','2011-08-14 10:09:57'),(2,'james@email.com','james',NULL,'James','m','2011-08-14 10:10:24','2011-08-14 10:10:28'),(3,'adam@email.com','adam',NULL,'Adam','m','2011-08-14 10:11:47','2011-08-14 10:11:51');
/*!40000 ALTER TABLE "user" ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-01-15 21:05:34
