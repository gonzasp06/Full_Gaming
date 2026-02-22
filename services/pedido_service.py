import mysql.connector
from database import conectar_base_datos
from services.negocio_models import Venta


class PedidoService:

    def __init__(self):
        self.conexion = conectar_base_datos()

    def _columna_existe(self, tabla, columna):
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT COUNT(*)
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = %s
                  AND COLUMN_NAME = %s
            """
            cursor.execute(query, (tabla, columna))
            resultado = cursor.fetchone()
            cursor.close()
            return bool(resultado and resultado[0] > 0)
        except Exception:
            if cursor:
                cursor.close()
            return False

    def _obtener_costos_unitarios_productos(self, producto_ids):
        if not producto_ids:
            return {}

        cursor = self.conexion.cursor()
        placeholders = ",".join(["%s"] * len(producto_ids))
        query = f"SELECT id, COALESCE(costo, 0) FROM producto WHERE id IN ({placeholders})"
        cursor.execute(query, tuple(producto_ids))
        filas = cursor.fetchall()
        cursor.close()
        return {int(row[0]): float(row[1] or 0) for row in filas}

    def crear_pedido(self, usuario_id, email, total, items, direccion=None, provincia=None, codigo_postal=None, dni=None, telefono=None):
        """
        Crea un pedido y sus items en BD
        
        items: lista de dicts con:
            - producto_id
            - cantidad
            - precio
            - subtotal
        
        Retorna: {'ok': True, 'pedido_id': X} o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            columnas_costos_disponibles = (
                self._columna_existe('pedido_items', 'costo_unitario_aplicado')
                and self._columna_existe('pedido_items', 'costo_total')
                and self._columna_existe('pedido_items', 'ganancia_item')
            )

            costos_por_producto = self._obtener_costos_unitarios_productos(
                [int(item['producto_id']) for item in items]
            )
            
            # Insertar pedido con todos los datos
            query_pedido = """
                INSERT INTO pedidos (usuario_id, email, total, estado, direccion, provincia, codigo_postal, dni, telefono)
                VALUES (%s, %s, %s, 'completado', %s, %s, %s, %s, %s)
            """
            cursor.execute(query_pedido, (usuario_id, email, total, direccion, provincia, codigo_postal, dni, telefono))
            self.conexion.commit()
            
            pedido_id = cursor.lastrowid
            
            # Insertar items
            for item in items:
                producto_id = int(item['producto_id'])
                cantidad = int(item['cantidad'])
                precio_unitario = float(item['precio'])
                subtotal = float(item['subtotal'])
                costo_unitario = float(costos_por_producto.get(producto_id, 0))

                venta = Venta(
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    costo_unitario=costo_unitario,
                )

                if columnas_costos_disponibles:
                    query_item = """
                        INSERT INTO pedido_items (
                            pedido_id,
                            producto_id,
                            cantidad,
                            precio,
                            subtotal,
                            costo_unitario_aplicado,
                            costo_total,
                            ganancia_item
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_item, (
                        pedido_id,
                        producto_id,
                        cantidad,
                        int(precio_unitario),
                        int(subtotal),
                        round(costo_unitario, 2),
                        round(venta.costo_total(), 2),
                        round(venta.ganancia_real(), 2)
                    ))
                else:
                    query_item = """
                        INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio, subtotal)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_item, (
                        pedido_id,
                        producto_id,
                        cantidad,
                        int(precio_unitario),
                        int(subtotal)
                    ))
            
            self.conexion.commit()
            cursor.close()
            
            return {"ok": True, "pedido_id": pedido_id}
            
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    def obtener_pedidos_recientes(self, usuario_id, limite=5):
        """
        Obtiene los últimos pedidos de un usuario
        
        Args:
            usuario_id: ID del usuario
            limite: cantidad de pedidos a retornar (default 5)
        
        Retorna: lista de dicts con los pedidos
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            
            query = """
                SELECT id, usuario_id, email, total, estado, fecha
                FROM pedidos
                WHERE usuario_id = %s
                ORDER BY fecha DESC
                LIMIT %s
            """
            cursor.execute(query, (usuario_id, limite))
            pedidos = cursor.fetchall()
            cursor.close()
            
            resultado = []
            for pedido in pedidos:
                # Formatear fecha: si es datetime, convertir a string DD/MM/YYYY
                fecha_str = 'N/A'
                if pedido[5]:
                    if hasattr(pedido[5], 'strftime'):
                        fecha_str = pedido[5].strftime('%d/%m/%Y')
                    else:
                        fecha_str = str(pedido[5])
                
                resultado.append({
                    "id": pedido[0],
                    "usuario_id": pedido[1],
                    "email": pedido[2],
                    "total": pedido[3],
                    "estado": pedido[4],
                    "fecha": fecha_str
                })
            
            return resultado
        except Exception as e:
            print(f"Error obtener_pedidos_recientes: {e}")
            return []