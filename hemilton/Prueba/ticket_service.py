# ticket_service.py
# -------------------------
# Servicio de acceso a BD para la venta de boletos.
# Usa la conexión centralizada (conexion.crear_conexion).
# Adaptaciones: tablas y columnas según tu esquema RBE.
# -------------------------

from conexion import crear_conexion
from datetime import datetime

def get_viajes_proximos():
    """
    Devuelve lista de viajes próximos con info (numero, fecHoraSalida, fecHoraEntrada, ruta, origen_nombre, destino_nombre, autobus).
    """
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

def get_terminal_nombre(num_terminal):
    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)
    cur.execute("SELECT nombre FROM terminal WHERE numero=%s", (num_terminal,))
    r = cur.fetchone()
    cur.close()
    cn.close()
    return r['nombre'] if r else str(num_terminal)

def get_asientos_disponibles_por_viaje(viaje_num):
    """
    Devuelve lista de asientos (numero, tipo) que NO están ocupados para un viaje.
    Utiliza viaje_asiento para verificar existencia; si no existe la fila de viaje_asiento
    asumimos que el asiento está disponible (pero normalmente preparamos viaje_asiento cuando se crea el viaje).
    """
    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)

    # Primero, todos los asientos del autobús del viaje
    cur.execute("""
        SELECT a.numero AS asiento_num, a.tipo
        FROM asiento a
        JOIN viaje v ON v.autobus = a.autobus
        WHERE v.numero = %s
        ORDER BY a.numero
    """, (viaje_num,))
    asientos = cur.fetchall()

    # Luego, cuales están marcados ocupados en viaje_asiento
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
    """
    Busca pasajeros por coincidencia simple en nombre o apellido.
    """
    cn = crear_conexion()
    cur = cn.cursor(dictionary=True)
    term = f"%{q}%"
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
    """
    Inserta pasajero y devuelve su id (num).
    """
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

# ---------- operaciones transaccionales: pago + ticket + marcar asiento ----------
def vender_boleto(transaccion):
    """
    Realiza la venta dentro de una transacción atómica.
    transaccion: dict con keys:
      - viaje (int)
      - asiento (int)
      - pasajero (int)
      - tipopasajero (int)
      - precio (decimal/float)
      - tipo_pago (int)
      - vendedor (id taquillero)
    Retorna: (True, {'ticket_id':..., 'pago_id':...}) o (False, error_str)
    """
    cn = crear_conexion()
    cur = cn.cursor()
    try:
        # 1) insertar pago
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO pago (fechapago, monto, tipo, vendedor)
            VALUES (%s, %s, %s, %s)
        """, (now, transaccion['precio'], transaccion['tipo_pago'], transaccion['vendedor']))
        pago_id = cur.lastrowid

        # 2) insertar ticket
        cur.execute("""
            INSERT INTO ticket (precio, fechaEmision, asiento, viaje, pasajero, tipopasajero, pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (transaccion['precio'], now, transaccion['asiento'], transaccion['viaje'],
              transaccion['pasajero'], transaccion['tipopasajero'], pago_id))
        ticket_id = cur.lastrowid

        # 3) marcar asiento ocupado en viaje_asiento:
        # si ya existe fila en viaje_asiento la actualizamos; si no existe la insertamos.
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
