-- Active: 1760978807635@@127.0.0.1@3306@prototipo
-- 🚫 1. Borrar base de datos anterior si existe
DROP DATABASE IF EXISTS prototipo;

-- 🆕 2. Crear base de datos nueva
CREATE DATABASE prototipo;
USE prototipo;

-- ==========================================
-- 🚌 SISTEMA DE TICKETS - MODELO RELACIONAL
-- Autor: Misael Urquidez Arredondo
-- ==========================================

-- 1️⃣ TABLAS BASE

CREATE TABLE ciudad (
    clave VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
) ENGINE=InnoDB;

INSERT INTO ciudad (clave, nombre) VALUES
('TJU','Tijuana'),
('ENS','Ensenada'),
('ROS','Rosarito'),
('TEC','Tecate'),
('MXL','Mexicali'),
('SFE','San Felipe');

CREATE TABLE modelo (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    numasientos INT NOT NULL,
    anio INT NOT NULL,
    cre INT NOT NULL,
    marca VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE edo_viaje (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE tipo_asientos (
    codigo VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(30) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE tipo_pasajero (
    num INT PRIMARY KEY AUTO_INCREMENT,
    descuento DECIMAL(5,2),
    descripcion VARCHAR(30) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE tipo_pago (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 2️⃣ TABLAS INTERMEDIAS

CREATE TABLE terminal (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    ternombre VARCHAR(30) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    ternumero VARCHAR(10) NOT NULL,
    tercalle VARCHAR(30) NOT NULL,
    tercolonia VARCHAR(30) NOT NULL,
    ciudad VARCHAR(5) NOT NULL,
    FOREIGN KEY (ciudad) REFERENCES ciudad(clave)
) ENGINE=InnoDB;

INSERT INTO terminal (ternombre, telefono, ternumero, tercalle, tercolonia, ciudad) VALUES
('Terminal Tijuana', '6641234567', '123', 'Revolución', 'Centro', 'TJU'),
('Terminal Ensenada', '6469876543', '456', 'Juárez', 'Valle Dorado', 'ENS'),
('Terminal Rosarito', '6611122334', '78', 'Héroes', 'Playas', 'ROS'),
('Terminal Tecate', '6655566778', '90', 'Independencia', 'Centro', 'TEC'),
('Terminal Mexicali', '6862233445', '321', 'Lázaro Cárdenas', 'Zona Centro', 'MXL'),
('Terminal San Felipe', '6869988776', '12', 'Marina', 'Pueblo Nuevo', 'SFE');

CREATE TABLE ruta (
    codigo INT PRIMARY KEY AUTO_INCREMENT,
    origen INT NOT NULL,
    destino INT NOT NULL,
    duracion VARCHAR(10) NOT NULL,
    FOREIGN KEY (origen) REFERENCES terminal(numero),
    FOREIGN KEY (destino) REFERENCES terminal(numero)
) ENGINE=InnoDB;

CREATE TABLE autobus (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    modelo INT NOT NULL,
    placas VARCHAR(10) NOT NULL UNIQUE,
    FOREIGN KEY (modelo) REFERENCES modelo(numero)
) ENGINE=InnoDB;

CREATE TABLE conductor (
    registro INT PRIMARY KEY AUTO_INCREMENT,
    connombre VARCHAR(30) NOT NULL,
    conprimerapell VARCHAR(30) NOT NULL,
    consegundoapell VARCHAR(30),
    licnumero VARCHAR(15) NOT NULL,
    licvencimiento DATE NOT NULL,
    fechacontrato DATE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE pasajero (
    num INT PRIMARY KEY AUTO_INCREMENT,
    panombre VARCHAR(30) NOT NULL,
    paprimerapell VARCHAR(30) NOT NULL,
    pasegundoapell VARCHAR(30),
    fechanacimiento DATE NOT NULL,
    edad INT
) ENGINE=InnoDB;

CREATE TABLE taquillero (
    registro INT PRIMARY KEY AUTO_INCREMENT,
    taqnombre VARCHAR(30) NOT NULL,
    taqprimerapell VARCHAR(30) NOT NULL,
    taqsegundoapell VARCHAR(30),
    fechacontrato DATE NOT NULL,
    usuario VARCHAR(20) NOT NULL,
    contrasena VARCHAR(20) NOT NULL,
    terminal INT NOT NULL,
    FOREIGN KEY (terminal) REFERENCES terminal(numero)
) ENGINE=InnoDB;

-- 3️⃣ TABLAS DE OPERACIÓN

CREATE TABLE viaje (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    horasalida TIME NOT NULL,
    horaentrada TIME NOT NULL,
    ruta INT NOT NULL,
    estado INT NOT NULL,
    FOREIGN KEY (ruta) REFERENCES ruta(codigo),
    FOREIGN KEY (estado) REFERENCES edo_viaje(numero)
) ENGINE=InnoDB;

CREATE TABLE detalle_viaje (
    autobus INT,
    viaje INT,
    conductor INT,
    PRIMARY KEY (autobus, viaje, conductor),
    FOREIGN KEY (autobus) REFERENCES autobus(numero),
    FOREIGN KEY (viaje) REFERENCES viaje(numero),
    FOREIGN KEY (conductor) REFERENCES conductor(registro)
) ENGINE=InnoDB;

CREATE TABLE asiento (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    ocupado BOOLEAN NOT NULL,
    tipo VARCHAR(5) NOT NULL,
    autobus INT NOT NULL,
    FOREIGN KEY (tipo) REFERENCES tipo_asientos(codigo),
    FOREIGN KEY (autobus) REFERENCES autobus(numero)
) ENGINE=InnoDB;

CREATE TABLE pago (
    codigo INT PRIMARY KEY AUTO_INCREMENT,
    fechapago DATETIME NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    tipo INT NOT NULL,
    FOREIGN KEY (tipo) REFERENCES tipo_pago(numero)
) ENGINE=InnoDB;

CREATE TABLE ticket (
    codigo INT PRIMARY KEY AUTO_INCREMENT,
    precio DECIMAL(10,2) NOT NULL,
    fechaemision DATETIME NOT NULL,
    asiento INT NOT NULL,
    viaje INT NOT NULL,
    pasajero INT NOT NULL,
    tipopasajero INT NOT NULL,
    pago INT NOT NULL,
    vendedor INT NOT NULL,
    FOREIGN KEY (asiento) REFERENCES asiento(numero),
    FOREIGN KEY (viaje) REFERENCES viaje(numero),
    FOREIGN KEY (pasajero) REFERENCES pasajero(num),
    FOREIGN KEY (tipopasajero) REFERENCES tipo_pasajero(num),
    FOREIGN KEY (pago) REFERENCES pago(codigo),
    FOREIGN KEY (vendedor) REFERENCES taquillero(registro)
) ENGINE=InnoDB;

-- 4️⃣ DATOS DE PRUEBA BÁSICOS

INSERT INTO modelo (nombre, numasientos, anio, cre, marca)
VALUES ('Volvo 9700', 40, 2020, 3, 'Volvo');

INSERT INTO edo_viaje (nombre, descripcion)
VALUES ('Programado', 'Viaje aún no iniciado'),
       ('En curso', 'Viaje en progreso'),
       ('Finalizado', 'Viaje completado');

INSERT INTO tipo_asientos (codigo, descripcion)
VALUES ('NOR', 'Normal'), ('PRE', 'Premium');

INSERT INTO tipo_pasajero (descuento, descripcion)
VALUES (0.00, 'Adulto'), (0.50, 'Estudiante');

INSERT INTO tipo_pago (nombre, descripcion)
VALUES ('Efectivo', 'Pago en ventanilla'),
       ('Tarjeta', 'Pago con tarjeta bancaria');
