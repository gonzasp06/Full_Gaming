"""
Servicio para gestionar devoluciones y reembolsos.
Maneja solicitudes de usuarios, aprobación/rechazo por admin,
y registra egresos reales cuando se aprueba una devolución.
"""
import mysql.connector
from database import conectar_base_datos
from datetime import datetime


class DevolucionService:
    """Gestiona el ciclo de vida completo de devoluciones"""

    MOTIVOS_VALIDOS = ['producto_defectuoso', 'no_coincide', 'arrepentimiento', 'otro']
    MOTIVOS_LABELS = {
        'producto_defectuoso': 'Producto defectuoso',
        'no_coincide': 'No coincide con la descripción',
        'arrepentimiento': 'Arrepentimiento de compra',
        'otro': 'Otro motivo'
    }

    # ======================== SOLICITUDES DE USUARIO ========================

    def solicitar_devolucion(self, pedido_id, usuario_id, motivo, comentarios=None):
        """
        Crea una solicitud de devolución para un pedido.
        Solo si el pedido pertenece al usuario y está en estado 'completado'.
        No permite duplicados (un pedido solo puede tener una devolución activa).
        """
        if motivo not in self.MOTIVOS_VALIDOS:
            return {"ok": False, "error": f"Motivo inválido. Motivos permitidos: {', '.join(self.MOTIVOS_VALIDOS)}"}

        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            # Verificar que el pedido pertenece al usuario y está completado
            cursor.execute(
                "SELECT id, total, estado FROM pedidos WHERE id = %s AND usuario_id = %s",
                (pedido_id, usuario_id)
            )
            pedido = cursor.fetchone()

            if not pedido:
                cursor.close()
                conexion.close()
                return {"ok": False, "error": "Pedido no encontrado o no te pertenece"}

            if pedido[2] != 'completado':
                cursor.close()
                conexion.close()
                return {"ok": False, "error": "Solo se pueden devolver pedidos completados"}

            # Verificar que no exista una devolución activa para este pedido
            cursor.execute(
                "SELECT id, estado FROM devoluciones WHERE pedido_id = %s AND estado IN ('pendiente', 'aprobada')",
                (pedido_id,)
            )
            devolucion_existente = cursor.fetchone()

            if devolucion_existente:
                cursor.close()
                conexion.close()
                estado_existente = devolucion_existente[1]
                if estado_existente == 'pendiente':
                    return {"ok": False, "error": "Ya existe una solicitud de devolución pendiente para este pedido"}
                else:
                    return {"ok": False, "error": "Este pedido ya fue devuelto"}

            monto_devolucion = float(pedido[1])

            # Crear la solicitud de devolución
            query = """
                INSERT INTO devoluciones (pedido_id, usuario_id, motivo, comentarios, estado, monto_devolucion)
                VALUES (%s, %s, %s, %s, 'pendiente', %s)
            """
            cursor.execute(query, (pedido_id, usuario_id, motivo, comentarios, monto_devolucion))

            # Actualizar estado del pedido
            cursor.execute(
                "UPDATE pedidos SET estado = 'devolucion_pendiente' WHERE id = %s",
                (pedido_id,)
            )

            conexion.commit()
            devolucion_id = cursor.lastrowid
            cursor.close()
            conexion.close()

            return {
                "ok": True,
                "id": devolucion_id,
                "mensaje": "Solicitud de devolución enviada correctamente. Te notificaremos por email."
            }

        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}

    def obtener_devoluciones_usuario(self, usuario_id):
        """Obtiene todas las devoluciones de un usuario"""
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            query = """
                SELECT d.id, d.pedido_id, d.motivo, d.comentarios, d.estado,
                       d.monto_devolucion, d.fecha_solicitud, d.fecha_resolucion,
                       d.motivo_rechazo, p.total
                FROM devoluciones d
                JOIN pedidos p ON d.pedido_id = p.id
                WHERE d.usuario_id = %s
                ORDER BY d.fecha_solicitud DESC
            """
            cursor.execute(query, (usuario_id,))
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()

            devoluciones = []
            for row in resultados:
                devoluciones.append({
                    "id": row[0],
                    "pedido_id": row[1],
                    "motivo": row[2],
                    "motivo_label": self.MOTIVOS_LABELS.get(row[2], row[2]),
                    "comentarios": row[3] or "",
                    "estado": row[4],
                    "monto_devolucion": int(row[5]) if row[5] else 0,
                    "fecha_solicitud": row[6].strftime('%d/%m/%Y %H:%M') if row[6] else "",
                    "fecha_resolucion": row[7].strftime('%d/%m/%Y %H:%M') if row[7] else "",
                    "motivo_rechazo": row[8] or "",
                    "total_pedido": int(row[9]) if row[9] else 0
                })

            return devoluciones

        except Exception as e:
            print(f"Error obtener_devoluciones_usuario: {e}")
            if cursor:
                cursor.close()
            return []

    def obtener_devolucion_por_pedido(self, pedido_id):
        """Obtiene la devolución asociada a un pedido (si existe)"""
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT id, estado, motivo, fecha_solicitud FROM devoluciones WHERE pedido_id = %s ORDER BY id DESC LIMIT 1",
                (pedido_id,)
            )
            row = cursor.fetchone()
            cursor.close()
            conexion.close()

            if row:
                return {
                    "id": row[0],
                    "estado": row[1],
                    "motivo": row[2],
                    "fecha_solicitud": row[3].strftime('%d/%m/%Y %H:%M') if row[3] else ""
                }
            return None

        except Exception as e:
            if cursor:
                cursor.close()
            return None

    # ======================== ADMINISTRACIÓN ========================

    def contar_pendientes(self):
        """Cuenta las devoluciones pendientes (para badge de notificación)"""
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM devoluciones WHERE estado = 'pendiente'")
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            return resultado[0] if resultado else 0
        except Exception as e:
            if cursor:
                cursor.close()
            return 0

    def obtener_devoluciones_pendientes(self):
        """Obtiene todas las devoluciones pendientes con datos del usuario y pedido"""
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            query = """
                SELECT d.id, d.pedido_id, d.motivo, d.comentarios, d.estado,
                       d.monto_devolucion, d.fecha_solicitud,
                       u.nombre AS usuario_nombre, u.email AS usuario_email,
                       p.total AS pedido_total, p.fecha AS pedido_fecha
                FROM devoluciones d
                JOIN usuario u ON d.usuario_id = u.idusuario
                JOIN pedidos p ON d.pedido_id = p.id
                WHERE d.estado = 'pendiente'
                ORDER BY d.fecha_solicitud ASC
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()

            devoluciones = []
            for row in resultados:
                devoluciones.append({
                    "id": row[0],
                    "pedido_id": row[1],
                    "motivo": row[2],
                    "motivo_label": self.MOTIVOS_LABELS.get(row[2], row[2]),
                    "comentarios": row[3] or "",
                    "estado": row[4],
                    "monto_devolucion": int(row[5]) if row[5] else 0,
                    "fecha_solicitud": row[6].strftime('%d/%m/%Y %H:%M') if row[6] else "",
                    "usuario_nombre": row[7],
                    "usuario_email": row[8],
                    "pedido_total": int(row[9]) if row[9] else 0,
                    "pedido_fecha": row[10].strftime('%d/%m/%Y') if row[10] else ""
                })

            return devoluciones

        except Exception as e:
            print(f"Error obtener_devoluciones_pendientes: {e}")
            if cursor:
                cursor.close()
            return []

    def obtener_todas_devoluciones(self, limite=50):
        """Obtiene todas las devoluciones (historial completo) para el admin"""
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            query = """
                SELECT d.id, d.pedido_id, d.motivo, d.comentarios, d.estado,
                       d.monto_devolucion, d.fecha_solicitud, d.fecha_resolucion,
                       d.motivo_rechazo,
                       u.nombre AS usuario_nombre, u.email AS usuario_email,
                       p.total AS pedido_total
                FROM devoluciones d
                JOIN usuario u ON d.usuario_id = u.idusuario
                JOIN pedidos p ON d.pedido_id = p.id
                ORDER BY d.fecha_solicitud DESC
                LIMIT %s
            """
            cursor.execute(query, (limite,))
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()

            devoluciones = []
            for row in resultados:
                devoluciones.append({
                    "id": row[0],
                    "pedido_id": row[1],
                    "motivo": row[2],
                    "motivo_label": self.MOTIVOS_LABELS.get(row[2], row[2]),
                    "comentarios": row[3] or "",
                    "estado": row[4],
                    "monto_devolucion": int(row[5]) if row[5] else 0,
                    "fecha_solicitud": row[6].strftime('%d/%m/%Y %H:%M') if row[6] else "",
                    "fecha_resolucion": row[7].strftime('%d/%m/%Y %H:%M') if row[7] else "",
                    "motivo_rechazo": row[8] or "",
                    "usuario_nombre": row[9],
                    "usuario_email": row[10],
                    "pedido_total": int(row[11]) if row[11] else 0
                })

            return devoluciones

        except Exception as e:
            print(f"Error obtener_todas_devoluciones: {e}")
            if cursor:
                cursor.close()
            return []

    def aprobar_devolucion(self, devolucion_id, admin_id):
        """
        Aprueba una devolución: actualiza estado, registra fecha,
        actualiza pedido y registra egreso real automáticamente.
        """
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            # Obtener datos de la devolución
            cursor.execute(
                """SELECT d.id, d.pedido_id, d.usuario_id, d.monto_devolucion, d.estado,
                          u.email, u.nombre
                   FROM devoluciones d
                   JOIN usuario u ON d.usuario_id = u.idusuario
                   WHERE d.id = %s""",
                (devolucion_id,)
            )
            devolucion = cursor.fetchone()

            if not devolucion:
                cursor.close()
                conexion.close()
                return {"ok": False, "error": "Devolución no encontrada"}

            if devolucion[4] != 'pendiente':
                cursor.close()
                conexion.close()
                return {"ok": False, "error": "Esta devolución ya fue procesada"}

            pedido_id = devolucion[1]
            usuario_id = devolucion[2]
            monto = float(devolucion[3])
            email_usuario = devolucion[5]
            nombre_usuario = devolucion[6]

            # Actualizar devolución
            cursor.execute(
                """UPDATE devoluciones 
                   SET estado = 'aprobada', fecha_resolucion = NOW(), admin_id = %s
                   WHERE id = %s""",
                (admin_id, devolucion_id)
            )

            # Actualizar estado del pedido
            cursor.execute(
                "UPDATE pedidos SET estado = 'devuelto' WHERE id = %s",
                (pedido_id,)
            )

            conexion.commit()
            cursor.close()
            conexion.close()

            # Registrar egreso real (usando el servicio existente)
            from services.egreso_service import EgresoService
            egreso_service = EgresoService()

            # Obtener primer producto del pedido para asociar el egreso
            try:
                conexion2 = conectar_base_datos()
                cursor2 = conexion2.cursor()
                cursor2.execute(
                    "SELECT producto_id, cantidad FROM pedido_items WHERE pedido_id = %s LIMIT 1",
                    (pedido_id,)
                )
                item = cursor2.fetchone()
                producto_id = item[0] if item else None
                cantidad = item[1] if item else 1
                cursor2.close()
                conexion2.close()
            except Exception:
                producto_id = None
                cantidad = 1

            egreso_service.registrar_egreso(
                tipo='devolucion',
                monto=monto,
                cantidad=cantidad,
                descripcion=f"Devolución aprobada - Pedido #{pedido_id} - Cliente: {nombre_usuario}",
                producto_id=producto_id,
                pedido_id=pedido_id,
                usuario_id=admin_id
            )

            return {
                "ok": True,
                "mensaje": "Devolución aprobada correctamente",
                "email_usuario": email_usuario,
                "nombre_usuario": nombre_usuario,
                "pedido_id": pedido_id,
                "monto": monto
            }

        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}

    def rechazar_devolucion(self, devolucion_id, admin_id, motivo_rechazo=None):
        """
        Rechaza una devolución. El pedido vuelve a estado 'completado'.
        """
        cursor = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            # Obtener datos de la devolución
            cursor.execute(
                """SELECT d.id, d.pedido_id, d.estado,
                          u.email, u.nombre
                   FROM devoluciones d
                   JOIN usuario u ON d.usuario_id = u.idusuario
                   WHERE d.id = %s""",
                (devolucion_id,)
            )
            devolucion = cursor.fetchone()

            if not devolucion:
                cursor.close()
                conexion.close()
                return {"ok": False, "error": "Devolución no encontrada"}

            if devolucion[2] != 'pendiente':
                cursor.close()
                conexion.close()
                return {"ok": False, "error": "Esta devolución ya fue procesada"}

            pedido_id = devolucion[1]
            email_usuario = devolucion[3]
            nombre_usuario = devolucion[4]

            # Actualizar devolución
            cursor.execute(
                """UPDATE devoluciones 
                   SET estado = 'rechazada', fecha_resolucion = NOW(), admin_id = %s, motivo_rechazo = %s
                   WHERE id = %s""",
                (admin_id, motivo_rechazo, devolucion_id)
            )

            # Restaurar estado del pedido
            cursor.execute(
                "UPDATE pedidos SET estado = 'completado' WHERE id = %s",
                (pedido_id,)
            )

            conexion.commit()
            cursor.close()
            conexion.close()

            return {
                "ok": True,
                "mensaje": "Devolución rechazada",
                "email_usuario": email_usuario,
                "nombre_usuario": nombre_usuario,
                "pedido_id": pedido_id
            }

        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
