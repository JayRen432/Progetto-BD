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
-- Table structure for table `temporaryuser`
--

DROP TABLE IF EXISTS `temporaryuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temporaryuser` (
  `CodiceFiscale` varchar(16) NOT NULL,
  `Nome` varchar(100) DEFAULT NULL,
  `Cognome` varchar(100) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  `annoNascita` varchar(20) DEFAULT NULL,
  `matricola` varchar(6) DEFAULT '000000',
  `password` varchar(520) DEFAULT NULL,
  `CorsoLaurea` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`CodiceFiscale`),
  KEY `CorsoLaurea` (`CorsoLaurea`),
  CONSTRAINT `temporaryuser_ibfk_1` FOREIGN KEY (`CorsoLaurea`) REFERENCES `corsi_di_laurea` (`CodCorsoLaurea`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temporaryuser`
--

LOCK TABLES `temporaryuser` WRITE;
/*!40000 ALTER TABLE `temporaryuser` DISABLE KEYS */;
INSERT INTO `temporaryuser` VALUES ('PTRPRM95A17B666Q','Pietro','Primo','pietro@libero.it','1995-11-17','000000','09c12d01508bb6b857cf2f84199fb3134b58985806b40d6440a1acf453b2e106','CL002'),('STFSST93Z13A589D','Stefano ','Sesto','stefano@yahoo.it','1993-10-13','000000','05b9115df05a2a467841772eccc969822d884c9e71841050fe9e0893cce7d11b','CL003');
/*!40000 ALTER TABLE `temporaryuser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-06 11:43:48
