-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server Version:               10.5.12-MariaDB-0ubuntu0.21.04.1 - Ubuntu 21.04
-- Server Betriebssystem:        debian-linux-gnu
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Exportiere Datenbank Struktur für bug-free-waffle
CREATE DATABASE IF NOT EXISTS `bug-free-waffle-dev` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `bug-free-waffle-dev`;

-- Exportiere Struktur von Tabelle bug-free-waffle.reviews
CREATE TABLE IF NOT EXISTS `reviews` (
  `servername` varchar(50) NOT NULL DEFAULT '',
  `revtext` varchar(400) DEFAULT NULL,
  `dcuserid` varchar(45) DEFAULT NULL,
  `revat` timestamp(6) NULL DEFAULT NULL,
  `serverid` int(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Tabelle bug-free-waffle.servers
CREATE TABLE IF NOT EXISTS `servers` (
  `servername` varchar(45) DEFAULT NULL,
  `serverurl` varchar(45) DEFAULT NULL,
  `discordserverid` varchar(45) DEFAULT NULL,
  `server_text` varchar(2000) DEFAULT NULL,
  `registered_by` varchar(45) DEFAULT NULL,
  `votes` int(11) DEFAULT NULL,
  `serverid` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`serverid`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4;

-- Daten Export vom Benutzer nicht ausgewählt

-- Exportiere Struktur von Tabelle bug-free-waffle.user_votes
CREATE TABLE IF NOT EXISTS `user_votes` (
  `dcuserid` varchar(50) DEFAULT '',
  `voted` varchar(50) DEFAULT NULL,
  `voted_time` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Daten Export vom Benutzer nicht ausgewählt

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
