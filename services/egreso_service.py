"""
Servicio para gestionar egresos reales (pérdidas no recuperables):
fallas, devoluciones, roturas, errores, etc.
Separado de la inversión en stock (stock_compras).
"""
import mysql.connector
from database import conectar_base_datos
from datetime import datetime, timedelta


class EgresoService:
    """Gestiona los egresos reales del negocio"""

    TIPOS_VALIDOS = ['falla', 'devolucion', 'rotura', 'error', 'otro']

    def __init__(self):
        self.conexion = conectar_base_datos()

    def _tabla_existe(self):
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT COUNT(*)
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'egresos_reales'
            """
            cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            return bool(resultado and resultado[0] > 0)
        except Exception:
            if cursor:
                cursor.close()
            return False

    def registrar_egreso(self, tipo, monto, cantidad=1, descripcion=None,
                         producto_id=None, pedido_id=None, usuario_id=None):
        """
        Registra un egreso real (pérdida no recuperable).

        Args:
            tipo: 'falla' | 'devolucion' | 'rotura' | 'error' | 'otro'
            monto: monto total de la pérdida
            cantidad: cantidad de unidades afectadas
            descripcion: texto descriptivo de la pérdida
            producto_id: (opcional) producto relacionado
            pedido_id: (opcional) pedido relacionado
            usuario_id: (opcional) admin que registró

        Returns:
            dict con ok y id del egreso creado
        """
        if tipo not in self.TIPOS_VALIDOS:
            return {"ok": False, "error": f"Tipo inválido. Tipos permitidos: {', '.join(self.TIPOS_VALIDOS)}"}

        if monto <= 0:
            return {"ok": False, "error": "El monto debe ser mayor a 0"}

        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            # Si hay producto asociado, descontar stock
            if producto_id and cantidad > 0:
                cursor.execute("SELECT cantidad FROM producto WHERE id = %s", (producto_id,))
                prod = cursor.fetchone()
                if prod:
                    stock_actual = int(prod[0]) if prod[0] else 0
                    nuevo_stock = max(0, stock_actual - cantidad)
                    cursor.execute("UPDATE producto SET cantidad = %s WHERE id = %s", (nuevo_stock, producto_id))

            query = """
                INSERT INTO egresos_reales 
                    (producto_id, pedido_id, tipo, monto, cantidad, descripcion, usuario_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                producto_id, pedido_id, tipo, monto, cantidad, descripcion, usuario_id
            ))
            conexion.commit()
            egreso_id = cursor.lastrowid
            cursor.close()
            conexion.close()

            return {"ok": True, "id": egreso_id, "mensaje": "Egreso registrado y stock actualizado"}

        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}

    def obtener_egresos_acumulados(self):
        """
        Total acumulado de egresos reales (pérdidas).
        """
        cursor = None
        try:
            if not self._tabla_existe():
                return {"ok": True, "egresos_reales": 0}

            conexion = conectar_base_datos()
            cursor = conexion.cursor()
            query = "SELECT COALESCE(SUM(monto), 0) FROM egresos_reales"
            cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            return {"ok": True, "egresos_reales": int(resultado[0]) if resultado and resultado[0] else 0}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}

    def obtener_egresos_por_mes(self, cantidad_meses=12):
        """
        Egresos reales agrupados por mes para el gráfico.
        """
        try:
            if not self._tabla_existe():
                return {"ok": True, "datos": {}}

            conexion = conectar_base_datos()
            cursor = conexion.cursor()
            query = """
                SELECT
                    YEAR(fecha) AS anio,
                    MONTH(fecha) AS numero_mes,
                    COALESCE(SUM(monto), 0) AS total_egresos
                FROM egresos_reales
                WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
                GROUP BY YEAR(fecha), MONTH(fecha)
            """
            cursor.execute(query, (cantidad_meses,))
            datos = {(row[0], row[1]): row[2] for row in cursor.fetchall()}
            cursor.close()
            conexion.close()
            return {"ok": True, "datos": datos}
        except Exception as e:
            return {"ok": False, "error": str(e), "datos": {}}

    def obtener_egresos_por_tipo(self):
        """
        Resumen de egresos agrupados por tipo.
        """
        cursor = None
        try:
            if not self._tabla_existe():
                return {"ok": True, "tipos": []}

            conexion = conectar_base_datos()
            cursor = conexion.cursor()
            query = """
                SELECT tipo, COUNT(*) as cantidad, COALESCE(SUM(monto), 0) as total
                FROM egresos_reales
                GROUP BY tipo
                ORDER BY total DESC
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()

            tipos = []
            for row in resultados:
                tipos.append({
                    "tipo": row[0],
                    "cantidad": int(row[1]),
                    "total": int(row[2])
                })

            return {"ok": True, "tipos": tipos}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}

    def obtener_listado_egresos(self, limite=50):
        """
        Lista los últimos egresos registrados con detalle.
        """
        cursor = None
        try:
            if not self._tabla_existe():
                return {"ok": True, "egresos": []}

            conexion = conectar_base_datos()
            cursor = conexion.cursor()
            query = """
                SELECT 
                    e.id, e.tipo, e.monto, e.cantidad, e.descripcion, e.fecha,
                    p.nombre AS producto_nombre,
                    e.pedido_id,
                    e.producto_id
                FROM egresos_reales e
                LEFT JOIN producto p ON e.producto_id = p.id
                ORDER BY e.fecha DESC
                LIMIT %s
            """
            cursor.execute(query, (limite,))
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()

            egresos = []
            for row in resultados:
                egresos.append({
                    "id": row[0],
                    "tipo": row[1],
                    "monto": int(row[2]) if row[2] else 0,
                    "cantidad": int(row[3]) if row[3] else 1,
                    "descripcion": row[4] or "",
                    "fecha": row[5].strftime('%d/%m/%Y %H:%M') if row[5] else "",
                    "producto": row[6] or "Sin producto",
                    "pedido_id": row[7],
                    "producto_id": row[8]
                })

            return {"ok": True, "egresos": egresos}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}

    def eliminar_egreso(self, egreso_id):
        """Elimina un egreso por ID"""
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM egresos_reales WHERE id = %s", (egreso_id,))
            conexion.commit()
            eliminados = cursor.rowcount
            cursor.close()
            conexion.close()

            if eliminados > 0:
                return {"ok": True, "mensaje": "Egreso eliminado"}
            else:
                return {"ok": False, "error": "Egreso no encontrado"}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}

    def actualizar_egreso(self, egreso_id, tipo=None, monto=None, cantidad=None,
                          descripcion=None, producto_id=None):
        """
        Actualiza un egreso existente.
        Solo modifica los campos que se envíen (no None).
        """
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            # Verificar que existe
            cursor.execute("SELECT id FROM egresos_reales WHERE id = %s", (egreso_id,))
            if not cursor.fetchone():
                cursor.close()
                conexion.close()
                return {"ok": False, "error": "Egreso no encontrado"}

            campos = []
            valores = []

            if tipo is not None and tipo in self.TIPOS_VALIDOS:
                campos.append("tipo = %s")
                valores.append(tipo)
            if monto is not None:
                if float(monto) <= 0:
                    cursor.close()
                    conexion.close()
                    return {"ok": False, "error": "El monto debe ser mayor a 0"}
                campos.append("monto = %s")
                valores.append(float(monto))
            if cantidad is not None:
                campos.append("cantidad = %s")
                valores.append(int(cantidad))
            if descripcion is not None:
                campos.append("descripcion = %s")
                valores.append(descripcion)
            if producto_id is not None:
                campos.append("producto_id = %s")
                valores.append(producto_id if producto_id else None)

            if not campos:
                cursor.close()
                conexion.close()
                return {"ok": False, "error": "No hay campos para actualizar"}

            valores.append(egreso_id)
            query = f"UPDATE egresos_reales SET {', '.join(campos)} WHERE id = %s"
            cursor.execute(query, tuple(valores))
            conexion.commit()
            cursor.close()
            conexion.close()

            return {"ok": True, "mensaje": "Egreso actualizado correctamente"}

        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
