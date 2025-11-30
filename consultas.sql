-- Active: 1764103994512@@127.0.0.1@3306@rbe
--1. Información de un viaje
SELECT 
    v.numero AS viaje,
    v.ruta,
    v.fecHoraSalida AS salida,
    v.fecHoraEntrada AS llegada,
    co.nombre AS ciudad_origen,
    to2.nombre AS terminal_origen,
    cd.nombre AS ciudad_destino,
    td.nombre AS terminal_destino,
    CONCAT(c.conNombre, ' ', c.conPrimerApell, ' ', IFNULL(c.conSegundoApell,'')) AS operador,
    a.numero AS autobus,
    a.placas,
    m.numasientos,
    COUNT(t.codigo) AS cantidad_pasajeros
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal to2 ON r.origen = to2.numero
JOIN ciudad co ON to2.ciudad = co.clave
JOIN terminal td ON r.destino = td.numero
JOIN ciudad cd ON td.ciudad = cd.clave
LEFT JOIN conductor c ON v.conductor = c.registro
LEFT JOIN autobus a ON v.autobus = a.numero
LEFT JOIN modelo m ON a.modelo = m.numero
LEFT JOIN ticket t ON t.viaje = v.numero
WHERE v.numero = 1
GROUP BY v.numero;

--2. Pasajeros de un viaje específico
SELECT 
    v.numero AS viaje,
    co.nombre AS ciudad_origen,
    cd.nombre AS ciudad_destino,
    v.fecHoraSalida AS salida,
    CONCAT(p.paNombre, ' ', p.paPrimerApell, ' ', IFNULL(p.paSegundoApell,'')) AS pasajero,
    p.edad,
    v.autobus,
    t.codigo AS boleto,
    t.asiento AS asiento
FROM ticket t
JOIN pasajero p ON t.pasajero = p.num
JOIN viaje v ON t.viaje = v.numero
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal to2 ON r.origen = to2.numero
JOIN ciudad co ON to2.ciudad = co.clave
JOIN terminal td ON r.destino = td.numero
JOIN ciudad cd ON td.ciudad = cd.clave
WHERE v.numero = 1;

--3. Asientos disponibles para un viaje
SELECT
    v.numero AS viaje,
    co.nombre AS ciudad_origen,
    cd.nombre AS ciudad_destino,
    v.fecHoraSalida AS salida,
    v.autobus,
    a.numero AS asiento_disponible
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal o ON r.origen = o.numero
JOIN ciudad co ON o.ciudad = co.clave
JOIN terminal d ON r.destino = d.numero
JOIN ciudad cd ON d.ciudad = cd.clave
JOIN asiento a ON a.autobus = v.autobus
LEFT JOIN viaje_asiento va ON va.asiento = a.numero AND va.viaje = v.numero
WHERE v.numero = 1
  AND (va.ocupado = 0 OR va.ocupado IS NULL);

--4. Viajes programados en una fecha
SELECT
    v.fecHoraSalida AS salida,
    v.numero AS viaje,
    co.nombre AS ciudad_origen,
    cd.nombre AS ciudad_destino,
    v.autobus
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal o ON r.origen = o.numero
JOIN ciudad co ON o.ciudad = co.clave
JOIN terminal d ON r.destino = d.numero
JOIN ciudad cd ON d.ciudad = cd.clave
WHERE DATE(v.fecHoraSalida) = '01/10/2025';

--5. Detalle de un boleto
SELECT 
    v.numero AS viaje,
    v.fecHoraSalida AS salida,
    v.fecHoraEntrada AS llegada,
    co.nombre AS ciudad_origen,
    cd.nombre AS ciudad_destino,
    CONCAT(p.paNombre, ' ', p.paPrimerApell, ' ', IFNULL(p.paSegundoApell,'')) AS pasajero,
    ta.descripcion AS tipo_asiento,
    t.asiento,
    t.precio
FROM ticket t
JOIN viaje v ON t.viaje = v.numero
JOIN pasajero p ON t.pasajero = p.num
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal o ON r.origen = o.numero
JOIN ciudad co ON o.ciudad = co.clave
JOIN terminal d ON r.destino = d.numero
JOIN ciudad cd ON d.ciudad = cd.clave
JOIN asiento a ON t.asiento = a.numero
JOIN tipo_asiento ta ON a.tipo = ta.codigo
WHERE t.codigo = 1;

--6. Boletos vendidos por viaje en una fecha
SELECT
    DATE(v.fecHoraSalida) AS fecha,
    v.numero AS viaje,
    v.fecHoraSalida AS salida,
    co.nombre AS ciudad_origen,
    cd.nombre AS ciudad_destino,
    v.autobus,
    COUNT(t.codigo) AS boletos_vendidos,
    (SELECT COUNT(*) FROM asiento WHERE autobus = v.autobus) - COUNT(t.codigo) AS boletos_disponibles
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal o ON r.origen = o.numero
JOIN ciudad co ON o.ciudad = co.clave
JOIN terminal d ON r.destino = d.numero
JOIN ciudad cd ON d.ciudad = cd.clave
LEFT JOIN ticket t ON t.viaje = v.numero
WHERE DATE(v.fecHoraSalida) = 1
GROUP BY v.numero;

--7. Viajes de un conductor
SELECT
    CONCAT(c.conNombre, ' ', c.conPrimerApell, ' ', IFNULL(c.conSegundoApell,'')) AS conductor,
    v.numero AS viaje,
    v.fecHoraSalida AS salida,
    v.fecHoraEntrada AS llegada,
    co.nombre AS ciudad_origen,
    cd.nombre AS ciudad_destino,
    v.autobus
FROM viaje v
JOIN conductor c ON v.conductor = c.registro
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal o ON r.origen = o.numero
JOIN ciudad co ON o.ciudad = co.clave
JOIN terminal d ON r.destino = d.numero
JOIN ciudad cd ON d.ciudad = cd.clave
WHERE c.registro = 1;

--8. Información de un autobús
SELECT
    a.numero AS autobus,
    a.placas,
    m2.nombre AS marca,
    m.nombre AS modelo,
    m.año,
    m.numasientos
FROM autobus a
JOIN modelo m ON a.modelo = m.numero
JOIN marca m2 ON m.marca = m2.numero
WHERE a.numero = 1;

--9. Cantidad por tipo de asiento en un autobús
SELECT
    a.autobus,
    ta.descripcion,
    COUNT(*) AS cantidad
FROM asiento a
JOIN tipo_asiento ta ON a.tipo = ta.codigo
WHERE a.autobus = 1
GROUP BY a.tipo;

--10. Corridas que salen de una misma ciudad en una fecha
SELECT
    ciu.nombre AS ciudad_origen,
    v.fecHoraSalida AS salida,
    v.numero AS corrida,
    cd.nombre AS ciudad_destino,
    v.autobus,
    a.placas,
    CONCAT(c.conNombre, ' ', c.conPrimerApell, ' ', IFNULL(c.conSegundoApell,'')) AS operador
FROM viaje v
JOIN ruta r ON v.ruta = r.codigo
JOIN terminal t ON r.origen = t.numero
JOIN ciudad ciu ON t.ciudad = ciu.clave
JOIN terminal td ON r.destino = td.numero
JOIN ciudad cd ON td.ciudad = cd.clave
JOIN autobus a ON v.autobus = a.numero
JOIN conductor c ON v.conductor = c.registro
WHERE DATE(v.fecHoraSalida) = '01/10/2025'
AND t.ciudad = 'MXL';