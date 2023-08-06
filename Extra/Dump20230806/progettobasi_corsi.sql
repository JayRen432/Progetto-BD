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
-- Table structure for table `corsi`
--

DROP TABLE IF EXISTS `corsi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corsi` (
  `CodiceCorso` varchar(50) NOT NULL,
  `NomeCorso` varchar(100) DEFAULT NULL,
  `Valore` int DEFAULT NULL,
  PRIMARY KEY (`CodiceCorso`),
  UNIQUE KEY `NomeCorso` (`NomeCorso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corsi`
--

LOCK TABLES `corsi` WRITE;
/*!40000 ALTER TABLE `corsi` DISABLE KEYS */;
INSERT INTO `corsi` VALUES ('CT0005','Architettura degli elaboratori',12),('CT0006','Base di dati',12),('CT0066','Diritto dell informatica',6),('CT0090','Ingegneria del software',6),('CT0111','Probabilità e statistica',6),('CT0125','Sistemi operativi',12),('CT0178','Linguaggi per la rete',6),('CT0371','Aldoritmi e strutture dati',12),('CT0372','Programmazione ad oggetti',12),('CT0373','Reti di calcolatori',6),('CT0374','Calcolabilità e linguaggi formali',6),('CT0429','Analisi predittiva',6),('CT0441','Introduzione alla programmazione',6),('CT0509','Data & web minig',6),('CT0539','Sicurezza',6),('CT0540','Social network analysis',6),('ET4004','Accounting and business administration',12),('ET4008','Banking law',6),('ET4011','Monetary economics',6),('ET4015','Data managment',12),('ET4017','Diritto contabile',6),('ET4018','Introduction to coding',12),('ET4021','English for economics',6),('ET4022','English for business practice',6),('ET4025','Public governance and markets regulation',6),('LT7040','Storai dei rapporti tra Europa e Giappone',6),('LT7041','Letteratura Giapponese',3),('LT7042','Lingua Giapponese',3),('LT7050','Storia delle relazioni iternazionali',12),('LT7051','Lingua Cinese avanzata',12),('LT7052','Lingua Coreana',6),('LT7053','Lingua Coreana Esercitazioni',6),('LT7054','Lingua Cinese di base',12),('LT7060','Lettratura Cinese',12),('LT7061','Letteratura Coreana',12);
/*!40000 ALTER TABLE `corsi` ENABLE KEYS */;
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
