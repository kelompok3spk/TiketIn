-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 24, 2025 at 04:57 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db-tiketin-app`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `nama_admin` varchar(100) NOT NULL,
  `email_admin` varchar(100) NOT NULL,
  `no_telp_admin` varchar(15) DEFAULT NULL,
  `password_admin` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `nama_admin`, `email_admin`, `no_telp_admin`, `password_admin`) VALUES
(1, 'Farah', 'farahdina@gmail.com', '08766253426', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
(2, 'Rani', 'rani@gmail.com', '098654321678', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

-- --------------------------------------------------------

--
-- Table structure for table `pemesanan`
--

CREATE TABLE `pemesanan` (
  `id_pemesanan` int(11) NOT NULL,
  `id_pengguna` int(11) DEFAULT NULL,
  `id_tempat` int(11) DEFAULT NULL,
  `nama_pengguna` varchar(25) NOT NULL,
  `email_pengguna` varchar(100) NOT NULL,
  `jumlah_orang` int(11) NOT NULL,
  `nama_tempat` varchar(100) NOT NULL,
  `lokasi_tempat` varchar(100) NOT NULL,
  `tgl_pemesanan` date NOT NULL,
  `harga_per_orang` int(11) NOT NULL,
  `nomor_hp` varchar(15) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pemesanan`
--

INSERT INTO `pemesanan` (`id_pemesanan`, `id_pengguna`, `id_tempat`, `nama_pengguna`, `email_pengguna`, `jumlah_orang`, `nama_tempat`, `lokasi_tempat`, `tgl_pemesanan`, `harga_per_orang`, `nomor_hp`, `status`) VALUES
(14318564, NULL, 1, 'jana', 'jana123@gmail.com', 1, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2024-11-07', 15000, '097512357912', 'lunas'),
(24790893, NULL, 1, 'Tia Tini', 'tiatini@gmail.com', 2, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2024-11-07', 15000, '089753612346', 'lunas'),
(29454200, NULL, 1, 'Nisa', 'nisa@gmail.com', 2, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2024-11-07', 15000, '0876541234', 'lunas'),
(32762200, NULL, 1, 'Farelli', 'farelli@gmail.com', 2, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2024-11-12', 15000, '085100', 'lunas'),
(37167846, NULL, 2, 'awaneka', 'awaneka@gmail.com', 1, 'THE LAWU PARK', 'Bulakrejo, Gondosuli Kidul, Gondosuli, Kec. Tawangmangu, Kabupaten Karanganyar, Jawa Tengah 57792', '2024-11-08', 20000, '098783936762', 'lunas'),
(39336539, NULL, 1, 'jana', 'jana123@gmail.com', 1, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2024-11-07', 15000, '097512357912', 'lunas'),
(45952142, NULL, 1, 'awaneka', 'awaneka@gmail.com', 2, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2024-11-11', 15000, '0876541234', 'lunas'),
(47935726, NULL, 11, 'Tata Ratu', 'tataratu@gmail.com', 2, 'The Heritage Palace', 'Jln. Permata Raya Dukuh Tegal Mulyo rt.002/rw.008, Honggobayan, Pabelan, Kec. Kartasura, Kabupaten S', '2024-11-09', 35000, '087654367854', 'lunas'),
(52537527, NULL, 2, 'Tia Tini', 'tiatini@gmail.com', 2, 'THE LAWU PARK', 'Bulakrejo, Gondosuli Kidul, Gondosuli, Kec. Tawangmangu, Kabupaten Karanganyar, Jawa Tengah 57792', '2024-11-07', 20000, '089753612346', 'lunas'),
(64543897, NULL, 5, 'Tes', 'email@email.com', 2, 'Museum Batik Danar Hadi', 'Sriwedari, Laweyan, Surakarta', '2024-11-05', 35000, '08123456789', 'lunas'),
(64543898, NULL, 1, 'Tes 1', 'email1@email.com', 3, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2024-11-05', 15000, '08123456780', 'lunas'),
(64543899, NULL, 2, 'Tes 2', 'email2@email.com', 2, 'Pasar Klewer', 'Gajahan, Pasar Kliwon, Surakarta', '2024-11-03', 0, '08123456781', 'lunas'),
(64543900, NULL, 3, 'Tes 3', 'email3@email.com', 5, 'Taman Balekambang', 'Manahan, Banjarsari, Surakarta', '2024-11-03', 5000, '08123456782', 'lunas'),
(64543901, NULL, 4, 'Tes 4', 'email4@email.com', 1, 'Kampung Batik Kauman', 'Kauman, Pasar Kliwon, Surakarta', '2024-11-01', 0, '08123456783', 'lunas'),
(64543902, NULL, 6, 'Tes 5', 'email5@email.com', 4, 'Pura Mangkunegaran', 'Keprabon, Banjarsari, Surakarta', '2024-11-01', 20000, '08123456784', 'lunas'),
(74150413, NULL, 2, 'Dwi', 'dwi123@gmail.com', 2, 'THE LAWU PARK', 'Bulakrejo, Gondosuli Kidul, Gondosuli, Kec. Tawangmangu, Kabupaten Karanganyar, Jawa Tengah 57792', '2024-11-07', 20000, '087641325676', 'lunas'),
(98280833, NULL, 1, 'jana', 'jana123@gmail.com', 1, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2025-06-10', 15000, '097512357912', 'lunas'),
(98520682, NULL, 1, 'awaneka', 'awaneka@gmail.com', 2, 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', '2024-11-09', 15000, '0876541234', 'lunas');

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `id_pengguna` int(11) NOT NULL,
  `nama_pengguna` varchar(100) NOT NULL,
  `email_pengguna` varchar(100) NOT NULL,
  `no_telp_pengguna` varchar(15) DEFAULT NULL,
  `password_pengguna` varchar(255) NOT NULL,
  `is_blocked` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengguna`
--

INSERT INTO `pengguna` (`id_pengguna`, `nama_pengguna`, `email_pengguna`, `no_telp_pengguna`, `password_pengguna`, `is_blocked`) VALUES
(17, 'Yuni', 'yuni123@gmail.com', '087512345678', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tempat_wisata`
--

CREATE TABLE `tempat_wisata` (
  `id_tempat` int(11) NOT NULL,
  `image` varchar(255) NOT NULL,
  `nama_tempat` varchar(100) NOT NULL,
  `lokasi_tempat` varchar(100) NOT NULL,
  `harga_per_orang` decimal(10,2) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `rating` decimal(2,1) NOT NULL DEFAULT 0.0,
  `jam_buka` varchar(50) NOT NULL,
  `hari_buka` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tempat_wisata`
--

INSERT INTO `tempat_wisata` (`id_tempat`, `image`, `nama_tempat`, `lokasi_tempat`, `harga_per_orang`, `deskripsi`, `rating`, `jam_buka`, `hari_buka`) VALUES
(1, 'static/uploads/Keraton-Surakarta.webp', 'Keraton Surakarta Hadiningrat', 'Baluwarti, Pasar Kliwon, Surakarta', 15000.00, 'Keraton Surakarta Hadiningrat adalah istana resmi Kasunanan Surakarta yang menampilkan arsitektur tradisional Jawa dan berbagai koleksi peninggalan sejarah kerajaan.', 4.5, '09:00 - 14:00', 'Senin - Kamis'),
(2, 'static/uploads/1lawu.jpg', 'THE LAWU PARK', 'Bulakrejo, Gondosuli Kidul, Gondosuli, Kec. Tawangmangu, Kabupaten Karanganyar, Jawa Tengah 57792', 20000.00, 'Resor gunung dengan kelinci & domba, jalan setapak di atas pohon & zona salju, plus kabin simpel.', 4.6, '08:00 - 17:00', 'Setiap Hari'),
(3, '/static/uploads/objek-wisata-taman-balekambang-solo-2.jpg', 'Taman Balekambang', 'Manahan, Banjarsari, Surakarta', 5000.00, 'Taman Balekambang adalah taman kota yang asri, cocok untuk rekreasi keluarga dengan fasilitas seperti area bermain anak dan danau buatan.', 4.5, '06:00 - 18:00', 'Setiap Hari'),
(4, 'static/uploads/snapinstaapp-278878164-1339014909934625-2667693909324945276-n-1080-143a5a7f3f0e039e1473818cd7fd17ae-ceb4d89d9aca9b6a0317729825378d87_600x400.jpg', 'Kampung Batik Kauman', 'Kauman, Pasar Kliwon, Surakarta', 0.00, 'Kampung Batik Kauman adalah sentra industri batik di Solo, di mana pengunjung dapat melihat proses pembuatan batik dan membeli produk langsung dari pengrajin.', 4.2, '08:00 - 17:00', 'Senin - Sabtu'),
(5, 'static/uploads/Museum-of-Batik-Danar-Hadi.jpg', 'Museum Batik Danar Hadi', 'Sriwedari, Laweyan, Surakarta', 35000.00, 'Museum Batik Danar Hadi menampilkan koleksi batik dari berbagai daerah di Indonesia, memberikan wawasan mendalam tentang sejarah dan perkembangan batik.', 4.6, '09:00 - 16:30', 'Senin - Sabtu'),
(6, 'static/uploads/3343809363.jpg', 'Pura Mangkunegaran', 'Keprabon, Banjarsari, Surakarta', 20000.00, 'Pura Mangkunegaran adalah istana resmi Kadipaten Mangkunegaran dengan arsitektur khas Jawa dan koleksi seni yang bernilai tinggi.', 4.5, '09:00 - 15:00', 'Senin - Minggu'),
(7, 'static/uploads/TAMAN-SRIWEDARI-SOLO-1024x683.jpg', 'Taman Sriwedari', 'Sriwedari, Laweyan, Surakarta', 3000.00, 'Taman Sriwedari adalah kompleks pertamanan yang sering digunakan untuk pertunjukan seni dan budaya, serta tempat rekreasi bagi warga Solo.', 4.1, '10:00 - 22:00', 'Setiap Hari'),
(8, 'static/uploads/2a56631c-990f-424f-bee9-e021c302e5ff-3355463219.webp', 'Museum Keris Nusantara', 'Sriwedari, Laweyan, Surakarta', 10000.00, 'Museum Keris Nusantara menampilkan berbagai koleksi keris dari seluruh Indonesia, memberikan wawasan tentang senjata tradisional dan budaya keris.', 4.3, '08:00 - 16:00', 'Selasa - Minggu'),
(11, 'static/uploads/heritagejpeg.jpeg', 'The Heritage Palace', 'Jln. Permata Raya Dukuh Tegal Mulyo rt.002/rw.008, Honggobayan, Pabelan, Kec. Kartasura, Kabupaten S', 35000.00, 'Museum The Heritage Palace merupakan destinasi wisata bersejarah di\r\nKabupaten Sukoharjo yang dulunya ialah bangunan bekas dari pabrik gula yang\r\ndirevitalisasikan. Museum The Heritage Palace dikelola oleh PT , konsep\r\nbangunannya yang unik membuat Museum The Heritage Palace memiliki daya\r\ntarik tersendiri di mata wisatawan, selain itu bangunan bersejarah ini sudah resmi\r\ndijadikan Bangunan Cagar Budaya oleh pemerintah setempat. Selain dari konsep\r\nbangunannya yang unik, Museum The Heritage Palace memiliki daya tarik wisata\r\nlain yang patut dikembangkan seperti pameran mobil antik dan lukisan 3D\r\nArtnya. Penelitian ini menggunakan metode kualitatif dengan teknik analisis\r\nSWOT agar dapat mementukan strategi yang dapat dikembangkan untuk menarik\r\nminat wisatawan dalam berkunjung ke Museum The Heritage Palace.', 4.6, '08.00-16.00', 'Senin-Minggu'),
(12, 'static/uploads/candi_sukuh.jpg', 'Candi Sukuh', 'Tambak, Berjo, Kec. Ngargoyoso, Kabupaten Karanganyar, Jawa Tengah 57793', 15000.00, 'Candi Sukuh adalah sebuah kompleks candi Hindu yang secara administrasi terletak di wilayah Desa Berjo, Kecamatan Ngargoyoso, Kabupaten Karanganyar, Jawa Tengah.', 4.5, '08.00-16.00', 'Senin-Minggu'),
(13, 'static/uploads/tenggir1.webp', 'tenggir park', ' Tambak, Berjo, Kec. Ngargoyoso, Kabupaten Karanganyar, Jawa Tengah 57793', 10.00, '\r\nTenggir Park menyediakan beragam spot foto, seperti taman bunga, spot sepeda, rumah pohon, spot rumah honai, \r\nspot ranjang layang, air terjun bidadari, kolam renang, hingga permadani atau karpet terbang. \r\nTenggir Park merupakan kawasan yang tergolong masih baru,', 0.7, '08.00-16.00', 'Senin-Minggu');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `email_admin` (`email_admin`);

--
-- Indexes for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD PRIMARY KEY (`id_pemesanan`),
  ADD KEY `id_pengguna` (`id_pengguna`),
  ADD KEY `id_tempat` (`id_tempat`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`id_pengguna`),
  ADD UNIQUE KEY `email_pengguna` (`email_pengguna`);

--
-- Indexes for table `tempat_wisata`
--
ALTER TABLE `tempat_wisata`
  ADD PRIMARY KEY (`id_tempat`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `pemesanan`
--
ALTER TABLE `pemesanan`
  MODIFY `id_pemesanan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=98520683;

--
-- AUTO_INCREMENT for table `pengguna`
--
ALTER TABLE `pengguna`
  MODIFY `id_pengguna` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `tempat_wisata`
--
ALTER TABLE `tempat_wisata`
  MODIFY `id_tempat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD CONSTRAINT `pemesanan_ibfk_1` FOREIGN KEY (`id_pengguna`) REFERENCES `pengguna` (`id_pengguna`),
  ADD CONSTRAINT `pemesanan_ibfk_2` FOREIGN KEY (`id_tempat`) REFERENCES `tempat_wisata` (`id_tempat`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
