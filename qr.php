<?php
// qr.php - API del sistema

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$db = new mysqli("localhost", "root", "", "rbe");

if ($db->connect_error) {
    die(json_encode(['error' => 'Error de conexión']));
}

$action = $_GET['action'] ?? '';

switch($action) {
    
    case 'rutas':
        $sql = "SELECT r.codigo, r.precio,
                       co.nombre as ciudad_origen, 
                       cd.nombre as ciudad_destino
                FROM ruta r
                INNER JOIN terminal to ON r.origen = to.numero
                INNER JOIN terminal td ON r.destino = td.numero
                INNER JOIN ciudad co ON to.ciudad = co.clave
                INNER JOIN ciudad cd ON td.ciudad = cd.clave";
        
        $result = $db->query($sql);
        $data = [];
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;
    
    case 'viajes':
        $ruta = $_GET['ruta'] ?? 0;
        $fecha = $_GET['fecha'] ?? date('Y-m-d');
        
        $sql = "SELECT v.numero, v.fecHoraSalida, v.fecHoraEntrada as fecHoraLlegada, m.numasientos,
                       (SELECT COUNT(*) FROM viaje_asiento va 
                        WHERE va.viaje = v.numero AND va.ocupado = 1) as asientos_ocupados
                FROM viaje v
                INNER JOIN autobus a ON v.autobus = a.numero
                INNER JOIN modelo m ON a.modelo = m.numero
                WHERE v.ruta = ? AND DATE(v.fecHoraSalida) = ?
                AND v.estado = 1 AND v.fecHoraSalida > NOW()";
        
        $stmt = $db->prepare($sql);
        $stmt->bind_param("is", $ruta, $fecha);
        $stmt->execute();
        $result = $stmt->get_result();
        
        $data = [];
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;
    
    case 'asientos':
        $viaje = $_GET['viaje'] ?? 0;
        
        $sql = "SELECT a.numero, COALESCE(va.ocupado, 0) as ocupado
                FROM asiento a
                INNER JOIN viaje v ON v.autobus = a.autobus
                LEFT JOIN viaje_asiento va ON va.asiento = a.numero AND va.viaje = v.numero
                WHERE v.numero = ?
                ORDER BY a.numero";
        
        $stmt = $db->prepare($sql);
        $stmt->bind_param("i", $viaje);
        $stmt->execute();
        $result = $stmt->get_result();
        
        $data = [];
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;
    
    case 'tipos':
        $result = $db->query("SELECT * FROM tipo_pasajero");
        $data = [];
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;
    
    case 'crear':
        $input = json_decode(file_get_contents('php://input'), true);
        
        $db->begin_transaction();
        
        try {
            // Insertar pasajero
            $stmt = $db->prepare("INSERT INTO pasajero (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad) VALUES (?, ?, '', ?, ?)");
            $stmt->bind_param("sssi", $input['nombre'], $input['apellido'], $input['fechaNac'], $input['edad']);
            $stmt->execute();
            $pasajeroId = $db->insert_id;
            
            // Insertar pago
            $stmt = $db->prepare("INSERT INTO pago (fechapago, monto, tipo, vendedor) VALUES (NOW(), ?, 1, 1)");
            $stmt->bind_param("d", $input['monto']);
            $stmt->execute();
            $pagoId = $db->insert_id;
            
            // Crear ticket
            $stmt = $db->prepare("INSERT INTO ticket (precio, fechaEmision, asiento, viaje, pasajero, tipopasajero, pago) VALUES (?, NOW(), ?, ?, ?, ?, ?)");
            $stmt->bind_param("diiiii", $input['precio'], $input['asiento'], $input['viaje'], $pasajeroId, $input['tipo'], $pagoId);
            $stmt->execute();
            $ticketId = $db->insert_id;
            
            // Ocupar asiento
            $stmt = $db->prepare("INSERT INTO viaje_asiento (asiento, viaje, ocupado) VALUES (?, ?, 1) ON DUPLICATE KEY UPDATE ocupado = 1");
            $stmt->bind_param("ii", $input['asiento'], $input['viaje']);
            $stmt->execute();
            
            // Obtener info completa del boleto
            $sql = "SELECT 
                        t.codigo,
                        t.precio,
                        t.fechaEmision,
                        p.paNombre,
                        p.paPrimerApell,
                        tp.descripcion as tipo_pasajero,
                        a.numero as num_asiento,
                        v.fecHoraSalida,
                        v.fecHoraEntrada as fecHoraLlegada,
                        t_origen.nombre as terminal_origen,
                        t_destino.nombre as terminal_destino,
                        co.nombre as ciudad_origen,
                        cd.nombre as ciudad_destino
                    FROM ticket t
                    INNER JOIN pasajero p ON t.pasajero = p.num
                    INNER JOIN tipo_pasajero tp ON t.tipopasajero = tp.num
                    INNER JOIN asiento a ON t.asiento = a.numero
                    INNER JOIN viaje v ON t.viaje = v.numero
                    INNER JOIN ruta r ON v.ruta = r.codigo
                    INNER JOIN terminal t_origen ON r.origen = t_origen.numero
                    INNER JOIN terminal t_destino ON r.destino = t_destino.numero
                    INNER JOIN ciudad co ON t_origen.ciudad = co.clave
                    INNER JOIN ciudad cd ON t_destino.ciudad = cd.clave
                    WHERE t.codigo = ?";
            
            $stmt = $db->prepare($sql);
            $stmt->bind_param("i", $ticketId);
            $stmt->execute();
            $boleto = $stmt->get_result()->fetch_assoc();
            
            $db->commit();
            echo json_encode($boleto);
            
        } catch (Exception $e) {
            $db->rollback();
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;
    
    default:
        echo json_encode(['error' => 'Acción inválida']);
}

$db->close();
?>