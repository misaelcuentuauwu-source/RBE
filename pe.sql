-- Insertar viajes futuros (Diciembre 2025 - Enero 2026)

-- Viaje 4: Tijuana → Ensenada (1 Diciembre 2025)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(4, '2025-12-01 08:00:00', '2025-12-01 12:00:00', 3, 1, 1, 1);

-- Viaje 5: Rosarito → Tijuana (5 Diciembre 2025)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(5, '2025-12-05 09:00:00', '2025-12-05 13:30:00', 2, 1, 2, 2);

-- Viaje 6: Tijuana → Ensenada (10 Diciembre 2025)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(6, '2025-12-10 07:30:00', '2025-12-10 11:45:00', 3, 1, 3, 3);

-- Viaje 7: Tijuana → Mexicali (15 Diciembre 2025)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(7, '2025-12-15 10:00:00', '2025-12-15 12:50:00', 7, 1, 4, 4);

-- Viaje 8: Ensenada → Tijuana (20 Diciembre 2025)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(8, '2025-12-20 14:00:00', '2025-12-20 18:00:00', 4, 1, 5, 5);

-- Viaje 9: Tijuana → Rosarito (25 Diciembre 2025)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(9, '2025-12-25 06:30:00', '2025-12-25 10:45:00', 1, 1, 1, 1);

-- Viaje 10: Tijuana → Ensenada (1 Enero 2026)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(10, '2026-01-01 08:00:00', '2026-01-01 12:00:00', 3, 1, 2, 2);

-- Viaje 11: Tijuana → Tecate (5 Enero 2026)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(11, '2026-01-05 09:15:00', '2026-01-05 13:30:00', 5, 1, 3, 3);

-- Viaje 12: Rosarito → Tijuana (10 Enero 2026)
INSERT INTO viaje (numero, fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor) VALUES
(12, '2026-01-10 15:00:00', '2026-01-10 19:45:00', 2, 1, 4, 4);

-- Ahora necesitas crear los registros de viaje_asiento para cada viaje
-- (Asientos del 1-52 para autobus 1, 53-100 para autobus 2, etc.)

-- Para viaje 4 (autobus 1, 52 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 4, 0 FROM asiento WHERE autobus = 1;

-- Para viaje 5 (autobus 2, 48 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 5, 0 FROM asiento WHERE autobus = 2;

-- Para viaje 6 (autobus 3, 50 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 6, 0 FROM asiento WHERE autobus = 3;

-- Para viaje 7 (autobus 4, 46 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 7, 0 FROM asiento WHERE autobus = 4;

-- Para viaje 8 (autobus 5, 49 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 8, 0 FROM asiento WHERE autobus = 5;

-- Para viaje 9 (autobus 1, 52 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 9, 0 FROM asiento WHERE autobus = 1;

-- Para viaje 10 (autobus 2, 48 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 10, 0 FROM asiento WHERE autobus = 2;

-- Para viaje 11 (autobus 3, 50 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 11, 0 FROM asiento WHERE autobus = 3;

-- Para viaje 12 (autobus 4, 46 asientos)
INSERT INTO viaje_asiento (asiento, viaje, ocupado)
SELECT numero, 12, 0 FROM asiento WHERE autobus = 4;