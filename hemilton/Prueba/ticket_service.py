from conexion import crear_conexion
from datetime import datetime

# Consulta para sacar viajes proximos #

def get_viajes_proximos():

    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)
    cur.execute("""
        SELECT v.numero, v.fecHoraSalida, v.fecHoraEntrada, v.ruta, v.autobus,
               r.origen, r.destino
        FROM viaje v
        JOIN ruta r ON v.ruta = r.codigo
        WHERE v.fecHoraSalida >= NOW()
        ORDER BY v.fecHoraSalida ASC
    """)
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows

#consulta para sacar el nombre de la terminal#

def get_terminal_nombre(num_terminal):
    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)
    cur.execute("SELECT nombre FROM terminal WHERE numero=%s", (num_terminal,))
    r = cur.fetchone()
    cur.close()
    cn.close()
    return r['nombre'] if r else str(num_terminal)

def get_asientos_disponibles_por_viaje(viaje_num):
    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)

    # Consulta para sacar numeros del autobus #
    cur.execute("""
        SELECT a.numero AS asiento_num, a.tipo
        FROM asiento a
        JOIN viaje v ON v.autobus = a.autobus
        WHERE v.numero = %s
        ORDER BY a.numero
    """, (viaje_num,))
    asientos = cur.fetchall()

    # Consulta para sacar asientos ocupados #
    cur.execute("""
        SELECT asiento FROM viaje_asiento
        WHERE viaje = %s AND ocupado = 1
    """, (viaje_num,))
    ocupados = {row['asiento'] for row in cur.fetchall()}

    cur.close()
    cn.close()

    disponibles = [a for a in asientos if a['asiento_num'] not in ocupados]
    return disponibles

def buscar_pasajeros_por_nombre(q):
    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)
    term = f"%{q}%"
    #consulta para sacar nombre del pasajero#
    
    cur.execute("""
        SELECT num, paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad
        FROM pasajero
        WHERE paNombre LIKE %s OR paPrimerApell LIKE %s OR paSegundoApell LIKE %s
        LIMIT 50
    """, (term, term, term))
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows

def crear_pasajero(paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad):
    #insertar datos de pasajero#
    cn = crear_conexion()
    cur = cn.cursor()
    cur.execute("""
        INSERT INTO pasajero (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad)
        VALUES (%s, %s, %s, %s, %s)
    """, (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad))
    cn.commit()
    nuevo_id = cur.lastrowid
    cur.close()
    cn.close()
    return nuevo_id

def get_tipo_pasajeros():
    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)
    cur.execute("SELECT num, descuento, descripcion FROM tipo_pasajero")
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows

def get_tipos_pago():
    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)
    cur.execute("SELECT numero, nombre, descripcion FROM tipo_pago")
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows

# metodo para la venta del boleto #
def vender_boleto(transaccion):
    cn = crear_conexion()
    cur = cn.cursor()
    try:
        # insertar pago
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO pago (fechapago, monto, tipo, vendedor)
            VALUES (%s, %s, %s, %s)
        """, (now, transaccion['precio'], transaccion['tipo_pago'], transaccion['vendedor']))
        pago_id = cur.lastrowid

        # insertar ticket
        cur.execute("""
            INSERT INTO ticket (precio, fechaEmision, asiento, viaje, pasajero, tipopasajero, pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (transaccion['precio'], now, transaccion['asiento'], transaccion['viaje'],
              transaccion['pasajero'], transaccion['tipopasajero'], pago_id))
        ticket_id = cur.lastrowid

        cur.execute("""
            SELECT COUNT(*) cnt FROM viaje_asiento WHERE viaje=%s AND asiento=%s
        """, (transaccion['viaje'], transaccion['asiento']))
        exists = cur.fetchone()[0] > 0
        if exists:
            cur.execute("""
                UPDATE viaje_asiento SET ocupado=1 WHERE viaje=%s AND asiento=%s
            """, (transaccion['viaje'], transaccion['asiento']))
        else:
            cur.execute("""
                INSERT INTO viaje_asiento (asiento, viaje, ocupado) VALUES (%s, %s, 1)
            """, (transaccion['asiento'], transaccion['viaje']))

        cn.commit()
        cur.close()
        cn.close()
        return True, {'ticket_id': ticket_id, 'pago_id': pago_id}

    except Exception as e:
        cn.rollback()
        cur.close()
        cn.close()
        return False, str(e)
