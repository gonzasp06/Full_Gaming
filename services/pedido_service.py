import mysql.connector
from database import conectar_base_datos


class PedidoService:

    def __init__(self):
        self.conexion = conectar_base_datos()

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
                query_item = """
                    INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_item, (
                    pedido_id,
                    item['producto_id'],
                    item['cantidad'],
                    item['precio'],
                    item['subtotal']
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