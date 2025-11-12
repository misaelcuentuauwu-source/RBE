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
    numero INT
);