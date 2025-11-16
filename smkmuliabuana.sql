-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 09 Nov 2025 pada 08.03
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
-- Database: `smkmuliabuana`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `absensi`
--

CREATE TABLE `absensi` (
  `id` int(11) NOT NULL,
  `siswa_id` int(11) NOT NULL,
  `guru_id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `status` enum('Hadir','Tidak Hadir','Sakit','Izin') NOT NULL,
  `mata_pelajaran_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `guru`
--

CREATE TABLE `guru` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `guru`
--

INSERT INTO `guru` (`id`, `nama`, `username`, `password`) VALUES
(6, 'Muhamad Nurdin S.Kom', 'Nurdin', '$2b$12$jPubWIrfu.jy.nr7nV2xKurmtZoUAtGyFzhmrLsJEsj.DGkI.S2fy'),
(8, 'Septian Handita Surya S.Kom', 'Septian', '$2b$12$KDSue7E29.BSzozobxL3Q.pJ1Is74pg8XWn9AXdQWWLm6VrTZtkPe'),
(9, 'Al Ghozi S.kom', 'Alghozi', '$2b$12$EH1Fm2tQzLd0WJQAASNHdef53TDFNtvIQllQMYqMP2XUxHxAJSCGK'),
(10, 'Agung Setyadi', 'Agung', '$2b$12$C2dNZwW4B57lJHQlRjpIv.PqQNJDn9AHCHiaeA.w2iI75PvV9Kq52'),
(11, 'asep racing', 'asep', '$2b$12$fL1qGdrnAkYtocEzIFKz4..ulx47LNsN3OhUKyWwQChiQ6qkNIgB6');

-- --------------------------------------------------------

--
-- Struktur dari tabel `jurusan`
--

CREATE TABLE `jurusan` (
  `id` int(11) NOT NULL,
  `nama_jurusan` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `jurusan`
--

INSERT INTO `jurusan` (`id`, `nama_jurusan`) VALUES
(1, 'TKJ 1'),
(3, 'TKJ 2'),
(4, 'TKJ 3'),
(5, 'TKJ 4'),
(6, 'TAV 1'),
(7, 'TAV 2'),
(8, 'TAV 3'),
(9, 'OTKP 1'),
(10, 'OTKP 2'),
(11, 'OTKP 3'),
(12, 'Akuntansi 1'),
(13, 'Akuntansi 2'),
(14, 'Akuntansi 3');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mata_pelajaran`
--

CREATE TABLE `mata_pelajaran` (
  `id` int(11) NOT NULL,
  `nama_mapel` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mata_pelajaran`
--

INSERT INTO `mata_pelajaran` (`id`, `nama_mapel`) VALUES
(2, 'Bahasa Indonesia'),
(3, 'Bahasa Inggris'),
(4, 'Matematika'),
(5, 'Ilmu Pengetahuan Alam'),
(6, 'Seni Budaya'),
(7, 'PPKn'),
(8, 'Kewirausahaan'),
(9, 'Sistem Operasi'),
(10, 'Pemrograman Dasar'),
(11, 'Komputer dan Jaringan Dasar'),
(12, 'Teknologi Layanan Jaringan'),
(13, 'Akuntansi Dasar'),
(14, 'Administrasi Pajak'),
(15, 'Komputer Akuntansi'),
(16, 'Pengantar Akuntansi');

-- --------------------------------------------------------

--
-- Struktur dari tabel `siswa`
--

CREATE TABLE `siswa` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `nisn` varchar(50) NOT NULL,
  `kelas` varchar(10) NOT NULL,
  `jurusan` varchar(50) NOT NULL,
  `mapel` varchar(100) NOT NULL,
  `nama_ortu` varchar(100) NOT NULL,
  `no_ortu` varchar(20) NOT NULL,
  `mapel_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `siswa`
--

INSERT INTO `siswa` (`id`, `nama`, `nisn`, `kelas`, `jurusan`, `mapel`, `nama_ortu`, `no_ortu`, `mapel_id`) VALUES
(11, 'Muhamad Nurdin', '251140008', '10', 'TKJ 1', '', 'Rusman', '6282126276388', 9),
(12, 'Muhammad Tafarel Akbar', '251140002', '10', 'TKJ 1', '', 'Farel', '6289637380130', 9),
(14, 'Muhammad Akbar Khadafi', '251140003', '10', 'Akuntansi 1', '', 'Akbar', '6282125243567', 14),
(15, 'Najwa Meyda', '251140001', '10', 'TKJ 1', '', 'Mey', '6282154327890', 6),
(16, 'Andi Ilham', '251140004', '10', 'TKJ 1', '', 'Andi', '6282143565432', 10),
(17, 'Muhammad Akhtar', '251140005', '10', 'TKJ 1', '', 'Akhtar', '6282134567654', 3),
(18, 'Al Ghozi', '251140007', '10', 'Akuntansi 1', '', 'Al', '6282125654356', 14),
(19, 'Prima Prayoga', '251140009', '10', 'TKJ 1', '', 'Prima', '6282125434532', 9),
(20, 'Agung Setyadi', '251140010', '10', 'Akuntansi 1', '', 'Agung', '6282167542345', 14),
(21, 'Septian Handita', '251140006', '10', 'TKJ 1', '', 'Handita', '6282112344321', 9),
(22, 'Bolang', '1445667', '11', 'TKJ 2', '', 'Oki', '6282123456543', 9);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `absensi`
--
ALTER TABLE `absensi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `siswa_id` (`siswa_id`),
  ADD KEY `guru_id` (`guru_id`),
  ADD KEY `fk_mata_pelajaran` (`mata_pelajaran_id`);

--
-- Indeks untuk tabel `guru`
--
ALTER TABLE `guru`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `jurusan`
--
ALTER TABLE `jurusan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `mata_pelajaran`
--
ALTER TABLE `mata_pelajaran`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `siswa`
--
ALTER TABLE `siswa`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nisn` (`nisn`),
  ADD KEY `fk_mapel` (`mapel_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `absensi`
--
ALTER TABLE `absensi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT untuk tabel `guru`
--
ALTER TABLE `guru`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT untuk tabel `jurusan`
--
ALTER TABLE `jurusan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT untuk tabel `mata_pelajaran`
--
ALTER TABLE `mata_pelajaran`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT untuk tabel `siswa`
--
ALTER TABLE `siswa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `absensi`
--
ALTER TABLE `absensi`
  ADD CONSTRAINT `absensi_ibfk_1` FOREIGN KEY (`siswa_id`) REFERENCES `siswa` (`id`),
  ADD CONSTRAINT `absensi_ibfk_2` FOREIGN KEY (`guru_id`) REFERENCES `guru` (`id`),
  ADD CONSTRAINT `fk_mata_pelajaran` FOREIGN KEY (`mata_pelajaran_id`) REFERENCES `mata_pelajaran` (`id`);

--
-- Ketidakleluasaan untuk tabel `siswa`
--
ALTER TABLE `siswa`
  ADD CONSTRAINT `fk_mapel` FOREIGN KEY (`mapel_id`) REFERENCES `mata_pelajaran` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
