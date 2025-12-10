import mysql.connector
from database import conectar_base_datos


class PedidoService:

    def __init__(self):
        self.conexion = conectar_base_datos()

    def crear_pedido(self, usuario_id, email, total, items):
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
            
            # Insertar pedido
            query_pedido = """
                INSERT INTO pedidos (usuario_id, email, total, estado)
                VALUES (%s, %s, %s, 'completado')
            """
            cursor.execute(query_pedido, (usuario_id, email, total))
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
