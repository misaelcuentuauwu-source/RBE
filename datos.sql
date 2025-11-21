USE rbe;

-- Ciudades
INSERT INTO ciudad (clave, nombre) VALUES
('TIJ', 'Tijuana'),
('MXL', 'Mexicali'),
('ENS', 'Ensenada');

-- Terminales (teléfono incluido)
INSERT INTO terminal (numero, nombre, dirCalle, dirNumero, dirColonia, telefono, ciudad) VALUES
(1, 'Terminal Tijuana', 'Av Revolución', '100', 'Centro', '6641234567', 'TIJ'),
(2, 'Terminal Mexicali', 'Calzada Independencia', '200', 'Centro', '6861234567', 'MXL'),
(3, 'Terminal Ensenada', 'Blvd Costero', '300', 'Playa', '6461234567', 'ENS');

-- Tipos de asiento
INSERT INTO tipo_asiento (codigo, descripcion) VALUES
('NOR', 'Normal'),
('PRE', 'Premium');

-- Tipos de pasajero
INSERT INTO tipo_pasajero (num, descuento, descripcion) VALUES
(1, 0, 'Adulto'),
(2, 50, 'Estudiante'),
(3, 30, 'INAPAM');

-- Tipos de pago
INSERT INTO tipo_pago (numero, nombre, descripcion) VALUES
(1, 'Efectivo', 'Pago en efectivo'),
(2, 'Tarjeta', 'Pago con tarjeta bancaria');

-- Estados de viaje
INSERT INTO edo_viaje (numero, nombre, descripcion) VALUES
(1, 'Programado', 'Viaje aún no inicia'),
(2, 'En curso', 'Viaje en progreso'),
(3, 'Finalizado', 'Viaje terminado');

-- Conductores
INSERT INTO conductor (registro, conNombre, conPrimerApell, conSegundoApell, licNumero, licVencimiento, fechaContrato) VALUES
(100, 'Luis', 'Rojas', 'Lopez', 'LIC12345', '2027-05-10', '2020-01-01'),
(101, 'Marcos', 'Pérez', 'Hernandez', 'LIC56433', '2026-11-20', '2019-03-14');

-- Marcas
INSERT INTO marca (numero, nombre) VALUES 
(1, 'Mercedes-Benz'),
(2, 'Volvo'),
(3, 'Scania');

-- Modelos
INSERT INTO modelo (numero, nombre, numasientos, año, capacidad, marca) VALUES
(1, 'Modelo 2022', 40, 2022, 5000, 1),
(2, 'Modelo 2021', 50, 2021, 6000, 2);

-- Autobuses
INSERT INTO autobus (numero, modelo, placas, serieVIN) VALUES
(10, 1, 'ABC1234', '1A2B3C4D5E6F7G8H1'),
(11, 2, 'XYZ9876', '9H8G7F6E5D4C3B2A1');

-- Asientos autobús 10
INSERT INTO asiento (tipo, autobus)
SELECT 'NOR', 10 FROM 
(SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10) a,
(SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) b
LIMIT 40;

-- Asientos autobús 11
INSERT INTO asiento (tipo, autobus)
SELECT 'NOR', 11 FROM 
(SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10) a,
(SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5) b
LIMIT 50;

-- Rutas
INSERT INTO ruta (codigo, duracion, origen, destino, precio) VALUES
(1, '02:30', 1, 2, 450.00),  
(2, '02:30', 2, 1, 450.00),  
(3, '01:45', 1, 3, 300.00),  
(4, '01:45', 3, 1, 300.00),  
(5, '03:00', 2, 3, 400.00),  
(6, '03:00', 3, 2, 400.00);

-- Viajes
INSERT INTO viaje (fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
('2025-01-10 08:00:00', '2025-01-10 10:30:00', 1, 1, 10, 100),
('2025-01-11 08:00:00', '2025-01-11 10:30:00', 2, 1, 11, 101),
('2025-01-12 09:00:00', '2025-01-12 10:45:00', 3, 1, 10, 100),
('2025-01-12 12:00:00', '2025-01-12 13:45:00', 4, 1, 11, 101);

-- Taquilleros (nuevo esquema con supervisa booleano)
INSERT INTO taquillero (taqNombre, taqPrimerApell, taqSegundoApell, fechaContrato, usuario, `contraseña`, terminal, supervisa) VALUES
('Miguel', 'Vargas', 'Lopez', '2022-05-10', 'miquel', '1234', 1, FALSE),
('Lucia', 'Nava', NULL, '2023-07-15', 'lucia', 'abcd', 2, TRUE);

-- Pasajeros
INSERT INTO pasajero (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad) VALUES
('Carlos', 'Martinez', 'Lopez', '1990-05-10', 34),
('Ana', 'Soto', NULL, '2001-10-21', 23);
