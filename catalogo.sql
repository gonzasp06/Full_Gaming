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
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigos_postales`
--

LOCK TABLES `codigos_postales` WRITE;
/*!40000 ALTER TABLE `codigos_postales` DISABLE KEYS */;
INSERT INTO `codigos_postales` VALUES (1,'Buenos Aires','Buenos Aires','1000'),(53,'CABA','Centro','1000'),(56,'CABA','Once','1026'),(57,'CABA','San Telmo','1104'),(58,'CABA','La Boca','1169'),(55,'CABA','Villa Crespo','1414'),(15,'CABA','Caballito','1425'),(54,'CABA','Palermo','1425'),(10,'CABA','Recoleta','1425'),(14,'CABA','Belgrano','1426'),(12,'CABA','Vicente López','1638'),(11,'CABA','San Isidro','1642'),(13,'CABA','San Martín','1650'),(7,'Buenos Aires','Lanús','1824'),(8,'Buenos Aires','Lomas de Zamora','1836'),(43,'Buenos Aires','Esteban Echeverría','1842'),(9,'Buenos Aires','Almirante Brown','1870'),(42,'Buenos Aires','Avellaneda','1870'),(6,'Buenos Aires','Quilmes','1876'),(40,'Buenos Aires','Berazategui','1884'),(41,'Buenos Aires','Florencio Varela','1888'),(2,'Buenos Aires','La Plata','1900'),(3,'Buenos Aires','La Plata','1910'),(39,'Buenos Aires','La Plata','1920'),(23,'Santa Fe','Rosario','2000'),(24,'Santa Fe','Rosario','2004'),(60,'Santa Fe','Rafaela','2300'),(62,'Santa Fe','Morteros','2540'),(61,'Santa Fe','Venado Tuerto','2600'),(25,'Santa Fe','Santa Fe','3000'),(37,'Entre Ríos','Paraná','3100'),(76,'Entre Ríos','Victoria','3153'),(38,'Entre Ríos','Concordia','3200'),(74,'Entre Ríos','Concepción del Uruguay','3260'),(75,'Entre Ríos','Gualeguaychú','3260'),(79,'Misiones','Leandro N. Alem','3324'),(82,'Corrientes','Saladas','3337'),(78,'Misiones','Aristóbulo del Valle','3350'),(34,'Misiones','Oberá','3360'),(81,'Corrientes','Paso de la Cruz','3370'),(33,'Misiones','Puerto Iguazú','3370'),(77,'Misiones','Eldorado','3380'),(80,'Corrientes','Corrientes','3400'),(83,'Corrientes','Mercedes','3470'),(59,'Santa Fe','Reconquista','3560'),(84,'Corrientes','Ituzaingó','3627'),(29,'Tucumán','San Miguel de Tucumán','4000'),(30,'Tucumán','San Miguel de Tucumán','4001'),(85,'Tucumán','San Miguel de Tucumán','4002'),(88,'Tucumán','Lules','4104'),(86,'Tucumán','Yerba Buena','4107'),(87,'Tucumán','Tafí Viejo','4134'),(89,'Tucumán','Monteros','4150'),(98,'Jujuy','Purmamarca','4348'),(97,'Jujuy','Tilcara','4380'),(31,'Salta','Salta','4400'),(32,'Salta','Salta','4401'),(92,'Salta','Oran','4530'),(93,'Salta','Tartagal','4560'),(94,'Jujuy','San Salvador de Jujuy','4600'),(90,'Salta','San Salvador de Jujuy','4600'),(95,'Jujuy','Palpalá','4610'),(96,'Jujuy','Perico','4626'),(91,'Salta','Villazón','4650'),(99,'Catamarca','San Fernando del Valle de Catamarca','4700'),(101,'Catamarca','Andalgalá','4754'),(102,'Catamarca','Santa María','4760'),(100,'Catamarca','Belén','4828'),(16,'Córdoba','Córdoba','5000'),(17,'Córdoba','Córdoba','5001'),(18,'Córdoba','Córdoba','5002'),(19,'Córdoba','Córdoba','5003'),(20,'Córdoba','Córdoba','5004'),(21,'Córdoba','Córdoba','5005'),(22,'Córdoba','Córdoba','5006'),(66,'Córdoba','Cosquín','5147'),(64,'Córdoba','Villa Carlos Paz','5152'),(65,'Córdoba','La Falda','5172'),(103,'La Rioja','La Rioja','5300'),(105,'La Rioja','Chamical','5310'),(106,'La Rioja','Arauco','5340'),(104,'La Rioja','Chilecito','5360'),(107,'San Juan','San Juan','5400'),(108,'San Juan','Deán Funes','5420'),(109,'San Juan','Jáchal','5450'),(110,'San Juan','San Martín','5480'),(26,'Mendoza','Mendoza','5500'),(27,'Mendoza','Godoy Cruz','5501'),(67,'Mendoza','Maipú','5505'),(68,'Mendoza','Luján de Cuyo','5507'),(28,'Mendoza','Guaymallén','5521'),(69,'Mendoza','San Martín','5550'),(71,'Mendoza','San Rafael','5600'),(73,'Mendoza','Malargüe','5613'),(72,'Mendoza','General Alvear','5690'),(70,'Mendoza','Tunuyán','5700'),(111,'San Luis','San Luis','5730'),(112,'San Luis','La Punta','5732'),(113,'San Luis','El Chorrillo','5733'),(63,'Córdoba','Río Cuarto','5800'),(114,'San Luis','Merlo','5881'),(46,'Buenos Aires','Junín','6000'),(52,'Buenos Aires','Carlos Casares','6260'),(135,'La Pampa','Santa Rosa','6300'),(138,'La Pampa','Anguil','6326'),(136,'La Pampa','General Pico','6360'),(137,'La Pampa','Intendente Alvear','6385'),(47,'Buenos Aires','Bragado','6600'),(49,'Buenos Aires','Salto','6650'),(48,'Buenos Aires','San Andrés de Giles','6680'),(44,'Buenos Aires','Tandil','7000'),(45,'Buenos Aires','Tandil','7100'),(50,'Buenos Aires','Azul','7300'),(51,'Buenos Aires','Olavarría','7400'),(4,'Buenos Aires','Mar del Plata','7600'),(5,'Buenos Aires','Mar del Plata','7610'),(131,'Neuquén','Neuquén','8300'),(129,'Río Negro','Cipolletti','8324'),(130,'Río Negro','General Roca','8332'),(132,'Neuquén','Zapala','8340'),(133,'Neuquén','San Martín de los Andes','8370'),(134,'Neuquén','Junín de los Andes','8371'),(127,'Río Negro','Bariloche','8400'),(128,'Río Negro','San Carlos de Bariloche','8400'),(126,'Río Negro','Viedma','8500'),(121,'Santa Cruz','Puerto Deseado','9050'),(35,'Chubut','Comodrivadavia','9100'),(122,'Chubut','Comodrivavia','9100'),(123,'Chubut','Puerto Madryn','9100'),(36,'Chubut','Trelew','9100'),(125,'Chubut','Rawson','9103'),(124,'Chubut','Esquel','9200'),(120,'Santa Cruz','Puerto Santa Cruz','9400'),(118,'Santa Cruz','Río Gallegos','9400'),(119,'Santa Cruz','El Calafate','9405'),(115,'Tierra del Fuego','Ushuaia','9410'),(116,'Tierra del Fuego','Río Grande','9420'),(117,'Tierra del Fuego','Tolhuin','9430');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direcciones`
--

LOCK TABLES `direcciones` WRITE;
/*!40000 ALTER TABLE `direcciones` DISABLE KEYS */;
INSERT INTO `direcciones` VALUES (4,22,'Las fucsias','798','','5600','Mendoza','San Rafael',1,'2026-02-13 22:51:16','2026-02-13 23:15:59'),(5,22,'Avenida 9 de julio','798','','1000','CABA','Centro',0,'2026-02-13 23:07:19','2026-02-13 23:15:59');
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
  `precio` int NOT NULL DEFAULT '0',
  `subtotal` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `pedido_items_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `pedido_items_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_items`
--

LOCK TABLES `pedido_items` WRITE;
/*!40000 ALTER TABLE `pedido_items` DISABLE KEYS */;
INSERT INTO `pedido_items` VALUES (1,1,54,1,10000,10000),(4,2,54,1,10000,10000),(5,3,54,1,10000,10000),(7,4,54,1,10000,10000),(9,5,54,1,10000,10000),(10,6,54,1,10000,10000),(16,10,54,2,10000,20000),(17,11,54,3,10000,30000),(21,13,54,3,10000,30000),(24,14,54,2,10000,20000),(30,20,54,1,200000,200000),(31,21,54,1,200000,200000),(32,22,54,5,200000,1000000),(33,23,54,7,200000,1400000);
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
  `total` int NOT NULL DEFAULT '0',
  `estado` varchar(50) DEFAULT 'completado',
  `direccion` varchar(255) DEFAULT NULL,
  `provincia` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `dni` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,NULL,'anonimo@email.com','2025-12-10 00:52:21',42222,'completado',NULL,NULL,NULL,NULL,NULL),(2,NULL,'anonimo@email.com','2025-12-10 00:57:08',20000,'completado',NULL,NULL,NULL,NULL,NULL),(3,NULL,'anonimo@email.com','2025-12-10 00:57:12',20000,'completado',NULL,NULL,NULL,NULL,NULL),(4,NULL,'anonimo@email.com','2025-12-10 00:57:39',20000,'completado',NULL,NULL,NULL,NULL,NULL),(5,NULL,'anonimo@email.com','2025-12-10 00:58:33',20000,'completado',NULL,NULL,NULL,NULL,NULL),(6,NULL,'anonimo@email.com','2025-12-10 00:58:36',20000,'completado',NULL,NULL,NULL,NULL,NULL),(7,NULL,'anonimo@email.com','2025-12-10 00:59:25',20000,'completado',NULL,NULL,NULL,NULL,NULL),(8,NULL,'anonimo@email.com','2025-12-10 01:03:33',42222,'completado',NULL,NULL,NULL,NULL,NULL),(9,NULL,'anonimo@email.com','2025-12-10 01:03:35',42222,'completado',NULL,NULL,NULL,NULL,NULL),(10,NULL,'anonimo@email.com','2025-12-10 01:04:38',52222,'completado',NULL,NULL,NULL,NULL,NULL),(11,NULL,'anonimo@email.com','2025-12-10 01:04:43',62222,'completado',NULL,NULL,NULL,NULL,NULL),(12,NULL,'anonimo@email.com','2025-12-10 01:05:22',62222,'completado',NULL,NULL,NULL,NULL,NULL),(13,NULL,'anonimo@email.com','2025-12-10 01:07:21',62222,'completado',NULL,NULL,NULL,NULL,NULL),(14,NULL,'anonimo@email.com','2025-12-10 01:09:03',20000,'completado',NULL,NULL,NULL,NULL,NULL),(15,NULL,'anonimo@email.com','2025-12-10 02:05:55',99999,'completado',NULL,NULL,NULL,NULL,NULL),(16,22,'bautiriveirabuca8@gmail.com','2025-12-15 21:32:57',99999,'completado',NULL,NULL,NULL,NULL,NULL),(17,22,'bautiriveirabuca8@gmail.com','2025-12-17 20:30:31',22222,'completado',NULL,NULL,NULL,NULL,NULL),(18,22,'bautiriveirabuca8@gmail.com','2025-12-17 23:35:10',22222,'completado',NULL,NULL,NULL,NULL,NULL),(19,NULL,'anonimo@email.com','2026-02-01 22:48:23',44444,'completado',NULL,NULL,NULL,NULL,NULL),(20,22,'bautiriveirabuca8@gmail.com','2026-02-13 20:54:08',200000,'completado',NULL,NULL,NULL,NULL,NULL),(21,22,'bautiriveirabuca8@gmail.com','2026-02-13 20:56:29',200000,'completado',NULL,NULL,NULL,NULL,NULL),(22,22,'bautiriveirabuca8@gmail.com','2026-02-13 23:38:42',1000000,'completado',NULL,NULL,NULL,NULL,NULL),(23,22,'bautiriveirabuca8@gmail.com','2026-02-13 23:39:09',1400000,'completado',NULL,NULL,NULL,NULL,NULL);
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
  `precio` int NOT NULL DEFAULT '0',
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
INSERT INTO `producto` VALUES (54,'Teclado Gamer Corsair','<p>Hola</p>','Teclados',200000,93,'static/uploads\\compragamer_Imganen_general_40192_Teclado_Mecanico_Corsair_K65_PLUS_75__Wireless_2.4Ghz_Bluetooth_1ms_Switch_MLX_Red_RGB_266Hs_bc8f25f1-grn.jpg');
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

-- Dump completed on 2026-02-13 20:46:52
