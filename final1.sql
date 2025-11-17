-- ======================================================
--   RESET COMPLETO DE LA BASE DE DATOS RBE
-- ======================================================

DROP DATABASE IF EXISTS RBE;
CREATE DATABASE RBE;
USE RBE;

-- ======================================================
--   TABLAS BASE
-- ======================================================

CREATE TABLE marca (
    numero INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

CREATE TABLE conductor (
    registro INT PRIMARY KEY,
    conNombre VARCHAR(30) NOT NULL,
    conPrimerApell VARCHAR(30) NOT NULL,
    conSegundoApell VARCHAR(30),
    licNumero VARCHAR(15) NOT NULL,
    licVencimiento DATE NOT NULL,
    fechaContrato DATE NOT NULL
);

CREATE TABLE ciudad (
    clave VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

CREATE TABLE tipo_asiento (
    codigo VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE tipo_pasajero (
    num INT PRIMARY KEY,
    descuento INT NOT NULL,
    descripcion VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE tipo_pago (
    numero INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE edo_viaje (
    numero INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(50) NOT NULL
);

CREATE TABLE pasajero (
    num INT PRIMARY KEY AUTO_INCREMENT,
    paNombre VARCHAR(30) NOT NULL,
    paPrimerApell VARCHAR(30) NOT NULL,
    paSegundoApell VARCHAR(30),
    fechaNacimiento DATE NOT NULL,
    edad INT
);

CREATE TABLE modelo (
    numero INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    numAsientos INT NOT NULL,
    año INT NOT NULL,
    capacidad INT NOT NULL,
    marca INT NOT NULL,
    FOREIGN KEY (marca) REFERENCES marca(numero)
);

CREATE TABLE terminal (
    numero INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    dirCalle VARCHAR(30) NOT NULL,
    dirNumero VARCHAR(10) NOT NULL,
    dirColonia VARCHAR(30) NOT NULL,
    ciudad VARCHAR(5) NOT NULL,
    FOREIGN KEY (ciudad) REFERENCES ciudad(clave)
);

-- RUTA incluye precio base
CREATE TABLE ruta (
    codigo INT PRIMARY KEY,
    duracion VARCHAR(10) NOT NULL,
    origen INT NOT NULL,
    destino INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL DEFAULT 250,
    FOREIGN KEY (origen) REFERENCES terminal(numero),
    FOREIGN KEY (destino) REFERENCES terminal(numero)
);

CREATE TABLE autobus (
    numero INT PRIMARY KEY,
    modelo INT NOT NULL,
    placas VARCHAR(10) NOT NULL UNIQUE,
    serieVIN VARCHAR(17) NOT NULL UNIQUE,
    FOREIGN KEY (modelo) REFERENCES modelo(numero)
);

CREATE TABLE viaje (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    fecHoraSalida DATETIME NOT NULL,
    fecHoraEntrada DATETIME NOT NULL,
    ruta INT NOT NULL,
    estado INT NOT NULL,
    autobus INT NOT NULL,
    conductor INT NOT NULL,
    FOREIGN KEY (ruta) REFERENCES ruta(codigo),
    FOREIGN KEY (estado) REFERENCES edo_viaje(numero),
    FOREIGN KEY (autobus) REFERENCES autobus(numero),
    FOREIGN KEY (conductor) REFERENCES conductor(registro)
);

CREATE TABLE asiento (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(5) NOT NULL,
    autobus INT NOT NULL,
    FOREIGN KEY (tipo) REFERENCES tipo_asiento(codigo),
    FOREIGN KEY (autobus) REFERENCES autobus(numero)
);

CREATE TABLE viaje_asiento (
    asiento INT NOT NULL,
    viaje INT NOT NULL,
    ocupado BOOLEAN NOT NULL,
    PRIMARY KEY (asiento, viaje),
    FOREIGN KEY (asiento) REFERENCES asiento(numero),
    FOREIGN KEY (viaje) REFERENCES viaje(numero)
);

CREATE TABLE taquillero (
    registro INT PRIMARY KEY AUTO_INCREMENT,
    taqNombre VARCHAR(30) NOT NULL,
    taqPrimerApell VARCHAR(30) NOT NULL,
    taqSegundoApell VARCHAR(30),
    fechaContrato DATE NOT NULL,
    usuario VARCHAR(20) NOT NULL,
    contraseña VARCHAR(20) NOT NULL,
    terminal INT NOT NULL,
    FOREIGN KEY (terminal) REFERENCES terminal(numero)
);

CREATE TABLE pago (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    fechapago DATETIME NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    tipo INT NOT NULL,
    vendedor INT NOT NULL,
    FOREIGN KEY (tipo) REFERENCES tipo_pago(numero),
    FOREIGN KEY (vendedor) REFERENCES taquillero(registro)
);

CREATE TABLE ticket (
    codigo INT PRIMARY KEY AUTO_INCREMENT,
    precio DECIMAL(10,2) NOT NULL,
    fechaEmision DATETIME NOT NULL,
    asiento INT NOT NULL,
    viaje INT NOT NULL,
    pasajero INT NOT NULL,
    tipopasajero INT NOT NULL,
    pago INT NOT NULL,
    FOREIGN KEY (asiento) REFERENCES asiento(numero),
    FOREIGN KEY (viaje) REFERENCES viaje(numero),
    FOREIGN KEY (pasajero) REFERENCES pasajero(num),
    FOREIGN KEY (tipopasajero) REFERENCES tipo_pasajero(num),
    FOREIGN KEY (pago) REFERENCES pago(numero)
);

-- ======================================================
--   DATOS DE PRUEBA
-- ======================================================

-- Ciudades (Baja California)
INSERT INTO ciudad VALUES
('TIJ', 'Tijuana'),
('MXL', 'Mexicali'),
('ENS', 'Ensenada');

-- Terminales
INSERT INTO terminal VALUES
(1, 'Terminal Tijuana', 'Av Revolución', '100', 'Centro', 'TIJ'),
(2, 'Terminal Mexicali', 'Calzada Independencia', '200', 'Centro', 'MXL'),
(3, 'Terminal Ensenada', 'Blvd Costero', '300', 'Playa', 'ENS');

-- Tipos asiento/pasajero/pago y estados
INSERT INTO tipo_asiento VALUES
('NOR', 'Normal'),
('PRE', 'Premium');

INSERT INTO tipo_pasajero VALUES
(1, 0, 'Adulto'),
(2, 50, 'Estudiante'),
(3, 30, 'INAPAM');

INSERT INTO tipo_pago VALUES
(1, 'Efectivo', 'Pago en efectivo'),
(2, 'Tarjeta', 'Pago con tarjeta bancaria');

INSERT INTO edo_viaje VALUES
(1, 'Programado', 'Viaje aún no inicia'),
(2, 'En curso', 'Viaje en progreso'),
(3, 'Finalizado', 'Viaje terminado');

-- Conductores
INSERT INTO conductor VALUES
(100, 'Luis', 'Rojas', 'Lopez', 'LIC12345', '2027-05-10', '2020-01-01'),
(101, 'Marcos', 'Pérez', 'Hernandez', 'LIC56433', '2026-11-20', '2019-03-14');

-- Marcas y modelos
INSERT INTO marca VALUES 
(1, 'Mercedes-Benz'),
(2, 'Volvo'),
(3, 'Scania');

INSERT INTO modelo VALUES
(1, 'Modelo 2022', 40, 2022, 5000, 1),
(2, 'Modelo 2021', 50, 2021, 6000, 2);

-- Autobuses
INSERT INTO autobus VALUES
(10, 1, 'ABC1234', '1A2B3C4D5E6F7G8H1'),
(11, 2, 'XYZ9876', '9H8G7F6E5D4C3B2A1');

-- Asientos generados por autobús
INSERT INTO asiento (tipo, autobus)
SELECT 'NOR', 10 FROM (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) a,
(SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4) b
LIMIT 40;

INSERT INTO asiento (tipo, autobus)
SELECT 'NOR', 11 FROM (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10) a,
(SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) b
LIMIT 50;

-- Rutas con precio base (Baja California)
INSERT INTO ruta (codigo, duracion, origen, destino, precio) VALUES
(1, '02:30', 1, 2, 450.00),   -- Tijuana → Mexicali
(2, '02:30', 2, 1, 450.00),   -- Mexicali → Tijuana
(3, '01:45', 1, 3, 300.00),   -- Tijuana → Ensenada
(4, '01:45', 3, 1, 300.00),   -- Ensenada → Tijuana
(5, '03:00', 2, 3, 400.00),   -- Mexicali → Ensenada
(6, '03:00', 3, 2, 400.00);   -- Ensenada → Mexicali

-- Viajes (referencian rutas y autobuses válidos)
INSERT INTO viaje (fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
('2025-01-10 08:00:00', '2025-01-10 10:30:00', 1, 1, 10, 100),
('2025-01-11 08:00:00', '2025-01-11 10:30:00', 2, 1, 11, 101),
('2025-01-12 09:00:00', '2025-01-12 10:45:00', 3, 1, 10, 100),
('2025-01-12 12:00:00', '2025-01-12 13:45:00', 4, 1, 11, 101);

-- Taquilleros
INSERT INTO taquillero (registro, taqNombre, taqPrimerApell, taqSegundoApell, fechaContrato, usuario, contraseña, terminal) VALUES
(200, 'Miguel', 'Vargas', 'Lopez', '2022-05-10', 'miquel', '1234', 1),
(201, 'Lucia', 'Nava', NULL, '2023-07-15', 'lucia', 'abcd', 2);

-- Pasajeros
INSERT INTO pasajero (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad) VALUES
('Carlos', 'Martinez', 'Lopez', '1990-05-10', 34),
('Ana', 'Soto', NULL, '2001-10-21', 23);

-- Inicializar viaje_asiento para los viajes creados (asigna todos los asientos del autobús al viaje, como disponibles)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT a.numero, v.numero, 0
FROM asiento a
JOIN viaje v ON a.autobus = v.autobus
WHERE v.numero IN (1, 2, 3, 4);

-- Pagos de prueba
INSERT INTO pago (fechapago, monto, tipo, vendedor) VALUES
('2025-01-05 10:00:00', 450.00, 1, 200),
('2025-01-05 10:05:00', 300.00, 2, 201);

-- Tickets de prueba (asientos reales deben existir en esos autobuses)
-- Para viaje 1 (autobús 10), asiento 1 y 2 existen por la generación de 40 asientos
INSERT INTO ticket (precio, fechaEmision, asiento, viaje, pasajero, tipopasajero, pago) VALUES
(450.00, '2025-01-05 10:00:00', 1, 1, 1, 1, 1),
(300.00, '2025-01-05 10:05:00', 2, 1, 2, 2, 2);

-- Marcar ocupados esos asientos en viaje_asiento
UPDATE viaje_asiento SET ocupado = 1 WHERE viaje = 1 AND asiento IN (1, 2);
