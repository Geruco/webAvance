-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 22, 2022 at 02:05 AM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `webavance`
--

-- --------------------------------------------------------

--
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
CREATE TABLE IF NOT EXISTS `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `date_publication` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_revision` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `userId` int(11) NOT NULL,
  `statut` int(1) NOT NULL DEFAULT '0' COMMENT '0 = brouillon, 1= publié',
  PRIMARY KEY (`id`),
  KEY `FK_User` (`userId`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `article`
--

INSERT INTO `article` (`id`, `title`, `content`, `date_publication`, `date_revision`, `userId`, `statut`) VALUES
(10, 'Article de base', 'Contenu de l\'article de base', '2022-03-22 01:54:05', '2022-03-22 01:53:59', 1, 1),
(11, 'Je test un titre', 'jsfanfkjsnafkjnfs', '2022-03-22 02:00:32', '2022-03-22 02:00:12', 12, 1);

-- --------------------------------------------------------

--
-- Table structure for table `commentary`
--

DROP TABLE IF EXISTS `commentary`;
CREATE TABLE IF NOT EXISTS `commentary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `userId` int(11) NOT NULL,
  `articleId` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Article` (`articleId`),
  KEY `FK_User` (`userId`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `commentary`
--

INSERT INTO `commentary` (`id`, `text`, `date`, `userId`, `articleId`) VALUES
(3, 'dsadsads', '2022-03-22 02:00:39', 12, 11);

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
CREATE TABLE IF NOT EXISTS `profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`id`, `name`) VALUES
(1, 'Administrator'),
(3, 'Reader'),
(2, 'Author');

-- --------------------------------------------------------

--
-- Table structure for table `reaction`
--

DROP TABLE IF EXISTS `reaction`;
CREATE TABLE IF NOT EXISTS `reaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `icone` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reaction`
--

INSERT INTO `reaction` (`id`, `description`, `icone`) VALUES
(1, 'like', 'fa-thumbs-up'),
(2, 'circle-check', 'fa-circle-check');

-- --------------------------------------------------------

--
-- Table structure for table `reactionarticle`
--

DROP TABLE IF EXISTS `reactionarticle`;
CREATE TABLE IF NOT EXISTS `reactionarticle` (
  `articleId` int(11) NOT NULL,
  `reactionId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`articleId`,`reactionId`,`userId`),
  KEY `reactionId` (`reactionId`),
  KEY `userId` (`userId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reactionarticle`
--

INSERT INTO `reactionarticle` (`articleId`, `reactionId`, `userId`) VALUES
(6, 17, 1),
(6, 18, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tag`
--

INSERT INTO `tag` (`id`, `name`) VALUES
(1, 'Code'),
(2, 'MySQL'),
(3, 'Fun'),
(4, 'Culture'),
(5, 'Lays'),
(6, '7Up'),
(7, 'Refresh');

-- --------------------------------------------------------

--
-- Table structure for table `tagarticle`
--

DROP TABLE IF EXISTS `tagarticle`;
CREATE TABLE IF NOT EXISTS `tagarticle` (
  `articleId` int(11) NOT NULL,
  `tagId` int(11) NOT NULL,
  PRIMARY KEY (`articleId`,`tagId`),
  KEY `FK_Tag` (`tagId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tagarticle`
--

INSERT INTO `tagarticle` (`articleId`, `tagId`) VALUES
(1, 1),
(1, 2),
(10, 1),
(10, 2),
(11, 1),
(11, 4);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `profileId` int(11) NOT NULL DEFAULT '3',
  PRIMARY KEY (`id`),
  KEY `FK_Profile` (`profileId`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `first_name`, `last_name`, `email`, `profileId`) VALUES
(1, 'admin', '$5$rounds=535000$rKvOnB57rTLRhkj.$qdrvFBLX0aU.9ztd3xGcZMzNFJOGZ8kO5/xY8iH5gO5', 'admin', 'admin', 'admin@gmail.com', 1),
(12, 'test', '$5$rounds=535000$QK3.yP9fitA36Rjw$b0qvZOl0z1NLR3H/RkIbtEq0HkpgLcWugV/O3Bgk364', 'test', 'test', 'test', 2),
(11, 'lecteur', '$5$rounds=535000$zY/DpO5wPUpHTZ/Y$3483BG2BVq0Qef.kTSvCfvh5moo8KCJ/pevXNvJ/Yi2', 'lecteur', 'lecteur', 'lecteur', 3);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
