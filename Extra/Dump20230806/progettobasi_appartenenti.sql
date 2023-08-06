CREATE DATABASE  IF NOT EXISTS `progettobasi` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `progettobasi`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: progettobasi
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appartenenti`
--

DROP TABLE IF EXISTS `appartenenti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appartenenti` (
  `CorsoLaurea` varchar(50) NOT NULL,
  `CodCorso` varchar(50) NOT NULL,
  `Anno` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`CorsoLaurea`,`CodCorso`),
  KEY `CodCorso` (`CodCorso`),
  CONSTRAINT `appartenenti_ibfk_1` FOREIGN KEY (`CorsoLaurea`) REFERENCES `corsi_di_laurea` (`CodCorsoLaurea`),
  CONSTRAINT `appartenenti_ibfk_2` FOREIGN KEY (`CodCorso`) REFERENCES `corsi` (`CodiceCorso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appartenenti`
--

LOCK TABLES `appartenenti` WRITE;
/*!40000 ALTER TABLE `appartenenti` DISABLE KEYS */;
INSERT INTO `appartenenti` VALUES ('CL001','CT0005','Primo anno'),('CL001','CT0006','Secondo anno'),('CL001','CT0090','Terzo anno'),('CL001','CT0374','Primo anno'),('CL002','CT0005','Primo anno'),('CL002','CT0066','Terzo anno'),('CL002','CT0111','Secondo anno'),('CL003','ET4004','Secondo anno'),('CL003','ET4011','Primo anno'),('CL003','ET4017','Primo anno'),('CL003','ET4025','Terzo anno'),('CL004','LT7041','Primo anno'),('CL004','LT7042','Primo anno'),('CL004','LT7051','Terzo anno'),('CL004','LT7054','Secondo anno');
/*!40000 ALTER TABLE `appartenenti` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-06 11:43:47
