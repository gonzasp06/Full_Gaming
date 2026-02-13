-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: catalogo
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `codigos_postales`
--

DROP TABLE IF EXISTS `codigos_postales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `codigos_postales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provincia` varchar(100) NOT NULL,
  `municipio` varchar(100) NOT NULL,
  `codigo_postal` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_postal` (`codigo_postal`,`provincia`,`municipio`),
  KEY `idx_codigos_postales_provincia` (`provincia`),
  KEY `idx_codigos_postales_municipio` (`municipio`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigos_postales`
--

LOCK TABLES `codigos_postales` WRITE;
/*!40000 ALTER TABLE `codigos_postales` DISABLE KEYS */;
INSERT INTO `codigos_postales` VALUES (1,'Buenos Aires','Buenos Aires','1000'),(15,'CABA','Caballito','1425'),(10,'CABA','Recoleta','1425'),(14,'CABA','Belgrano','1426'),(12,'CABA','Vicente López','1638'),(11,'CABA','San Isidro','1642'),(13,'CABA','San Martín','1650'),(7,'Buenos Aires','Lanús','1824'),(8,'Buenos Aires','Lomas de Zamora','1836'),(9,'Buenos Aires','Almirante Brown','1870'),(6,'Buenos Aires','Quilmes','1876'),(2,'Buenos Aires','La Plata','1900'),(3,'Buenos Aires','La Plata','1910'),(23,'Santa Fe','Rosario','2000'),(24,'Santa Fe','Rosario','2004'),(25,'Santa Fe','Santa Fe','3000'),(37,'Entre Ríos','Paraná','3100'),(38,'Entre Ríos','Concordia','3200'),(34,'Misiones','Oberá','3360'),(33,'Misiones','Puerto Iguazú','3370'),(29,'Tucumán','San Miguel de Tucumán','4000'),(30,'Tucumán','San Miguel de Tucumán','4001'),(31,'Salta','Salta','4400'),(32,'Salta','Salta','4401'),(16,'Córdoba','Córdoba','5000'),(17,'Córdoba','Córdoba','5001'),(18,'Córdoba','Córdoba','5002'),(19,'Córdoba','Córdoba','5003'),(20,'Córdoba','Córdoba','5004'),(21,'Córdoba','Córdoba','5005'),(22,'Córdoba','Córdoba','5006'),(26,'Mendoza','Mendoza','5500'),(27,'Mendoza','Godoy Cruz','5501'),(28,'Mendoza','Guaymallén','5521'),(4,'Buenos Aires','Mar del Plata','7600'),(5,'Buenos Aires','Mar del Plata','7610'),(35,'Chubut','Comodrivadavia','9100'),(36,'Chubut','Trelew','9100');
/*!40000 ALTER TABLE `codigos_postales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direcciones`
--

DROP TABLE IF EXISTS `direcciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direcciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `calle` varchar(255) NOT NULL,
  `numero` varchar(20) NOT NULL,
  `piso_departamento` varchar(50) DEFAULT NULL,
  `codigo_postal` varchar(10) NOT NULL,
  `provincia` varchar(100) NOT NULL,
  `municipio` varchar(100) NOT NULL,
  `es_principal` tinyint(1) DEFAULT '0',
  `creado_en` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `codigo_postal` (`codigo_postal`),
  KEY `idx_direcciones_usuario` (`usuario_id`),
  CONSTRAINT `direcciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`idusuario`) ON DELETE CASCADE,
  CONSTRAINT `direcciones_ibfk_2` FOREIGN KEY (`codigo_postal`) REFERENCES `codigos_postales` (`codigo_postal`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direcciones`
--

LOCK TABLES `direcciones` WRITE;
/*!40000 ALTER TABLE `direcciones` DISABLE KEYS */;
INSERT INTO `direcciones` VALUES (3,22,'Las fucsias','798','','5501','Mendoza','Godoy Cruz',0,'2026-02-13 20:49:15','2026-02-13 20:49:15');
/*!40000 ALTER TABLE `direcciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido_items`
--

DROP TABLE IF EXISTS `pedido_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `pedido_items_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `pedido_items_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_items`
--

LOCK TABLES `pedido_items` WRITE;
/*!40000 ALTER TABLE `pedido_items` DISABLE KEYS */;
INSERT INTO `pedido_items` VALUES (1,1,54,1,10000.00,10000.00),(4,2,54,1,10000.00,10000.00),(5,3,54,1,10000.00,10000.00),(7,4,54,1,10000.00,10000.00),(9,5,54,1,10000.00,10000.00),(10,6,54,1,10000.00,10000.00),(16,10,54,2,10000.00,20000.00),(17,11,54,3,10000.00,30000.00),(21,13,54,3,10000.00,30000.00),(24,14,54,2,10000.00,20000.00),(30,20,54,1,200000.00,200000.00),(31,21,54,1,200000.00,200000.00);
/*!40000 ALTER TABLE `pedido_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) NOT NULL,
  `estado` varchar(50) DEFAULT 'completado',
  `direccion` varchar(255) DEFAULT NULL,
  `provincia` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `dni` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,NULL,'anonimo@email.com','2025-12-10 00:52:21',42222.00,'completado',NULL,NULL,NULL,NULL,NULL),(2,NULL,'anonimo@email.com','2025-12-10 00:57:08',20000.00,'completado',NULL,NULL,NULL,NULL,NULL),(3,NULL,'anonimo@email.com','2025-12-10 00:57:12',20000.00,'completado',NULL,NULL,NULL,NULL,NULL),(4,NULL,'anonimo@email.com','2025-12-10 00:57:39',20000.00,'completado',NULL,NULL,NULL,NULL,NULL),(5,NULL,'anonimo@email.com','2025-12-10 00:58:33',20000.00,'completado',NULL,NULL,NULL,NULL,NULL),(6,NULL,'anonimo@email.com','2025-12-10 00:58:36',20000.00,'completado',NULL,NULL,NULL,NULL,NULL),(7,NULL,'anonimo@email.com','2025-12-10 00:59:25',20000.00,'completado',NULL,NULL,NULL,NULL,NULL),(8,NULL,'anonimo@email.com','2025-12-10 01:03:33',42222.00,'completado',NULL,NULL,NULL,NULL,NULL),(9,NULL,'anonimo@email.com','2025-12-10 01:03:35',42222.00,'completado',NULL,NULL,NULL,NULL,NULL),(10,NULL,'anonimo@email.com','2025-12-10 01:04:38',52222.00,'completado',NULL,NULL,NULL,NULL,NULL),(11,NULL,'anonimo@email.com','2025-12-10 01:04:43',62222.00,'completado',NULL,NULL,NULL,NULL,NULL),(12,NULL,'anonimo@email.com','2025-12-10 01:05:22',62222.00,'completado',NULL,NULL,NULL,NULL,NULL),(13,NULL,'anonimo@email.com','2025-12-10 01:07:21',62222.00,'completado',NULL,NULL,NULL,NULL,NULL),(14,NULL,'anonimo@email.com','2025-12-10 01:09:03',20000.00,'completado',NULL,NULL,NULL,NULL,NULL),(15,NULL,'anonimo@email.com','2025-12-10 02:05:55',99999.00,'completado',NULL,NULL,NULL,NULL,NULL),(16,22,'bautiriveirabuca8@gmail.com','2025-12-15 21:32:57',99999.00,'completado',NULL,NULL,NULL,NULL,NULL),(17,22,'bautiriveirabuca8@gmail.com','2025-12-17 20:30:31',22222.00,'completado',NULL,NULL,NULL,NULL,NULL),(18,22,'bautiriveirabuca8@gmail.com','2025-12-17 23:35:10',22222.00,'completado',NULL,NULL,NULL,NULL,NULL),(19,NULL,'anonimo@email.com','2026-02-01 22:48:23',44444.00,'completado',NULL,NULL,NULL,NULL,NULL),(20,22,'bautiriveirabuca8@gmail.com','2026-02-13 20:54:08',200000.00,'completado',NULL,NULL,NULL,NULL,NULL),(21,22,'bautiriveirabuca8@gmail.com','2026-02-13 20:56:29',200000.00,'completado',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `categoria` varchar(100) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `foto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (54,'Teclado Gamer Corsair','<p>Hola</p>','Teclados',200000.00,105,'static/uploads\\compragamer_Imganen_general_40192_Teclado_Mecanico_Corsair_K65_PLUS_75__Wireless_2.4Ghz_Bluetooth_1ms_Switch_MLX_Red_RGB_266Hs_bc8f25f1-grn.jpg');
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idusuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  `direccion` varchar(255) DEFAULT NULL,
  `provincia` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `dni` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`idusuario`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (20,'Carlos','Martínez','carlos@example.com','$2b$12$/JGvnWbOwa9En8yNN1WkROLJOMp5z3lTykRlzZ81jPyGsJrEL1Xha',0,NULL,NULL,NULL,NULL,NULL),(22,'Bautista','','bautiriveirabuca8@gmail.com','$2b$12$Kk2NAqII1V3dwGIQFBQeFeqap3mG8GsViWkZwXwwuycdAFaRSa.Vy',0,NULL,NULL,NULL,NULL,'2604265930'),(23,'Bautista','Riveira Buca','bautiriveirabuca8@mail.com','$2b$12$sJND3SIazcpW5m5rMEaI8OjLmR.zgsqZ1//2iDqZANr5lRT9B20vC',0,NULL,NULL,NULL,NULL,NULL),(25,'Bautista','Riveira Buca','bautiriveira@gmail.com','$2b$12$qAOk.eruMpkGUmZnyTH6L.OpxGwCavwuOQAr3mgOS9WSyjbuD5Ot2',0,NULL,NULL,NULL,NULL,NULL),(26,'Bautista','Admin','bautista@admin.com','$2b$12$OFWy5UQerAsq/8jXEHmqNOGofg/mdChKen9yRUNx0LvJwoeXWrRsm',1,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-13 18:01:40
