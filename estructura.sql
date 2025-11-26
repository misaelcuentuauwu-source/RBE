-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 26, 2025 at 05:41 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `rbe`
--

-- --------------------------------------------------------

--
-- Table structure for table `asiento`
--

CREATE TABLE `asiento` (
  `numero` int(11) NOT NULL,
  `tipo` varchar(5) NOT NULL,
  `autobus` int(11) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `autobus`
--

CREATE TABLE `autobus` (
  `numero` int(11) NOT NULL,
  `modelo` int(11) NOT NULL,
  `placas` varchar(10) NOT NULL,
  `serieVIN` varchar(17) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `ciudad`
--

CREATE TABLE `ciudad` (
  `clave` varchar(5) NOT NULL,
  `nombre` varchar(30) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `conductor`
--

CREATE TABLE `conductor` (
  `registro` int(11) NOT NULL,
  `conNombre` varchar(30) NOT NULL,
  `conPrimerApell` varchar(30) NOT NULL,
  `conSegundoApell` varchar(30) DEFAULT NULL,
  `licNumero` varchar(15) NOT NULL,
  `licVencimiento` date NOT NULL,
  `fechaContrato` date NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `edo_viaje`
--

CREATE TABLE `edo_viaje` (
  `numero` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `descripcion` varchar(50) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `marca`
--

CREATE TABLE `marca` (
  `numero` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `modelo`
--

CREATE TABLE `modelo` (
  `numero` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `numasientos` int(11) NOT NULL,
  `año` int(11) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `marca` int(11) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `pago`
--

CREATE TABLE `pago` (
  `numero` int(11) NOT NULL,
  `fechapago` datetime NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `tipo` int(11) NOT NULL,
  `vendedor` int(11) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `pasajero`
--

CREATE TABLE `pasajero` (
  `num` int(11) NOT NULL,
  `paNombre` varchar(30) NOT NULL,
  `paPrimerApell` varchar(30) NOT NULL,
  `paSegundoApell` varchar(30) DEFAULT NULL,
  `fechaNacimiento` date NOT NULL,
  `edad` int(11) DEFAULT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `ruta`
--

CREATE TABLE `ruta` (
  `codigo` int(11) NOT NULL,
  `duracion` varchar(10) NOT NULL,
  `origen` int(11) NOT NULL,
  `destino` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL DEFAULT 250.00
);

-- --------------------------------------------------------

--
-- Table structure for table `taquillero`
--

CREATE TABLE `taquillero` (
  `registro` int(11) NOT NULL,
  `taqNombre` varchar(30) NOT NULL,
  `taqPrimerApell` varchar(30) NOT NULL,
  `taqSegundoApell` varchar(30) DEFAULT NULL,
  `fechaContrato` date NOT NULL,
  `usuario` varchar(20) NOT NULL,
  `contraseña` varchar(20) NOT NULL,
  `terminal` int(11) NOT NULL,
  `supervisa` tinyint(1) DEFAULT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `terminal`
--

CREATE TABLE `terminal` (
  `numero` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `dirCalle` varchar(30) NOT NULL,
  `dirNumero` varchar(10) NOT NULL,
  `dirColonia` varchar(30) NOT NULL,
  `telefono` varchar(12) DEFAULT NULL,
  `ciudad` varchar(5) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `codigo` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `fechaEmision` datetime NOT NULL,
  `asiento` int(11) NOT NULL,
  `viaje` int(11) NOT NULL,
  `pasajero` int(11) NOT NULL,
  `tipopasajero` int(11) NOT NULL,
  `pago` int(11) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `tipo_asiento`
--

CREATE TABLE `tipo_asiento` (
  `codigo` varchar(5) NOT NULL,
  `descripcion` varchar(30) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `tipo_pago`
--

CREATE TABLE `tipo_pago` (
  `numero` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `descripcion` varchar(50) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `tipo_pasajero`
--

CREATE TABLE `tipo_pasajero` (
  `num` int(11) NOT NULL,
  `descuento` int(11) NOT NULL,
  `descripcion` varchar(30) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `viaje`
--

CREATE TABLE `viaje` (
  `numero` int(11) NOT NULL,
  `fecHoraSalida` datetime NOT NULL,
  `fecHoraEntrada` datetime NOT NULL,
  `ruta` int(11) NOT NULL,
  `estado` int(11) NOT NULL,
  `autobus` int(11) DEFAULT NULL,
  `conductor` int(11) DEFAULT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `viaje_asiento`
--

CREATE TABLE `viaje_asiento` (
  `asiento` int(11) NOT NULL,
  `viaje` int(11) NOT NULL,
  `ocupado` tinyint(1) NOT NULL
);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `asiento`
--
ALTER TABLE `asiento`
  ADD PRIMARY KEY (`numero`),
  ADD KEY `tipo` (`tipo`),
  ADD KEY `autobus` (`autobus`);

--
-- Indexes for table `autobus`
--
ALTER TABLE `autobus`
  ADD PRIMARY KEY (`numero`),
  ADD UNIQUE KEY `placas` (`placas`),
  ADD UNIQUE KEY `serieVIN` (`serieVIN`),
  ADD KEY `modelo` (`modelo`);

--
-- Indexes for table `ciudad`
--
ALTER TABLE `ciudad`
  ADD PRIMARY KEY (`clave`);

--
-- Indexes for table `conductor`
--
ALTER TABLE `conductor`
  ADD PRIMARY KEY (`registro`);

--
-- Indexes for table `edo_viaje`
--
ALTER TABLE `edo_viaje`
  ADD PRIMARY KEY (`numero`);

--
-- Indexes for table `marca`
--
ALTER TABLE `marca`
  ADD PRIMARY KEY (`numero`);

--
-- Indexes for table `modelo`
--
ALTER TABLE `modelo`
  ADD PRIMARY KEY (`numero`),
  ADD KEY `marca` (`marca`);

--
-- Indexes for table `pago`
--
ALTER TABLE `pago`
  ADD PRIMARY KEY (`numero`),
  ADD KEY `tipo` (`tipo`),
  ADD KEY `vendedor` (`vendedor`);

--
-- Indexes for table `pasajero`
--
ALTER TABLE `pasajero`
  ADD PRIMARY KEY (`num`);

--
-- Indexes for table `ruta`
--
ALTER TABLE `ruta`
  ADD PRIMARY KEY (`codigo`),
  ADD KEY `origen` (`origen`),
  ADD KEY `destino` (`destino`);

--
-- Indexes for table `taquillero`
--
ALTER TABLE `taquillero`
  ADD PRIMARY KEY (`registro`),
  ADD KEY `terminal` (`terminal`);

--
-- Indexes for table `terminal`
--
ALTER TABLE `terminal`
  ADD PRIMARY KEY (`numero`),
  ADD KEY `ciudad` (`ciudad`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`codigo`),
  ADD KEY `asiento` (`asiento`),
  ADD KEY `viaje` (`viaje`),
  ADD KEY `pasajero` (`pasajero`),
  ADD KEY `tipopasajero` (`tipopasajero`),
  ADD KEY `pago` (`pago`);

--
-- Indexes for table `tipo_asiento`
--
ALTER TABLE `tipo_asiento`
  ADD PRIMARY KEY (`codigo`),
  ADD UNIQUE KEY `descripcion` (`descripcion`);

--
-- Indexes for table `tipo_pago`
--
ALTER TABLE `tipo_pago`
  ADD PRIMARY KEY (`numero`),
  ADD UNIQUE KEY `descripcion` (`descripcion`);

--
-- Indexes for table `tipo_pasajero`
--
ALTER TABLE `tipo_pasajero`
  ADD PRIMARY KEY (`num`),
  ADD UNIQUE KEY `descripcion` (`descripcion`);

--
-- Indexes for table `viaje`
--
ALTER TABLE `viaje`
  ADD PRIMARY KEY (`numero`),
  ADD KEY `ruta` (`ruta`),
  ADD KEY `estado` (`estado`),
  ADD KEY `autobus` (`autobus`),
  ADD KEY `conductor` (`conductor`);

--
-- Indexes for table `viaje_asiento`
--
ALTER TABLE `viaje_asiento`
  ADD PRIMARY KEY (`asiento`,`viaje`),
  ADD KEY `viaje` (`viaje`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `asiento`
--
ALTER TABLE `asiento`
  MODIFY `numero` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pago`
--
ALTER TABLE `pago`
  MODIFY `numero` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pasajero`
--
ALTER TABLE `pasajero`
  MODIFY `num` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `taquillero`
--
ALTER TABLE `taquillero`
  MODIFY `registro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ticket`
--
ALTER TABLE `ticket`
  MODIFY `codigo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `viaje`
--
ALTER TABLE `viaje`
  MODIFY `numero` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `asiento`
--
ALTER TABLE `asiento`
  ADD CONSTRAINT `asiento_ibfk_1` FOREIGN KEY (`tipo`) REFERENCES `tipo_asiento` (`codigo`),
  ADD CONSTRAINT `asiento_ibfk_2` FOREIGN KEY (`autobus`) REFERENCES `autobus` (`numero`);

--
-- Constraints for table `autobus`
--
ALTER TABLE `autobus`
  ADD CONSTRAINT `autobus_ibfk_1` FOREIGN KEY (`modelo`) REFERENCES `modelo` (`numero`);

--
-- Constraints for table `modelo`
--
ALTER TABLE `modelo`
  ADD CONSTRAINT `modelo_ibfk_1` FOREIGN KEY (`marca`) REFERENCES `marca` (`numero`);

--
-- Constraints for table `pago`
--
ALTER TABLE `pago`
  ADD CONSTRAINT `pago_ibfk_1` FOREIGN KEY (`tipo`) REFERENCES `tipo_pago` (`numero`),
  ADD CONSTRAINT `pago_ibfk_2` FOREIGN KEY (`vendedor`) REFERENCES `taquillero` (`registro`);

--
-- Constraints for table `ruta`
--
ALTER TABLE `ruta`
  ADD CONSTRAINT `ruta_ibfk_1` FOREIGN KEY (`origen`) REFERENCES `terminal` (`numero`),
  ADD CONSTRAINT `ruta_ibfk_2` FOREIGN KEY (`destino`) REFERENCES `terminal` (`numero`);

--
-- Constraints for table `taquillero`
--
ALTER TABLE `taquillero`
  ADD CONSTRAINT `taquillero_ibfk_1` FOREIGN KEY (`terminal`) REFERENCES `terminal` (`numero`);

--
-- Constraints for table `terminal`
--
ALTER TABLE `terminal`
  ADD CONSTRAINT `terminal_ibfk_1` FOREIGN KEY (`ciudad`) REFERENCES `ciudad` (`clave`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`asiento`) REFERENCES `asiento` (`numero`),
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`viaje`) REFERENCES `viaje` (`numero`),
  ADD CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`pasajero`) REFERENCES `pasajero` (`num`),
  ADD CONSTRAINT `ticket_ibfk_4` FOREIGN KEY (`tipopasajero`) REFERENCES `tipo_pasajero` (`num`),
  ADD CONSTRAINT `ticket_ibfk_5` FOREIGN KEY (`pago`) REFERENCES `pago` (`numero`);

--
-- Constraints for table `viaje`
--
ALTER TABLE `viaje`
  ADD CONSTRAINT `viaje_ibfk_1` FOREIGN KEY (`ruta`) REFERENCES `ruta` (`codigo`),
  ADD CONSTRAINT `viaje_ibfk_2` FOREIGN KEY (`estado`) REFERENCES `edo_viaje` (`numero`),
  ADD CONSTRAINT `viaje_ibfk_3` FOREIGN KEY (`autobus`) REFERENCES `autobus` (`numero`),
  ADD CONSTRAINT `viaje_ibfk_4` FOREIGN KEY (`conductor`) REFERENCES `conductor` (`registro`);

--
-- Constraints for table `viaje_asiento`
--
ALTER TABLE `viaje_asiento`
  ADD CONSTRAINT `viaje_asiento_ibfk_1` FOREIGN KEY (`asiento`) REFERENCES `asiento` (`numero`),
  ADD CONSTRAINT `viaje_asiento_ibfk_2` FOREIGN KEY (`viaje`) REFERENCES `viaje` (`numero`);
COMMIT;