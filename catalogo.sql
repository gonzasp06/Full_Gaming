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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direcciones`
--

LOCK TABLES `direcciones` WRITE;
/*!40000 ALTER TABLE `direcciones` DISABLE KEYS */;
INSERT INTO `direcciones` VALUES (13,22,'Avenida 9 de julio','1234','','1000','CABA','Centro',1,'2026-02-15 21:02:22','2026-02-15 21:13:28'),(14,33,'Chile','650','','5600','Mendoza','San Rafael',1,'2026-02-22 17:35:23','2026-02-22 17:44:34');
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
  `costo_unitario_aplicado` decimal(12,2) DEFAULT NULL,
  `costo_total` decimal(12,2) DEFAULT NULL,
  `ganancia_item` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `pedido_items_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `pedido_items_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_items`
--

LOCK TABLES `pedido_items` WRITE;
/*!40000 ALTER TABLE `pedido_items` DISABLE KEYS */;
INSERT INTO `pedido_items` VALUES (34,24,58,1,19500,19500,15000.00,15000.00,4500.00),(35,25,59,2,85000,170000,66666.67,133333.34,36666.66),(36,26,58,1,19500,19500,15000.00,15000.00,4500.00),(37,27,59,1,85000,85000,66666.67,66666.67,18333.33),(38,27,61,1,43333,43333,33333.33,33333.33,9999.67),(39,28,60,1,260000,260000,200000.00,200000.00,60000.00);
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,NULL,'anonimo@email.com','2025-12-10 00:52:21',42222,'completado',NULL,NULL,NULL,NULL,NULL),(2,NULL,'anonimo@email.com','2025-12-10 00:57:08',20000,'completado',NULL,NULL,NULL,NULL,NULL),(3,NULL,'anonimo@email.com','2025-12-10 00:57:12',20000,'completado',NULL,NULL,NULL,NULL,NULL),(4,NULL,'anonimo@email.com','2025-12-10 00:57:39',20000,'completado',NULL,NULL,NULL,NULL,NULL),(5,NULL,'anonimo@email.com','2025-12-10 00:58:33',20000,'completado',NULL,NULL,NULL,NULL,NULL),(6,NULL,'anonimo@email.com','2025-12-10 00:58:36',20000,'completado',NULL,NULL,NULL,NULL,NULL),(7,NULL,'anonimo@email.com','2025-12-10 00:59:25',20000,'completado',NULL,NULL,NULL,NULL,NULL),(8,NULL,'anonimo@email.com','2025-12-10 01:03:33',42222,'completado',NULL,NULL,NULL,NULL,NULL),(9,NULL,'anonimo@email.com','2025-12-10 01:03:35',42222,'completado',NULL,NULL,NULL,NULL,NULL),(10,NULL,'anonimo@email.com','2025-12-10 01:04:38',52222,'completado',NULL,NULL,NULL,NULL,NULL),(11,NULL,'anonimo@email.com','2025-12-10 01:04:43',62222,'completado',NULL,NULL,NULL,NULL,NULL),(12,NULL,'anonimo@email.com','2025-12-10 01:05:22',62222,'completado',NULL,NULL,NULL,NULL,NULL),(13,NULL,'anonimo@email.com','2025-12-10 01:07:21',62222,'completado',NULL,NULL,NULL,NULL,NULL),(14,NULL,'anonimo@email.com','2025-12-10 01:09:03',20000,'completado',NULL,NULL,NULL,NULL,NULL),(15,NULL,'anonimo@email.com','2025-12-10 02:05:55',99999,'completado',NULL,NULL,NULL,NULL,NULL),(16,22,'bautiriveirabuca8@gmail.com','2025-12-15 21:32:57',99999,'completado',NULL,NULL,NULL,NULL,NULL),(17,22,'bautiriveirabuca8@gmail.com','2025-12-17 20:30:31',22222,'completado',NULL,NULL,NULL,NULL,NULL),(18,22,'bautiriveirabuca8@gmail.com','2025-12-17 23:35:10',22222,'completado',NULL,NULL,NULL,NULL,NULL),(19,NULL,'anonimo@email.com','2026-02-01 22:48:23',44444,'completado',NULL,NULL,NULL,NULL,NULL),(20,22,'bautiriveirabuca8@gmail.com','2026-02-13 20:54:08',200000,'completado',NULL,NULL,NULL,NULL,NULL),(21,22,'bautiriveirabuca8@gmail.com','2026-02-13 20:56:29',200000,'completado',NULL,NULL,NULL,NULL,NULL),(22,22,'bautiriveirabuca8@gmail.com','2026-02-13 23:38:42',1000000,'completado',NULL,NULL,NULL,NULL,NULL),(23,22,'bautiriveirabuca8@gmail.com','2026-02-13 23:39:09',1400000,'completado',NULL,NULL,NULL,NULL,NULL),(24,33,'guadaguerra@gmail.com','2026-02-22 17:35:49',19500,'completado','Paunero 650','Mendoza','5600',NULL,NULL),(25,33,'guadaguerra@gmail.com','2026-02-22 23:50:45',170000,'completado','Chile 650','Mendoza','5600','45256306','2604265930'),(26,22,'bautiriveirabuca888@gmail.com','2026-02-24 02:52:22',19500,'completado','Avenida 9 de julio 1234','CABA','1000','45256306','2604265930'),(27,33,'guadaguerra@gmail.com','2026-02-24 23:19:03',128333,'completado','Chile 650','Mendoza','5600','45256306','2604265930'),(28,33,'guadaguerra@gmail.com','2026-02-24 23:20:06',260000,'completado','Chile 650','Mendoza','5600','45256306','2604265930');
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
  `nombre` varchar(255) DEFAULT NULL,
  `descripcion` text,
  `categoria` varchar(100) DEFAULT NULL,
  `precio` int NOT NULL DEFAULT '0',
  `cantidad` int DEFAULT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (58,'Corsair teclado','<p>Teclado</p>','Teclados',19500,8,'static/uploads\\D_Q_NP_2X_839905-MLA87126424990_072025-V.webp',15000.00),(59,'Gamesir Cyclone 2','El GameSir Cyclone 2 es un joystick versátil diseñado para ofrecer una experiencia de juego fluida y cómoda en múltiples plataformas. Su conectividad Bluetooth, con cable (wired) y wireless permite alternar entre modos según la necesidad, garantizando baja latencia y gran compatibilidad. Su diseño ergonómico y agarre antideslizante aseguran largas horas de juego sin fatiga. Incorpora gatillos y botones de alta respuesta, ideales para títulos competitivos o de acción rápida. Además, su batería de larga duración y la posibilidad de jugar mientras se carga lo convierten en una opción confiable para jugadores exigentes.','Joysticks',85000,27,'static/uploads\\1994-producto-d-nq-np-2x-726239-mla10002555180.jpg',66666.67),(60,'Auriculares Corsair Void V2 Elite Wireless 2.4Ghz Bluetooth Premium Dolby Atmos 7.1 RGB White PC/PS/MAC 70Hs ','Sumérjase en la acción con los CORSAIR VOID RGB ELITE Wireless, con transductores de audio de neodimio de 50 mm de ajuste personalizado, un cómodo tejido de rejilla de microfibra con almohadillas de espuma con memoria y una conexión inalámbrica de 2,4 GHz.\r\n\r\nSONIDO INCREÍBLE\r\nEscúchelo todo con un sonido envolvente 7.1, desde la pisada más ligera hasta la explosión más atronadora, gracias a los transductores de audio de neodimio de alta densidad de 50 mm de ajuste personalizado con un rango de frecuencia ampliado de 20 Hz-30.000 Hz.\r\n\r\nCOMODIDAD TOTAL\r\nDiseñados para garantizar la comodidad en largas sesiones de juego, con un tejido de rejilla de microfibra transpirable y lujosas almohadillas de espuma con memoria.\r\n\r\nJUEGUE COMO QUIERA\r\nEl software CORSAIR iCUE permite controlar los auriculares de forma precisa con perfiles de audio preajustados, personalizar los ajustes del ecualizador, disfrutar de un sonido envolvente e inmersivo 7.1 y controlar el ruido local.','Audio',260000,49,'static/uploads\\compragamer_Imganen_general_47730_Auriculares_Corsair_Void_V2_Elite_Wireless_2.4Ghz_Bluetooth_Premium_Dolby_Atmos_7.1_RGB_White_PC_PS_MAC_70Hs_a4354f81-grn.jpg',200000.00),(61,'Joystick Redragon Harrow G808 inalámbrico negro','Control preciso\r\n\r\nEste mando combina funciones revolucionarias mientras conserva precisión, comodidad y exactitud en cada movimiento. Gracias a su ergonomía especialmente pensada para la posición de tu mano, podés pasar horas jugando con total confort.','Joysticks',43333,14,'static/uploads\\9194-producto-d-nq-np-892876-mlu72834470533-11.jpg',33333.33),(62,'Mouse Corsair Gaming IRONCLAW RGB Wireless','El ratón de juego CORSAIR IRONCLAW RGB WIRELESS combina un sensor óptico de 18&nbsp;000&nbsp;ppp nativos con un cómodo agarre para la palma. Puede conectarlo fácilmente al PC a través de una tecnología ultrarrápida, la TECNOLOGÍA SLIPSTREAM CORSAIR WIRELESS en menos de 1&nbsp;ms, Bluetooth o conexión por cable USB.','Mouse',162500,8,'static/uploads\\000000000041274743162-CH-9317011-NA-Gallery-IRONCLAW-RGB-WIRELESS-01.jpg',125000.00),(63,'PARLANTE BARRA DE SONIDO TRUST THORNE RGB WHITE','PARLANTE BARRA DE SONIDO TRUST THORNE RGB WHITE','Audio',83571,14,'static/uploads\\nb_PARLANTE-BARRA-DE-SONIDO-TRUST-THORNE-RGB-WHITE-GXT619W_export_fdd7d858433be5e7b1ede1fe7edf8731.png',64285.71),(64,'Parlantes G560 LIGHTSYNC PC Gaming LOGITECH','Logitech G560 ofrece un sonido natural, con una gran claridad y precisión, que se dispersa de manera uniforme. Un parlante que asegura potencia y calidad por igual en la reproducción de contenidos multimedia.\r\n\r\nGran potencia.\r\n\r\nDisfrutar de sonidos graves o de baja frecuencia con una calidad excelente será posible con este parlante subwoofer, incluso cuando subas el volumen. Olvidáte del amplificador. Al ser activo solo necesitarás conectarlo a la fuente de sonido y el mismo equipo se encargará de amplificar y reproducir: ganarás practicidad y espacio, ya que además requiere menos cableado que uno pasivo. Es la solución más conveniente si querés producir música en tu casa o en un estudio, y también para DJs. PARLANTES G560 LIGHTSYNC PARA JUEGOS EN PC','Audio',910000,10,'static/uploads\\47732-producto-vgfbvf560-gallery-1.jpg',700000.00),(65,'Monitor 24\" Asus Tuf VG249QL3A Gaming FHD Fast IPS 180Hz Altura Ajustable','El monitor ASUS VG249QL3A es una excelente opción para los entusiastas del gaming que buscan una experiencia visual inmersiva y de alta calidad. Con una pantalla de 24 pulgadas y resolución Full HD, este monitor ofrece imágenes nítidas y detalladas que harán que tus juegos cobren vida.\r\n\r\nUna de las características destacadas de este monitor es su panel Fast IPS con una frecuencia de actualización de 180Hz, lo que garantiza una reproducción fluida de imágenes sin desenfoques ni distorsiones. Esto es ideal para juegos de alta velocidad donde cada milisegundo cuenta.\r\n\r\nAdemás, el ASUS VG249QL3A cuenta con altura ajustable, lo que te permite encontrar la posición más cómoda para largas sesiones de juego. Su diseño ergonómico y bisel delgado también hacen que sea una adición elegante a tu setup de gaming. En resumen, el monitor ASUS VG249QL3A es una excelente elección para los gamers que buscan rendimiento, calidad de imagen y comodidad en un solo paquete. Experimenta tus juegos favoritos como nunca antes con este monitor de alta gama.','Otros',260000,15,'static/uploads\\96081-producto-nb-monitor-24-asus-as-vg249ql3a-gaming-fhd-fast-ips-180hz-altura-a.jpg',200000.00),(66,'Mouse Corsair Harpoon RGB Wireless Slipstream','El ratón para juegos CORSAIR HARPOON RGB WIRELESS le permite elegir cómo jugar, con la capacidad de conectarse fácilmente al PC a través de una tecnología ultrarrápida, la TECNOLOGÍA SLIPSTREAM CORSAIR WIRELESS en menos de 1&nbsp;ms, Bluetooth o conexión por cable USB.','Mouse',81250,8,'static/uploads\\0000000000412606866210413797--7-.png',62500.00);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_compras`
--

DROP TABLE IF EXISTS `stock_compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_compras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `inversion_total` decimal(12,2) NOT NULL,
  `cantidad_unidades` int NOT NULL,
  `costo_unitario` decimal(12,2) NOT NULL,
  `precio_venta_sugerido` decimal(12,2) DEFAULT NULL,
  `porcentaje_ganancia` decimal(8,2) DEFAULT '0.00',
  `observacion` varchar(255) DEFAULT NULL,
  `creado_en` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_stock_compras_producto` (`producto_id`),
  KEY `idx_stock_compras_usuario` (`usuario_id`),
  CONSTRAINT `fk_stock_compras_producto` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`),
  CONSTRAINT `fk_stock_compras_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`idusuario`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_compras`
--

LOCK TABLES `stock_compras` WRITE;
/*!40000 ALTER TABLE `stock_compras` DISABLE KEYS */;
INSERT INTO `stock_compras` VALUES (1,58,29,150000.00,10,15000.00,19500.00,30.00,'Carga inicial de producto','2026-02-22 17:24:32'),(2,59,26,2000000.00,30,66666.67,86666.67,30.00,'Carga inicial de producto','2026-02-22 23:45:50'),(3,60,29,10000000.00,50,200000.00,260000.00,30.00,'Carga inicial de producto','2026-02-24 01:26:28'),(4,61,29,500000.00,15,33333.33,43333.33,30.00,'Carga inicial de producto','2026-02-24 23:14:24'),(5,62,29,1000000.00,8,125000.00,162500.00,30.00,'Carga inicial de producto','2026-02-24 23:35:17'),(6,63,29,900000.00,14,64285.71,83571.43,30.00,'Carga inicial de producto','2026-02-24 23:38:43'),(7,64,29,7000000.00,10,700000.00,910000.00,30.00,'Carga inicial de producto','2026-02-24 23:42:45'),(8,65,29,3000000.00,15,200000.00,260000.00,30.00,'Carga inicial de producto','2026-02-24 23:49:32'),(9,66,29,500000.00,8,62500.00,81250.00,30.00,'Carga inicial de producto','2026-02-25 01:43:51');
/*!40000 ALTER TABLE `stock_compras` ENABLE KEYS */;
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
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `ultimo_acceso` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idusuario`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (20,'Carlos','Martínez','carlos@example.com','$2b$12$/JGvnWbOwa9En8yNN1WkROLJOMp5z3lTykRlzZ81jPyGsJrEL1Xha',0,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(22,'Bautista','','bautiriveirabuca888@gmail.com','$2b$12$Kk2NAqII1V3dwGIQFBQeFeqap3mG8GsViWkZwXwwuycdAFaRSa.Vy',0,'Avenida 9 de julio 1234','CABA','1000','45256306','2604265930','2026-02-21 21:46:59','2026-02-24 02:52:00'),(23,'Bautista','Riveira Buca','bautiriveirabuca8@mail.com','$2b$12$sJND3SIazcpW5m5rMEaI8OjLmR.zgsqZ1//2iDqZANr5lRT9B20vC',0,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(25,'Bautista','Riveira Buca','bautiriveira@gmail.com','$2b$12$qAOk.eruMpkGUmZnyTH6L.OpxGwCavwuOQAr3mgOS9WSyjbuD5Ot2',0,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(26,'Bautista','Admin','bautista@admin.com','$2b$12$OFWy5UQerAsq/8jXEHmqNOGofg/mdChKen9yRUNx0LvJwoeXWrRsm',1,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(27,'Bautista','Riveira','bauti123@gmail.com','$2b$12$dJmrIRiGm5vcWgLSwjKTuev.ynjz8Hux59klnOvOeMdCPSTr3mg2e',0,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(28,'Bautista','Riveira','bautiriveirabuca999@gmail.com','$2b$12$/70GGVbBEi0GozH0blAoI.MxqEddGryfu51LrOd.lTM1KYaBrUqg6',0,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(29,'Bautista','Riveira','bauti@admin.com','$2b$12$8e173K/BzSLfYyxZAMrhgOkWSgGXxj5G88qKiEi3PVvx0knSV/gR6',1,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-25 00:29:00'),(30,'Bautista','Buca','bautibuca@gmail.com','$2b$12$AD3xko/6NqYykSfnzZTtO.yoa00hbm0.JWMD9Sh6GU6Eyu1Ti6DbC',0,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(31,'Viviana','Buca','vivibuca@gmail.com','$2b$12$.N2pEenVcCD/aOsZ6pEmoOyvJcno5JIw4cQ8Vy2do7LZj8lD3E7u2',0,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(32,'Pilar','Riveira','piliriveira@yahoo.com','$2b$12$QLwghwR5m/gE/LuWHmFLwetYNIHM4CQtyiwPot/ZXcEKYqDHRMkce',0,NULL,NULL,NULL,NULL,NULL,'2026-02-21 21:46:59','2026-02-23 00:54:34'),(33,'Guadalupe','Guerra','guadaguerra@gmail.com','$2b$12$8IREwF6P8XCuknhRWP6vQebjI35db9yNaVRTyWOTZXfu2/ZCF4Mc6',0,NULL,NULL,NULL,'45256306','2604265930','2026-02-22 14:34:20','2026-02-24 23:19:56'),(34,'Juan ','Carlo','juancarlo@gmail.com','$2b$12$7CYGiC67yCxPMBuq6G3/lOp63N/aldLdhhwr49vIfexfnfXeidpeq',0,NULL,NULL,NULL,NULL,NULL,'2026-02-24 21:28:19','2026-02-25 00:28:19');
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

-- Dump completed on 2026-02-25 22:36:56
