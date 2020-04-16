-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 16, 2020 at 11:51 PM
-- Server version: 5.7.29-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mi_transport`
--
CREATE DATABASE IF NOT EXISTS `mi_transport` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `mi_transport`;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `Customer_Key` char(5) NOT NULL,
  `Customer_Name` varchar(20) NOT NULL,
  `Customer_Gender` char(1) DEFAULT NULL,
  `Customer_Address` varchar(120) NOT NULL,
  `Customer_District` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`Customer_Key`, `Customer_Name`, `Customer_Gender`, `Customer_Address`, `Customer_District`) VALUES
('1001', 'Edmond', 'M', 'Shan Tin', 'New Territories'),
('1004', 'Fong Wai', 'M', 'Hong Kong Is', 'Hong Kong Is'),
('1005', 'Leo Ling', 'M', 'North Point', 'Hong Kong Is');

-- --------------------------------------------------------

--
-- Table structure for table `order_item`
--

CREATE TABLE `order_item` (
  `Order_Key` char(5) NOT NULL,
  `Item_Key` char(5) NOT NULL,
  `Item_Name` varchar(20) NOT NULL,
  `Item_Description` varchar(200) NOT NULL,
  `Item_Type` varchar(15) NOT NULL,
  `Item_Brand` varchar(15) NOT NULL,
  `Item_Size` varchar(10) NOT NULL,
  `Item_Cost` decimal(5,0) NOT NULL,
  `Item_Price` decimal(5,0) NOT NULL,
  `Item_Quantity` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order_item`
--

INSERT INTO `order_item` (`Order_Key`, `Item_Key`, `Item_Name`, `Item_Description`, `Item_Type`, `Item_Brand`, `Item_Size`, `Item_Cost`, `Item_Price`, `Item_Quantity`) VALUES
('2001', '3001', 'RedMi 3S', 'RedMi 3S', 'Redmi Phone', 'Xiao Mi', '24 24', '2', '1700', 10000),
('2002', '3002', 'Xiao Mi Note 4X', 'Xiao Mi Note 4X', 'Xiao Mi Phone', 'Xiao Mi', '24 24', '4000', '4100', 10000),
('2002', '3003', 'RedMi Note 4X', 'RedMi Note 4X', 'RedMi Phone', 'RedMi', '24 24', '1400', '1500', 1500);

-- --------------------------------------------------------

--
-- Table structure for table `purchase_order`
--

CREATE TABLE `purchase_order` (
  `Order_Key` char(5) NOT NULL,
  `Customer_Key` char(5) NOT NULL,
  `Order_Date` date NOT NULL,
  `Order_Count` int(5) NOT NULL,
  `Order_Total` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `purchase_order`
--

INSERT INTO `purchase_order` (`Order_Key`, `Customer_Key`, `Order_Date`, `Order_Count`, `Order_Total`) VALUES
('2002', '1004', '2020-01-23', 2, 2),
('2003', '1001', '2020-04-14', 4, 4);

-- --------------------------------------------------------

--
-- Table structure for table `xcustomer`
--

CREATE TABLE `xcustomer` (
  `Customer_Key` char(5) NOT NULL,
  `Customer_Name` varchar(20) NOT NULL,
  `Customer_Gender` char(1) DEFAULT NULL,
  `Customer_Address` varchar(120) NOT NULL,
  `Customer_District` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xcustomer`
--

INSERT INTO `xcustomer` (`Customer_Key`, `Customer_Name`, `Customer_Gender`, `Customer_Address`, `Customer_District`) VALUES
('1001', 'Edmond', 'M', 'Shan Tin', 'New Territories'),
('1004', 'Fong Wai', 'M', 'Hong Kong Is', 'Hong Kong Is'),
('1005', 'Leo Ling', 'M', 'North Point', 'Hong Kong Is');

-- --------------------------------------------------------

--
-- Table structure for table `xorder_item`
--

CREATE TABLE `xorder_item` (
  `Order_Key` char(5) NOT NULL,
  `Item_Key` char(5) NOT NULL,
  `Item_Name` varchar(20) NOT NULL,
  `Item_Description` varchar(200) NOT NULL,
  `Item_Type` varchar(15) NOT NULL,
  `Item_Brand` varchar(15) NOT NULL,
  `Item_Size` varchar(10) NOT NULL,
  `Item_Cost` decimal(5,0) NOT NULL,
  `Item_Price` decimal(5,0) NOT NULL,
  `Item_Quantity` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xorder_item`
--

INSERT INTO `xorder_item` (`Order_Key`, `Item_Key`, `Item_Name`, `Item_Description`, `Item_Type`, `Item_Brand`, `Item_Size`, `Item_Cost`, `Item_Price`, `Item_Quantity`) VALUES
('2001', '3001', 'RedMi 3S', 'RedMi 3S', 'Redmi Phone', 'Xiao Mi', '24 24', '2', '1700', 10000),
('2002', '3002', 'Xiao Mi Note 4X', 'Xiao Mi Note 4X', 'Xiao Mi Phone', 'Xiao Mi', '24 24', '4000', '4100', 10000),
('2002', '3003', 'RedMi Note 4X', 'RedMi Note 4X', 'RedMi Phone', 'RedMi', '24 24', '1400', '1500', 1500);

-- --------------------------------------------------------

--
-- Table structure for table `xpurchase_order`
--

CREATE TABLE `xpurchase_order` (
  `Order_Key` char(5) NOT NULL,
  `Customer_Key` char(5) NOT NULL,
  `Order_Date` date NOT NULL,
  `Order_Count` int(5) NOT NULL,
  `Order_Total` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xpurchase_order`
--

INSERT INTO `xpurchase_order` (`Order_Key`, `Customer_Key`, `Order_Date`, `Order_Count`, `Order_Total`) VALUES
('2002', '1004', '2020-01-23', 2, 2),
('2003', '1001', '2020-04-14', 4, 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`Customer_Key`);

--
-- Indexes for table `purchase_order`
--
ALTER TABLE `purchase_order`
  ADD PRIMARY KEY (`Order_Key`);

--
-- Indexes for table `xcustomer`
--
ALTER TABLE `xcustomer`
  ADD PRIMARY KEY (`Customer_Key`);

--
-- Indexes for table `xpurchase_order`
--
ALTER TABLE `xpurchase_order`
  ADD PRIMARY KEY (`Order_Key`);
--
-- Database: `sf_transport`
--
CREATE DATABASE IF NOT EXISTS `sf_transport` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `sf_transport`;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `Customer_Key` char(5) NOT NULL,
  `Customer_Name` varchar(20) NOT NULL,
  `Customer_Gender` char(1) DEFAULT NULL,
  `Customer_Address` varchar(120) NOT NULL,
  `Customer_District` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`Customer_Key`, `Customer_Name`, `Customer_Gender`, `Customer_Address`, `Customer_District`) VALUES
('1001', 'Edmond', 'M', 'Shan Tin', 'New Territories'),
('1004', 'Fong Wai', 'M', 'Hong Kong Is', 'Hong Kong Is'),
('1005', 'Leo Ling', 'M', 'North Point', 'Hong Kong Is');

-- --------------------------------------------------------

--
-- Table structure for table `order_item`
--

CREATE TABLE `order_item` (
  `Order_Key` char(5) NOT NULL,
  `Item_Key` char(5) NOT NULL,
  `Item_Name` varchar(20) NOT NULL,
  `Item_Description` varchar(200) NOT NULL,
  `Item_Type` varchar(15) NOT NULL,
  `Item_Brand` varchar(15) NOT NULL,
  `Item_Size` varchar(10) NOT NULL,
  `Item_Cost` decimal(5,0) NOT NULL,
  `Item_Price` decimal(5,0) NOT NULL,
  `Item_Quantity` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order_item`
--

INSERT INTO `order_item` (`Order_Key`, `Item_Key`, `Item_Name`, `Item_Description`, `Item_Type`, `Item_Brand`, `Item_Size`, `Item_Cost`, `Item_Price`, `Item_Quantity`) VALUES
('2001', '3001', 'RedMi 3S', 'RedMi 3S', 'Redmi Phone', 'Xiao Mi', '24 24', '2', '1700', 10000),
('2002', '3002', 'Xiao Mi Note 4X', 'Xiao Mi Note 4X', 'Xiao Mi Phone', 'Xiao Mi', '24 24', '4000', '4100', 10000),
('2002', '3003', 'RedMi Note 4X', 'RedMi Note 4X', 'RedMi Phone', 'RedMi', '24 24', '1400', '1500', 1500);

-- --------------------------------------------------------

--
-- Table structure for table `purchase_order`
--

CREATE TABLE `purchase_order` (
  `Order_Key` char(5) NOT NULL,
  `Customer_Key` char(5) NOT NULL,
  `Order_Date` date NOT NULL,
  `Order_Count` int(5) NOT NULL,
  `Order_Total` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `purchase_order`
--

INSERT INTO `purchase_order` (`Order_Key`, `Customer_Key`, `Order_Date`, `Order_Count`, `Order_Total`) VALUES
('2002', '1004', '2020-01-23', 2, 2),
('2003', '1001', '2020-04-14', 4, 4);

-- --------------------------------------------------------

--
-- Table structure for table `xcustomer`
--

CREATE TABLE `xcustomer` (
  `Customer_Key` char(5) NOT NULL,
  `Customer_Name` varchar(20) NOT NULL,
  `Customer_Gender` char(1) DEFAULT NULL,
  `Customer_Address` varchar(120) NOT NULL,
  `Customer_District` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xcustomer`
--

INSERT INTO `xcustomer` (`Customer_Key`, `Customer_Name`, `Customer_Gender`, `Customer_Address`, `Customer_District`) VALUES
('1001', 'Edmond', 'M', 'Shan Tin', 'New Territories'),
('1004', 'Fong Wai', 'M', 'Hong Kong Is', 'Hong Kong Is'),
('1005', 'Leo Ling', 'M', 'North Point', 'Hong Kong Is');

-- --------------------------------------------------------

--
-- Table structure for table `xorder_item`
--

CREATE TABLE `xorder_item` (
  `Order_Key` char(5) NOT NULL,
  `Item_Key` char(5) NOT NULL,
  `Item_Name` varchar(20) NOT NULL,
  `Item_Description` varchar(200) NOT NULL,
  `Item_Type` varchar(15) NOT NULL,
  `Item_Brand` varchar(15) NOT NULL,
  `Item_Size` varchar(10) NOT NULL,
  `Item_Cost` decimal(5,0) NOT NULL,
  `Item_Price` decimal(5,0) NOT NULL,
  `Item_Quantity` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xorder_item`
--

INSERT INTO `xorder_item` (`Order_Key`, `Item_Key`, `Item_Name`, `Item_Description`, `Item_Type`, `Item_Brand`, `Item_Size`, `Item_Cost`, `Item_Price`, `Item_Quantity`) VALUES
('2001', '3001', 'RedMi 3S', 'RedMi 3S', 'Redmi Phone', 'Xiao Mi', '24 24', '2', '1700', 10000),
('2002', '3002', 'Xiao Mi Note 4X', 'Xiao Mi Note 4X', 'Xiao Mi Phone', 'Xiao Mi', '24 24', '4000', '4100', 10000),
('2002', '3003', 'RedMi Note 4X', 'RedMi Note 4X', 'RedMi Phone', 'RedMi', '24 24', '1400', '1500', 1500);

-- --------------------------------------------------------

--
-- Table structure for table `xpurchase_order`
--

CREATE TABLE `xpurchase_order` (
  `Order_Key` char(5) NOT NULL,
  `Customer_Key` char(5) NOT NULL,
  `Order_Date` date NOT NULL,
  `Order_Count` int(5) NOT NULL,
  `Order_Total` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xpurchase_order`
--

INSERT INTO `xpurchase_order` (`Order_Key`, `Customer_Key`, `Order_Date`, `Order_Count`, `Order_Total`) VALUES
('2002', '1004', '2020-01-23', 2, 2),
('2003', '1001', '2020-04-14', 4, 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`Customer_Key`);

--
-- Indexes for table `purchase_order`
--
ALTER TABLE `purchase_order`
  ADD PRIMARY KEY (`Order_Key`);

--
-- Indexes for table `xcustomer`
--
ALTER TABLE `xcustomer`
  ADD PRIMARY KEY (`Customer_Key`);

--
-- Indexes for table `xpurchase_order`
--
ALTER TABLE `xpurchase_order`
  ADD PRIMARY KEY (`Order_Key`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
