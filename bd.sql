-- Active: 1762888131509@@127.0.0.1@3306@rbe
CREATE DATABASE RBE;
use RBE;

CREATE TaBLE modelo(
    numero INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    numAsientos INT NOT NULL,
    anio INT NOT NULL,
    capacidad INT NOT NULL,
    marca VARCHAR(20) NOT NULL
);

CREATE TABLE conductor(
    registro INT PRIMARY KEY,
    conNombre VARCHAR(30) NOT NULL,
    conPrimerApell VARCHAR(30) NOT NULL,
    conSegApell VARCHAR(30) NOT NULL,
    licNumero VARCHAR(14) NOT NULL,
    licVencimiento DATE NOT NULL
);

create table ciudad(
    codigo varchar(5) PRIMARY KEY,
    nombre varchar(15) not null unique
);

create table tipo_asiento(
    codigo varchar(5) PRIMARY KEY, 
    descripcion varchar(30) not null unique
);

create table tipo_pasajero(
    num INT PRIMARY KEY, 
    descuento INT NOT NULL,
    descripcion varchar(30) not null unique
);

create table tipo_pago(
    numero INT PRIMARY KEY, 
    nombre VARCHAR(30) NOT NULL,
    descripcion varchar(50) not null UNIQUE
);

create table edo_viaje(
    numero INT PRIMARY KEY, 
    nombre VARCHAR(30) NOT NULL,
    descripcion varchar(50) not null UNIQUE
);

CREATE Table terminal(
    numero INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    dirCalle VARCHAR(30) NOT NULL,
    dirNumero VARCHAR(30) NOT NULL,
    dirColonia VARCHAR(30) NOT NULL,
    ciudad varchar(5) NOT NULL,
    Foreign Key (ciudad) REFERENCES ciudad(codigo)
);

CREATE Table ruta(
    codigo VARCHAR(5) PRIMARY KEY,
    duracion INT NOT NULL,
    origen INT NOT NULL,
    destino INT NOT NULL,
    Foreign Key (origen) REFERENCES terminal(numero),
    Foreign Key (destino) REFERENCES terminal(numero)
);

CREATE Table viaje(
    numero INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    horaSalida TIME NOT NULL,
    horaEntrada TIME NOT NULL,
    ruta VARCHAR(5) NOT NULL,
    estado INT NOT NULL,
    FOREIGN KEY (ruta) REFERENCES ruta(codigo),
    FOREIGN KEY (estado) REFERENCES edo_viaje(numero)
)

CREATE Table autobus(
    numero INT PRIMARY KEY AUTO_INCREMENT,
    modelo INT NOT NULL,
    placas VARCHAR(7),
    FOREIGN KEY (modelo) REFERENCES modelo(numero)
);

CREATE TABLE detalle_viaje(
    viaje INT NOT NULL,
    conductor INT NOT NULL,
    autobus INT NOT NULL,
    PRIMARY KEY (viaje, conductor, autobus),
    FOREIGN KEY (viaje) REFERENCES viaje(numero),
    FOREIGN KEY (conductor) REFERENCES conductor(registro),
    FOREIGN KEY (autobus) REFERENCES autobus(numero)
);

CREATE TABLE asiento(
    numero INT PRIMARY KEY AUTO_INCREMENT,
    ocupado BOOLEAN NOT NULL,
    tipo VARCHAR(5) NOT NULL,
    autobus INT NOT NULL,
    FOREIGN KEY (tipo) REFERENCES tipo_asiento(codigo),
    FOREIGN KEY (autobus) REFERENCES autobus(numero)
);

CREATE TABLE pasajero(
    num INT PRIMARY KEY AUTO_INCREMENT,
    paNombre VARCHAR(30) NOT NULL,
    paPrimerApell VARCHAR(30) NOT NULL,
    paSegundoApell VARCHAR(30),
    fechaNacimiento DATE NOT NULL,
    edad INT
);

CREATE TABLE pago(
    codigo VARCHAR(5) PRIMARY KEY,
    fechaPago DATETIME NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    tipo INT NOT NULL,
    FOREIGN KEY (tipo) REFERENCES tipo_pago(numero)
);

CREATE TABLE taquillero(
    registro INT PRIMARY KEY,
    taqNombre VARCHAR(30) NOT NULL,
    taqPrimerApell VARCHAR(30) NOT NULL,
    taqSegundoApell VARCHAR(30),
    fechaContrato DATE NOT NULL,
    usuario VARCHAR(20) NOT NULL,
    contraseña VARCHAR(20) NOT NULL,
    terminal INT NOT NULL,
    FOREIGN KEY (terminal) REFERENCES terminal(numero)
);

CREATE TABLE ticket(
    codigo VARCHAR(10) PRIMARY KEY,
    precio DECIMAL(10,2) NOT NULL,
    fechaEmision DATETIME NOT NULL,
    asiento INT NOT NULL,
    viaje INT NOT NULL,
    pasajero INT NOT NULL,
    tipoPasajero INT NOT NULL,
    pago VARCHAR(5) NOT NULL,
    vendedor INT NOT NULL,
    FOREIGN KEY (asiento) REFERENCES asiento(numero),
    FOREIGN KEY (viaje) REFERENCES viaje(numero),
    FOREIGN KEY (pasajero) REFERENCES pasajero(num),
    FOREIGN KEY (tipoPasajero) REFERENCES tipo_pasajero(num),
    FOREIGN KEY (pago) REFERENCES pago(codigo),
    FOREIGN KEY (vendedor) REFERENCES taquillero(registro)
);

CREATE Table viaje_asiento(
    viaje INT NOT NULL,
    asiento INT NOT NULL,
    FOREIGN KEY (viaje) REFERENCES viaje(numero),
    FOREIGN KEY (asiento) REFERENCES asiento(numero)
);