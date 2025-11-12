-- 🚫 1. borrar base de datos anterior si existe
drop database if exists prototipo;

-- 🆕 2. crear base de datos nueva
create database prototipo;
use prototipo;

-- ==========================================
-- sistema de tickets - modelo relacional 2
-- autor: misael urquidez arredondo
-- ==========================================

-- 1️⃣ tablas base

create table ciudad (
    clave varchar(5) primary key,
    nombre varchar(30) not null
) engine=innodb;

insert into ciudad (clave, nombre) values
('TJU','Tijuana'),
('ENS','Ensenada'),
('ROS','Rosarito'),
('TEC','Tecate'),
('MXL','Mexicali'),
('SFE','San Felipe');


use prototipo;
insert into terminal (ternombre, ternumcalle, tercalle, tercolonia, ciudad) values
('Terminal Tijuana', '123', 'Revolución', 'Centro', 'TJU'),
('Terminal Ensenada', '456', 'Juárez', 'Valle Dorado', 'ENS'),
('Terminal Rosarito', '78', 'Héroes', 'Playas', 'ROS'),
('Terminal Tecate', '90', 'Independencia', 'Centro', 'TEC'),
('Terminal Mexicali', '321', 'Lázaro Cárdenas', 'Zona Centro', 'MXL'),
('Terminal San Felipe', '12', 'Marina', 'Pueblo Nuevo', 'SFE');


create table modelo (
    numero int primary key auto_increment,
    nombre varchar(30) not null,
    numasientos int not null,
    anio int not null,
    cre int not null,
    marca varchar(20) not null
) engine=innodb;

create table edo_viaje (
    numero int primary key auto_increment,
    nombre varchar(30) not null,
    descripcion varchar(50) not null
) engine=innodb;

create table tipo_asientos (
    codigo varchar(5) primary key,
    descripcion varchar(30) not null
) engine=innodb;

create table tipo_pasajero (
    num int primary key auto_increment,
    descuento decimal(5,2),
    descripcion varchar(30) not null
) engine=innodb;

create table tipo_pago (
    numero int primary key auto_increment,
    nombre varchar(30) not null,
    descripcion varchar(50) not null
) engine=innodb;

-- 2️⃣ tablas intermedias

create table terminal (
    numero int primary key auto_increment,
    ternombre varchar(30) not null,
    ternumero varchar(10) not null,
    tercalle varchar(30) not null,
    tercolonia varchar(30) not null,
    ciudad varchar(5) not null,
    foreign key (ciudad) references ciudad(clave)
) engine=innodb;


insert into terminal (ternombre, ternumero, tercalle, tercolonia, ciudad) values
('Terminal Tijuana', '123', 'Revolución', 'Centro', 'TJU'),
('Terminal Ensenada', '456', 'Juárez', 'Valle Dorado', 'ENS'),
('Terminal Rosarito', '78', 'Héroes', 'Playas', 'ROS'),
('Terminal Tecate', '90', 'Independencia', 'Centro', 'TEC'),
('Terminal Mexicali', '321', 'Lázaro Cárdenas', 'Zona Centro', 'MXL'),
('Terminal San Felipe', '12', 'Marina', 'Pueblo Nuevo', 'SFE');


create table ruta (
    codigo int primary key auto_increment,
    origen int not null,
    destino int not null,
    duracion varchar(10) not null,
    foreign key (origen) references terminal(numero),
    foreign key (destino) references terminal(numero)
) engine=innodb;

create table autobus (
    numero int primary key auto_increment,
    modelo int not null,
    placas varchar(10) not null unique,
    foreign key (modelo) references modelo(numero)
) engine=innodb;

create table conductor (
    registro int primary key auto_increment,
    connombre varchar(30) not null,
    conprimerapell varchar(30) not null,
    consegundoapell varchar(30),
    licnumero varchar(15) not null,
    licvencimiento date not null,
    fechacontrato date not null
) engine=innodb;

create table pasajero (
    num int primary key auto_increment,
    panombre varchar(30) not null,
    paprimerapell varchar(30) not null,
    pasegundoapell varchar(30),
    fechanacimiento date not null,
    edad int
) engine=innodb;

create table taquillero (
    registro int primary key auto_increment,
    taqnombre varchar(30) not null,
    taqprimerapell varchar(30) not null,
    taqsegundoapell varchar(30),
    fechacontrato date not null,
    usuario varchar(20) not null,
    contrasena varchar(20) not null,
    terminal int not null,
    foreign key (terminal) references terminal(numero)
) engine=innodb;

-- 3️⃣ tablas de operación

create table viaje (
    numero int primary key auto_increment,
    fecha date not null,
    horasalida time not null,
    horaentrada time not null,
    ruta int not null,
    estado int not null,
    foreign key (ruta) references ruta(codigo),
    foreign key (estado) references edo_viaje(numero)
) engine=innodb;

create table detalle_viaje (
    autobus int,
    viaje int,
    conductor int,
    primary key (autobus, viaje, conductor),
    foreign key (autobus) references autobus(numero),
    foreign key (viaje) references viaje(numero),
    foreign key (conductor) references conductor(registro)
) engine=innodb;

create table asiento (
    numero int primary key auto_increment,
    ocupado boolean not null,
    tipo varchar(5) not null,
    autobus int not null,
    foreign key (tipo) references tipo_asientos(codigo),
    foreign key (autobus) references autobus(numero)
) engine=innodb;

create table pago (
    codigo int primary key auto_increment,
    fechapago datetime not null,
    monto decimal(10,2) not null,
    tipo int not null,
    foreign key (tipo) references tipo_pago(numero)
) engine=innodb;

create table ticket (
    codigo int primary key auto_increment,
    precio decimal(10,2) not null,
    fechaemision datetime not null,
    asiento int not null,
    viaje int not null,
    pasajero int not null,
    tipopasajero int not null,
    pago int not null,
    vendedor int not null,
    foreign key (asiento) references asiento(numero),
    foreign key (viaje) references viaje(numero),
    foreign key (pasajero) references pasajero(num),
    foreign key (tipopasajero) references tipo_pasajero(num),
    foreign key (pago) references pago(codigo),
    foreign key (vendedor) references taquillero(registro)
) engine=innodb;
