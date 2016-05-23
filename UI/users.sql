-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: May 22, 2016 at 12:39 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `users`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `trn_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `trn_date`) VALUES
(1, 'A', 'A@A.com', '7fc56270e7a70fa81a5935b72eacbe29', '2016-05-10 14:56:02'),
(2, 'B', 'B@B.com', '9d5ed678fe57bcca610140957afab571', '2016-05-10 14:59:23'),
(3, 'C', 'C@C.com', '0d61f8370cad1d412f80b84d143e1257', '2016-05-10 14:59:46'),
(4, 'D', 'D@D.com', 'f623e75af30e62bbd73d6df5b50bb7b5', '2016-05-10 15:00:08'),
(5, 'E', 'E@E.com', '3a3ea00cfc35332cedf6e5e9a32e94da', '2016-05-10 15:00:33'),
(6, 'F', 'F@F.com', '800618943025315f869e4e1f09471012', '2016-05-10 15:01:52'),
(7, 'G', 'G@G.com', 'dfcf28d0734569a6a693bc8194de62bf', '2016-05-10 15:02:10'),
(8, 'H', 'H@H.com', 'c1d9f50f86825a1a2302ec2449c17196', '2016-05-10 15:02:35'),
(9, 'I', 'I@I.com', 'dd7536794b63bf90eccfd37f9b147d7f', '2016-05-10 15:02:49'),
(10, 'J', 'J@J.com', 'ff44570aca8241914870afbc310cdb85', '2016-05-10 15:03:08');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
