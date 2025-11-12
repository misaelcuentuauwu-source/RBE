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