-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 19, 2023 at 12:13 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `deteksi_katarak`
--

-- --------------------------------------------------------

--
-- Table structure for table `datapendertakatarak`
--

CREATE TABLE `datapendertakatarak` (
  `id` int(25) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `nik` varchar(50) NOT NULL,
  `tangal_lahir` varchar(80) NOT NULL,
  `pekerjaan` varchar(50) NOT NULL,
  `Log` date NOT NULL DEFAULT current_timestamp(),
  `kelamin` varchar(255) NOT NULL,
  `hasil_deteksi` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `datapendertakatarak`
--

INSERT INTO `datapendertakatarak` (`id`, `nama`, `nik`, `tangal_lahir`, `pekerjaan`, `Log`, `kelamin`, `hasil_deteksi`) VALUES
(101, 'RIZKI PUTRA UTAMA ENDRIANSYAH', '23432423', '2023-09-03', 'SOPIR', '2023-09-19', 'Laki Laki', 'normal'),
(102, 'RIZKI PUTRA UTAMA ENDRIANSYAH', '23432423', '2023-09-20', 'petani', '2023-09-19', 'Laki Laki', 'katarak'),
(103, 'RIZKI PUTRA', '23432423', '2023-09-03', 'petani', '2023-09-19', 'Perempuan', 'kualitas gambar kurang bagus edit!'),
(104, 'RIZKI PUTRA UTAMA ENDRIANSYAH', '23432423', '2023-09-28', 'buruh', '2023-09-19', 'Perempuan', 'katarak'),
(105, 'RIZKI PUTRA', '23432423', '2023-09-11', 'buruh', '2023-09-19', 'Laki Laki', 'katarak'),
(106, 'RIZKI PUTRA UTAMA ENDRIANSYAH', '23432423', '2023-09-18', 'SOPIR', '2023-09-19', 'Laki Laki', 'katarak');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `datapendertakatarak`
--
ALTER TABLE `datapendertakatarak`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
