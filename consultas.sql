/*
1. Información de un viaje
a. Número de viaje
b. Número de ruta
c. Fecha y hora de salida, en una columna
d. Fecha y hora de llegada, en una columna
e. Nombre de la ciudad de origen
f. Nombre de la terminal donde salen
g. Nombre de la ciudad de destino
h. Nombre de la terminal donde llegan
i. Nombre completo del operador, en una columna
j. Número del autobús asignado
k. Matrícula del autobús asignado
l. Cantidad de asientos del autobús
m. Cantidad de pasajeros
*/
SELECT
  v.numero AS numero_viaje,
  r.codigo AS numero_ruta,
  v.fecHoraSalida AS fecha_hora_salida,
  v.fecHoraEntrada AS fecha_hora_llegada,
  torig.nombre AS ciudad_origen,
  torg.nombre AS terminal_origen,         -- nombre de la terminal donde salen
  tdest_ci.nombre AS ciudad_destino,
  tdest.nombre AS terminal_destino,       -- nombre de la terminal donde llegan
  CONCAT(c.conNombre, ' ', c.conPrimerApell, ' ', IFNULL(c.conSegundoApell,'')) AS operador,
  v.autobus AS numero_autobus,
  a.placas AS matricula_autobus,
  m.numasientos AS cantidad_asientos,
  (SELECT COUNT(*) FROM ticket t WHERE t.viaje = v.numero) AS cantidad_pasajeros
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
LEFT JOIN conductor c ON v.conductor = c.registro
LEFT JOIN autobus a ON v.autobus = a.numero
LEFT JOIN modelo m ON a.modelo = m.numero
WHERE v.numero = 1;

/*
2. Obtener la lista de pasajeros que compraron boleto para un viaje específico.
a. Número de viaje
b. Nombre de la ciudad de origen
c. Nombre de la ciudad de destino
d. Fecha y hora de salida, en una columna
e. Nombre completo del pasajero, en una columna
f. Edad del pasajero
g. Número del autobús asignado
h. Número del boleto
i. Número del asiento
*/
SELECT
  v.numero AS numero_viaje,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.fecHoraSalida AS fecha_hora_salida,
  CONCAT(p.paNombre,' ', p.paPrimerApell, ' ', IFNULL(p.paSegundoApell,'')) AS nombre_pasajero,
  p.edad AS edad_pasajero,
  v.autobus AS numero_autobus,
  t.codigo AS numero_boleto,
  t.asiento AS numero_asiento
FROM ticket t
JOIN pasajero p ON t.pasajero = p.num
JOIN viaje v ON t.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE v.numero = 1
ORDER BY t.asiento;

/*
    Consulta dividida en 2
*/

SELECT
  v.numero AS numero_viaje,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.fecHoraSalida AS fecha_hora_salida
FROM ticket t
JOIN viaje v ON t.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE v.numero = 1
ORDER BY t.asiento
LIMIT 1;
SELECT
  CONCAT(p.paNombre,' ', p.paPrimerApell, ' ', IFNULL(p.paSegundoApell,'')) AS nombre_pasajero,
  p.edad AS edad_pasajero,
  v.autobus AS numero_autobus,
  t.codigo AS numero_boleto,
  t.asiento AS numero_asiento
FROM ticket t
JOIN pasajero p ON t.pasajero = p.num
JOIN viaje v ON t.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE v.numero = 1
ORDER BY t.asiento;

/*
3. Asientos que están disponibles para un viaje dado.
a. Número de viaje
b. Nombre de la ciudad de origen
c. Nombre de la ciudad de destino
d. Fecha y hora de salida, en una columna
e. Número del autobús asignado
f. Número del asiento disponible
*/
SELECT
  v.numero AS numero_viaje,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.fecHoraSalida AS fecha_hora_salida,
  v.autobus AS numero_autobus,
  a.numero AS numero_asiento
FROM viaje_asiento va
JOIN asiento a ON va.asiento = a.numero
JOIN viaje v ON va.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE v.numero = 1
  AND va.ocupado = 0
ORDER BY a.numero;

/*
    Consulta dividida en 2
*/

SELECT
  v.numero AS numero_viaje,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.fecHoraSalida AS fecha_hora_salida,
  v.autobus AS numero_autobus
FROM viaje_asiento va
JOIN asiento a ON va.asiento = a.numero
JOIN viaje v ON va.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE v.numero = 1
  AND va.ocupado = 0
LIMIT 1;
SELECT
  a.numero AS numero_asiento
FROM viaje_asiento va
JOIN asiento a ON va.asiento = a.numero
JOIN viaje v ON va.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE v.numero = 1
  AND va.ocupado = 0
ORDER BY a.numero;

/*
4. Viajes programados para una fecha específica.
a. Fecha y hora de salida, en una columna
b. Número del viaje
c. Ciudad de origen (nombre)
d. Ciudad de destino (nombre)
e. Número del autobús
*/
SELECT
  v.fecHoraSalida AS fecha_hora_salida,
  v.numero AS numero_viaje,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.autobus AS numero_autobus
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE DATE(v.fecHoraSalida) = '2025-01-10'
ORDER BY v.fecHoraSalida;

/*
5. Detalle de un boleto
a. Número del viaje
b. Fecha y hora de salida, en una columna
c. Fecha y hora de llegada, en una columna
d. Ciudad de origen (nombre)
e. Ciudad de destino (nombre)
f. Nombre completo del pasajero
g. Tipo de asiento (descripción)
h. Número del asiento
i. Precio del boleto
*/
SELECT
  v.numero AS numero_viaje,
  v.fecHoraSalida AS fecha_hora_salida,
  v.fecHoraEntrada AS fecha_hora_llegada,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  CONCAT(p.paNombre,' ', p.paPrimerApell, ' ', IFNULL(p.paSegundoApell,'')) AS nombre_pasajero,
  ta.descripcion AS tipo_asiento,
  t.asiento AS numero_asiento,
  t.precio AS precio_boleto
FROM ticket t
JOIN viaje v ON t.viaje = v.numero
JOIN pasajero p ON t.pasajero = p.num
JOIN asiento asi ON t.asiento = asi.numero
JOIN tipo_asiento ta ON asi.tipo = ta.codigo
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE t.codigo = 1;

/*
6. Boletos vendidos para cada viaje de una fecha.
a. Fecha programada
b. Número del viaje
c. Fecha y hora de salida, en una columna
d. Ciudad de origen (nombre)
e. Ciudad de destino (nombre)
f. Número del autobús
g. Cantidad de boletos vendidos
h. Cantidad de boletos disponibles
*/
SELECT
  DATE(v.fecHoraSalida) AS fecha_programada,
  v.numero AS numero_viaje,
  v.fecHoraSalida AS fecha_hora_salida,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.autobus AS numero_autobus,
  COUNT(t.codigo) AS boletos_vendidos,
  ( (SELECT COUNT(*) FROM asiento a WHERE a.autobus = v.autobus) - COUNT(t.codigo) ) AS boletos_disponibles
FROM viaje v
LEFT JOIN ticket t ON t.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE DATE(v.fecHoraSalida) = '2025-01-10'
GROUP BY v.numero, v.fecHoraSalida, torig.nombre, tdest_ci.nombre, v.autobus
ORDER BY v.fecHoraSalida;

/*
    Consulta dividida en 2
*/

SELECT
  DATE(v.fecHoraSalida) AS fecha_programada
FROM viaje v
WHERE DATE(v.fecHoraSalida) = '2025-01-10'
LIMIT 1;
SELECT
  v.numero AS numero_viaje,
  v.fecHoraSalida AS fecha_hora_salida,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.autobus AS numero_autobus,
  COUNT(t.codigo) AS boletos_vendidos,
  ( (SELECT COUNT(*) FROM asiento a WHERE a.autobus = v.autobus) - COUNT(t.codigo) ) AS boletos_disponibles
FROM viaje v
LEFT JOIN ticket t ON t.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE DATE(v.fecHoraSalida) = '2025-01-10'
GROUP BY v.numero, v.fecHoraSalida, torig.nombre, tdest_ci.nombre, v.autobus
ORDER BY v.fecHoraSalida;


/*
7. Viajes de un mismo conductor
a. Nombre completo del conductor, en una columna
b. Número del viaje
c. Fecha y hora de salida, en una columna
d. Fecha y hora de llegada, en una columna
e. Ciudad de origen (nombre)
f. Ciudad de destino (nombre)
g. Número del autobús
*/
SELECT
  CONCAT(c.conNombre,' ', c.conPrimerApell, ' ', IFNULL(c.conSegundoApell,'')) AS nombre_conductor,
  v.numero AS numero_viaje,
  v.fecHoraSalida AS fecha_hora_salida,
  v.fecHoraEntrada AS fecha_hora_llegada,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.autobus AS numero_autobus
FROM viaje v
JOIN conductor c ON v.conductor = c.registro
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE c.registro = 3
ORDER BY v.fecHoraSalida;

/*
    Consulta dividida en 2
*/

SELECT
  CONCAT(c.conNombre,' ', c.conPrimerApell, ' ', IFNULL(c.conSegundoApell,'')) AS nombre_conductor
FROM viaje v
JOIN conductor c ON v.conductor = c.registro
WHERE c.registro = 3;
SELECT
  v.numero AS numero_viaje,
  v.fecHoraSalida AS fecha_hora_salida,
  v.fecHoraEntrada AS fecha_hora_llegada,
  torig.nombre AS ciudad_origen,
  tdest_ci.nombre AS ciudad_destino,
  v.autobus AS numero_autobus
FROM viaje v
JOIN conductor c ON v.conductor = c.registro
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
WHERE c.registro = 3
ORDER BY v.fecHoraSalida;

/*
8. Información de un autobús
a. Número del autobús
b. Matricula
c. Nombre de la marca
d. Nombre del modelo
e. Año
f. Cantidad de asientos
*/
SELECT
  a.numero AS numero_autobus,
  a.placas AS matricula,
  mk.nombre AS marca,
  m.nombre AS modelo,
  m.año AS año,
  m.numasientos AS cantidad_asientos
FROM autobus a
JOIN modelo m ON a.modelo = m.numero
JOIN marca mk ON m.marca = mk.numero
WHERE a.numero = 3;


/*
9. Cantidad por tipos de asiento que tiene un autobús
a. Número del autobús
b. Descripción del tipo de asiento
c. Cantidad por tipo de asiento
*/
SELECT
  au.numero AS numero_autobus,
  ta.descripcion AS descripcion_tipo_asiento,
  COUNT(*) AS cantidad_por_tipo
FROM asiento a
JOIN tipo_asiento ta ON a.tipo = ta.codigo
JOIN autobus au ON a.autobus = au.numero
WHERE a.autobus = 1
GROUP BY ta.descripcion
ORDER BY ta.descripcion;

/*
    Consulta dividida en 2
*/

SELECT
  au.numero AS numero_autobus
FROM asiento a
JOIN autobus au ON a.autobus = au.numero
WHERE a.autobus = 1
LIMIT 1;
SELECT
  ta.descripcion AS descripcion_tipo_asiento,
  COUNT(*) AS cantidad_por_tipo
FROM asiento a
JOIN tipo_asiento ta ON a.tipo = ta.codigo
JOIN autobus au ON a.autobus = au.numero
WHERE a.autobus = 1
GROUP BY ta.descripcion
ORDER BY ta.descripcion;


/*
10.Corridas que salen de una misma ciudad en una fecha
a. Nombre de la ciudad
b. Fecha y hora de salida, en una columna
c. Número de la corrida
d. Ciudad de destino (nombre)
e. Número del autobús
f. Matricula del autobús
g. Nombre completo del operador asignado, en una columna
*/
SELECT
  torig.nombre AS ciudad,
  v.fecHoraSalida AS fecha_hora_salida,
  v.numero AS numero_corrida,
  tdest_ci.nombre AS ciudad_destino,
  v.autobus AS numero_autobus,
  aut.placas AS matricula_autobus,
  CONCAT(c.conNombre,' ', c.conPrimerApell, ' ', IFNULL(c.conSegundoApell,'')) AS operador_asignado
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
LEFT JOIN autobus aut ON v.autobus = aut.numero
LEFT JOIN conductor c ON v.conductor = c.registro
WHERE torig.nombre = 'Tijuana'
  AND DATE(v.fecHoraSalida) = '2025-01-10'
ORDER BY v.fecHoraSalida;


/*
    Consulta dividida en 2
*/

SELECT
  torig.nombre AS ciudad,
  v.fecHoraSalida AS fecha_hora_salida
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
WHERE torig.nombre = 'Tijuana'
  AND DATE(v.fecHoraSalida) = '2025-01-10'
LIMIT 1;
SELECT
  v.numero AS numero_corrida,
  tdest_ci.nombre AS ciudad_destino,
  v.autobus AS numero_autobus,
  aut.placas AS matricula_autobus,
  CONCAT(c.conNombre,' ', c.conPrimerApell, ' ', IFNULL(c.conSegundoApell,'')) AS operador_asignado
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal torg ON r.origen = torg.numero
JOIN ciudad torig ON torg.ciudad = torig.clave
JOIN terminal tdest ON r.destino = tdest.numero
JOIN ciudad tdest_ci ON tdest.ciudad = tdest_ci.clave
LEFT JOIN autobus aut ON v.autobus = aut.numero
LEFT JOIN conductor c ON v.conductor = c.registro
WHERE torig.nombre = 'Tijuana'
  AND DATE(v.fecHoraSalida) = '2025-01-10'
ORDER BY v.fecHoraSalida;