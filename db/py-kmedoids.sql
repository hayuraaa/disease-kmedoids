-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 07 Nov 2024 pada 11.09
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `py-kmedoids`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `data_bobot`
--

CREATE TABLE `data_bobot` (
  `id_data` int(11) NOT NULL,
  `id_kecamatan` int(11) NOT NULL,
  `id_kriteria` int(11) NOT NULL,
  `bobot` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `data_bobot`
--

INSERT INTO `data_bobot` (`id_data`, `id_kecamatan`, `id_kriteria`, `bobot`) VALUES
(1, 1, 1, 24),
(2, 1, 2, 19),
(3, 1, 3, 13),
(4, 2, 1, 11),
(5, 2, 2, 8),
(6, 2, 3, 10),
(7, 3, 1, 4),
(8, 3, 2, 6),
(9, 3, 3, 9),
(10, 4, 1, 5),
(11, 4, 2, 10),
(12, 4, 3, 4),
(13, 5, 1, 5),
(14, 5, 2, 2),
(15, 5, 3, 3),
(16, 6, 1, 2),
(17, 6, 2, 4),
(18, 6, 3, 3),
(19, 7, 1, 2),
(20, 7, 2, 2),
(21, 7, 3, 1),
(22, 8, 1, 7),
(23, 8, 2, 7),
(24, 8, 3, 9),
(25, 9, 1, 3),
(26, 9, 2, 3),
(27, 9, 3, 3),
(28, 10, 1, 3),
(29, 10, 2, 2),
(30, 10, 3, 7),
(31, 11, 1, 2),
(32, 11, 2, 7),
(33, 11, 3, 9),
(34, 12, 1, 19),
(35, 12, 2, 13),
(36, 12, 3, 19),
(37, 13, 1, 0),
(38, 13, 2, 1),
(39, 13, 3, 1),
(40, 14, 1, 1),
(41, 14, 2, 1),
(42, 14, 3, 0),
(43, 15, 1, 5),
(44, 15, 2, 3),
(45, 15, 3, 3),
(46, 16, 1, 4),
(47, 16, 2, 10),
(48, 16, 3, 2),
(49, 17, 1, 3),
(50, 17, 2, 2),
(51, 17, 3, 4),
(52, 18, 1, 19),
(53, 18, 2, 15),
(54, 18, 3, 15),
(55, 19, 1, 12),
(56, 19, 2, 16),
(57, 19, 3, 10),
(58, 20, 1, 5),
(59, 20, 2, 12),
(60, 20, 3, 11),
(61, 21, 1, 9),
(62, 21, 2, 7),
(63, 21, 3, 12),
(64, 22, 1, 1),
(65, 22, 2, 3),
(66, 22, 3, 5),
(67, 23, 1, 3),
(68, 23, 2, 1),
(69, 23, 3, 3),
(70, 24, 1, 0),
(71, 24, 2, 2),
(72, 24, 3, 2),
(73, 25, 1, 2),
(74, 25, 2, 7),
(75, 25, 3, 3),
(76, 26, 1, 5),
(77, 26, 2, 0),
(78, 26, 3, 4),
(79, 27, 1, 6),
(80, 27, 2, 4),
(81, 27, 3, 4),
(82, 28, 1, 7),
(83, 28, 2, 5),
(84, 28, 3, 8),
(85, 29, 1, 22),
(86, 29, 2, 13),
(87, 29, 3, 10),
(88, 30, 1, 4),
(89, 30, 2, 0),
(90, 30, 3, 2),
(91, 31, 1, 1),
(92, 31, 2, 4),
(93, 31, 3, 1),
(94, 32, 1, 1),
(95, 32, 2, 3),
(96, 32, 3, 1),
(97, 33, 1, 2),
(98, 33, 2, 6),
(99, 33, 3, 5),
(100, 34, 1, 1),
(101, 34, 2, 2),
(102, 34, 3, 4),
(103, 35, 1, 11),
(104, 35, 2, 14),
(105, 35, 3, 14),
(106, 36, 1, 4),
(107, 36, 2, 7),
(108, 36, 3, 5),
(109, 37, 1, 3),
(110, 37, 2, 6),
(111, 37, 3, 12),
(112, 38, 1, 4),
(113, 38, 2, 5),
(114, 38, 3, 11),
(115, 39, 1, 6),
(116, 39, 2, 4),
(117, 39, 3, 5),
(118, 40, 1, 1),
(119, 40, 2, 4),
(120, 40, 3, 0),
(121, 41, 1, 6),
(122, 41, 2, 4),
(123, 41, 3, 4),
(124, 42, 1, 9),
(125, 42, 2, 4),
(126, 42, 3, 9),
(127, 43, 1, 4),
(128, 43, 2, 3),
(129, 43, 3, 3),
(130, 44, 1, 10),
(131, 44, 2, 6),
(132, 44, 3, 4),
(133, 45, 1, 9),
(134, 45, 2, 16),
(135, 45, 3, 5),
(136, 46, 1, 15),
(137, 46, 2, 13),
(138, 46, 3, 8),
(139, 47, 1, 2),
(140, 47, 2, 3),
(141, 47, 3, 3),
(142, 48, 1, 6),
(143, 48, 2, 2),
(144, 48, 3, 4),
(145, 49, 1, 3),
(146, 49, 2, 2),
(147, 49, 3, 4),
(148, 50, 1, 3),
(149, 50, 2, 2),
(150, 50, 3, 2),
(151, 51, 1, 4),
(152, 51, 2, 5),
(153, 51, 3, 7),
(154, 52, 1, 25),
(155, 52, 2, 24),
(156, 52, 3, 20),
(157, 53, 1, 10),
(158, 53, 2, 12),
(159, 53, 3, 14),
(160, 54, 1, 10),
(161, 54, 2, 12),
(162, 54, 3, 8),
(163, 55, 1, 7),
(164, 55, 2, 12),
(165, 55, 3, 12),
(166, 56, 1, 3),
(167, 56, 2, 3),
(168, 56, 3, 3),
(169, 57, 1, 1),
(170, 57, 2, 2),
(171, 57, 3, 2),
(172, 58, 1, 1),
(173, 58, 2, 1),
(174, 58, 3, 1),
(175, 59, 1, 7),
(176, 59, 2, 1),
(177, 59, 3, 4),
(178, 60, 1, 5),
(179, 60, 2, 1),
(180, 60, 3, 3),
(181, 61, 1, 2),
(182, 61, 2, 3),
(183, 61, 3, 1),
(184, 62, 1, 10),
(185, 62, 2, 2),
(186, 62, 3, 6),
(187, 63, 1, 10),
(188, 63, 2, 16),
(189, 63, 3, 17),
(190, 64, 1, 3),
(191, 64, 2, 1),
(192, 64, 3, 2),
(193, 65, 1, 2),
(194, 65, 2, 2),
(195, 65, 3, 2),
(196, 66, 1, 2),
(197, 66, 2, 4),
(198, 66, 3, 2),
(199, 67, 1, 1),
(200, 67, 2, 3),
(201, 67, 3, 1),
(202, 68, 1, 1),
(203, 68, 2, 1),
(204, 68, 3, 2),
(205, 69, 1, 17),
(206, 69, 2, 14),
(207, 69, 3, 12),
(208, 70, 1, 9),
(209, 70, 2, 11),
(210, 70, 3, 9),
(211, 71, 1, 7),
(212, 71, 2, 7),
(213, 71, 3, 6),
(214, 72, 1, 12),
(215, 72, 2, 14),
(216, 72, 3, 7),
(217, 73, 1, 6),
(218, 73, 2, 1),
(219, 73, 3, 7),
(220, 74, 1, 2),
(221, 74, 2, 2),
(222, 74, 3, 3),
(223, 75, 1, 1),
(224, 75, 2, 4),
(225, 75, 3, 5),
(226, 76, 1, 3),
(227, 76, 2, 4),
(228, 76, 3, 8),
(229, 77, 1, 2),
(230, 77, 2, 4),
(231, 77, 3, 6),
(232, 78, 1, 2),
(233, 78, 2, 1),
(234, 78, 3, 4),
(235, 79, 1, 5),
(236, 79, 2, 6),
(237, 79, 3, 6),
(238, 80, 1, 21),
(239, 80, 2, 20),
(240, 80, 3, 11),
(241, 81, 1, 2),
(242, 81, 2, 1),
(243, 81, 3, 1),
(244, 82, 1, 1),
(245, 82, 2, 2),
(246, 82, 3, 4),
(247, 83, 1, 1),
(248, 83, 2, 3),
(249, 83, 3, 4),
(250, 84, 1, 5),
(251, 84, 2, 5),
(252, 84, 3, 2),
(253, 85, 1, 4),
(254, 85, 2, 1),
(255, 85, 3, 5);

-- --------------------------------------------------------

--
-- Struktur dari tabel `jenis_penyakit`
--

CREATE TABLE `jenis_penyakit` (
  `id_jenis` int(11) NOT NULL,
  `nama_jenis` varchar(100) NOT NULL,
  `inisial_tindak` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `jenis_penyakit`
--

INSERT INTO `jenis_penyakit` (`id_jenis`, `nama_jenis`, `inisial_tindak`) VALUES
(1, 'Stroke', 'X1'),
(2, 'Hipertensi', 'X2'),
(3, 'Skizopernia', 'X3'),
(4, 'Dyspepsia', 'X4'),
(5, 'Pneumonia', 'X5');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kecamatan`
--

CREATE TABLE `kecamatan` (
  `id_kecamatan` int(11) NOT NULL,
  `id_jenis` int(11) NOT NULL,
  `nama_kecamatan` varchar(100) NOT NULL,
  `inisial_kecamatan` varchar(100) NOT NULL,
  `latitude` decimal(10,6) DEFAULT NULL,
  `longitude` decimal(10,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kecamatan`
--

INSERT INTO `kecamatan` (`id_kecamatan`, `id_jenis`, `nama_kecamatan`, `inisial_kecamatan`, `latitude`, `longitude`) VALUES
(1, 1, 'Kota Juang', 'Kota Juang', 5.200037, 96.707686),
(2, 1, 'Jeumpa', 'Jeumpa', 5.163875, 96.652630),
(3, 1, 'Kuala', 'Kuala', 5.235612, 96.715703),
(4, 1, 'Juli', 'Juli', 5.113103, 96.688283),
(5, 1, 'Jeunieb', 'Jeunieb', 5.164819, 96.485626),
(6, 1, 'Peulimbang', 'Peulimbang', 5.185718, 96.539495),
(7, 1, 'Pandrah', 'Pandrah', 5.171632, 96.455889),
(8, 1, 'Peudada', 'Peudada', 5.189604, 96.608847),
(9, 1, 'Samalanga', 'Samalanga', 5.181163, 96.358011),
(10, 1, 'Simpang Mamplam', 'Simpang Mamplam', 5.186143, 96.416700),
(11, 1, 'Jangka', 'Jangka', 5.251282, 96.776527),
(12, 1, 'Peusangan', 'Peusangan', 5.200250, 96.766801),
(13, 1, 'Peusangan Selatan', 'Peusangan Selatan', 5.141150, 96.770459),
(14, 1, 'Peusangan Siblah Krueng', 'Peusangan Siblah Krueng', 5.158873, 96.816739),
(15, 1, 'Makmur', 'Makmur', 5.175225, 96.872030),
(16, 1, 'Kuta Blang', 'Kuta Blang', 5.216826, 96.831735),
(17, 1, 'Gandapura', 'Gandapura', 5.232569, 96.892660),
(18, 2, 'Kota Juang', 'Kota Juang', 5.200037, 96.707686),
(19, 2, 'Jeumpa', 'Jeumpa', 5.163875, 96.652630),
(20, 2, 'Kuala', 'Kuala', 5.235612, 96.715703),
(21, 2, 'Juli', 'Juli', 5.113103, 96.688283),
(22, 2, 'Jeunieb', 'Jeunieb', 5.164819, 96.485626),
(23, 2, 'Peulimbang', 'Peulimbang', 5.185718, 96.539495),
(24, 2, 'Pandrah', 'Pandrah', 5.171632, 96.455889),
(25, 2, 'Peudada', 'Peudada', 5.189604, 96.608847),
(26, 2, 'Samalanga', 'Samalanga', 5.181163, 96.358011),
(27, 2, 'Simpang Mamplam', 'Simpang Mamplam', 5.186143, 96.416700),
(28, 2, 'Jangka', 'Jangka', 5.251282, 96.776527),
(29, 2, 'Peusangan', 'Peusangan', 5.200250, 96.766801),
(30, 2, 'Peusangan Selatan', 'Peusangan Selatan', 5.141150, 96.770459),
(31, 2, 'Peusangan Siblah Krueng', 'Peusangan Siblah Krueng', 5.158873, 96.816739),
(32, 2, 'Makmur', 'Makmur', 5.175225, 96.872030),
(33, 2, 'Kuta Blang', 'Kuta Blang', 5.216826, 96.831735),
(34, 2, 'Gandapura', 'Gandapura', 5.232569, 96.892660),
(35, 3, 'Kota Juang', 'Kota Juang', 5.200037, 96.707686),
(36, 3, 'Jeumpa', 'Jeumpa', 5.163875, 96.652630),
(37, 3, 'Kuala', 'Kuala', 5.235612, 96.715703),
(38, 3, 'Juli', 'Juli', 5.113103, 96.688283),
(39, 3, 'Jeunieb', 'Jeunieb', 5.164819, 96.485626),
(40, 3, 'Peulimbang', 'Peulimbang', 5.185718, 96.539495),
(41, 3, 'Pandrah', 'Pandrah', 5.171632, 96.455889),
(42, 3, 'Peudada', 'Peudada', 5.189604, 96.608847),
(43, 3, 'Samalanga', 'Samalanga', 5.181163, 96.358011),
(44, 3, 'Simpang Mamplam', 'Simpang Mamplam', 5.186143, 96.416700),
(45, 3, 'Jangka', 'Jangka', 5.251282, 96.776527),
(46, 3, 'Peusangan', 'Peusangan', 5.200250, 96.766801),
(47, 3, 'Peusangan Selatan', 'Peusangan Selatan', 5.141150, 96.770459),
(48, 3, 'Peusangan Siblah Krueng', 'Peusangan Siblah Krueng', 5.158873, 96.816739),
(49, 3, 'Makmur', 'Makmur', 5.175225, 96.872030),
(50, 3, 'Kuta Blang', 'Kuta Blang', 5.216826, 96.831735),
(51, 3, 'Gandapura', 'Gandapura', 5.232569, 96.892660),
(52, 4, 'Kota Juang', 'Kota Juang', 5.200037, 96.707686),
(53, 4, 'Jeumpa', 'Jeumpa', 5.163875, 96.652630),
(54, 4, 'Kuala', 'Kuala', 5.235612, 96.715703),
(55, 4, 'Juli', 'Juli', 5.113103, 96.688283),
(56, 4, 'Jeunieb', 'Jeunieb', 5.164819, 96.485626),
(57, 4, 'Peulimbang', 'Peulimbang', 5.185718, 96.539495),
(58, 4, 'Pandrah', 'Pandrah', 5.171632, 96.455889),
(59, 4, 'Peudada', 'Peudada', 5.189604, 96.608847),
(60, 4, 'Samalanga', 'Samalanga', 5.181163, 96.358011),
(61, 4, 'Simpang Mamplam', 'Simpang Mamplam', 5.186143, 96.416700),
(62, 4, 'Jangka', 'Jangka', 5.251282, 96.776527),
(63, 4, 'Peusangan', 'Peusangan', 5.200250, 96.766801),
(64, 4, 'Peusangan Selatan', 'Peusangan Selatan', 5.141150, 96.770459),
(65, 4, 'Peusangan Siblah Krueng', 'Peusangan Siblah Krueng', 5.158873, 96.816739),
(66, 4, 'Makmur', 'Makmur', 5.175225, 96.872030),
(67, 4, 'Kuta Blang', 'Kuta Blang', 5.216826, 96.831735),
(68, 4, 'Gandapura', 'Gandapura', 5.232569, 96.892660),
(69, 5, 'Kota Juang', 'Kota Juang', 5.200037, 96.707686),
(70, 5, 'Jeumpa', 'Jeumpa', 5.163875, 96.652630),
(71, 5, 'Kuala', 'Kuala', 5.235612, 96.715703),
(72, 5, 'Juli', 'Juli', 5.113103, 96.688283),
(73, 5, 'Jeunieb', 'Jeunieb', 5.164819, 96.485626),
(74, 5, 'Peulimbang', 'Peulimbang', 5.185718, 96.539495),
(75, 5, 'Pandrah', 'Pandrah', 5.171632, 96.455889),
(76, 5, 'Peudada', 'Peudada', 5.189604, 96.608847),
(77, 5, 'Samalanga', 'Samalanga', 5.181163, 96.358011),
(78, 5, 'Simpang Mamplam', 'Simpang Mamplam', 5.186143, 96.416700),
(79, 5, 'Jangka', 'Jangka', 5.251282, 96.776527),
(80, 5, 'Peusangan', 'Peusangan', 5.200250, 96.766801),
(81, 5, 'Peusangan Selatan', 'Peusangan Selatan', 5.141150, 96.770459),
(82, 5, 'Peusangan Siblah Krueng', 'Peusangan Siblah Krueng', 5.158873, 96.816739),
(83, 5, 'Makmur', 'Makmur', 5.175225, 96.872030),
(84, 5, 'Kuta Blang', 'Kuta Blang', 5.216826, 96.831735),
(85, 5, 'Gandapura', 'Gandapura', 5.232569, 96.892660);

-- --------------------------------------------------------

--
-- Struktur dari tabel `kriteria`
--

CREATE TABLE `kriteria` (
  `id_kriteria` int(11) NOT NULL,
  `nama_kriteria` varchar(100) NOT NULL,
  `inisial_kriteria` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kriteria`
--

INSERT INTO `kriteria` (`id_kriteria`, `nama_kriteria`, `inisial_kriteria`) VALUES
(1, '2021', 'X1'),
(2, '2022', 'X2'),
(3, '2023', 'X3');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `nama_user` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id_user`, `nama_user`, `username`, `password`) VALUES
(3, 'admin', 'admin', 'admin'),
(6, 'yaya', 'yaya', 'yaya');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `data_bobot`
--
ALTER TABLE `data_bobot`
  ADD PRIMARY KEY (`id_data`);

--
-- Indeks untuk tabel `jenis_penyakit`
--
ALTER TABLE `jenis_penyakit`
  ADD PRIMARY KEY (`id_jenis`);

--
-- Indeks untuk tabel `kecamatan`
--
ALTER TABLE `kecamatan`
  ADD PRIMARY KEY (`id_kecamatan`);

--
-- Indeks untuk tabel `kriteria`
--
ALTER TABLE `kriteria`
  ADD PRIMARY KEY (`id_kriteria`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `data_bobot`
--
ALTER TABLE `data_bobot`
  MODIFY `id_data` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=256;

--
-- AUTO_INCREMENT untuk tabel `jenis_penyakit`
--
ALTER TABLE `jenis_penyakit`
  MODIFY `id_jenis` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT untuk tabel `kecamatan`
--
ALTER TABLE `kecamatan`
  MODIFY `id_kecamatan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=86;

--
-- AUTO_INCREMENT untuk tabel `kriteria`
--
ALTER TABLE `kriteria`
  MODIFY `id_kriteria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
