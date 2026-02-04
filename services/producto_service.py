from database import conectar_base_datos

class ProductoService:
    def __init__(self):
        self.conexion = conectar_base_datos()
    
    def obtener_todos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM catalogo.producto")
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    def obtener_paginados(self, pagina, por_pagina):
        inicio = (pagina - 1) * por_pagina
        cursor = self.conexion.cursor()
        cursor.execute(
            'SELECT * FROM catalogo.producto LIMIT %s, %s',
            (inicio, por_pagina)
        )
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    def filtrar_categoria(self, categoria):
        cursor = self.conexion.cursor()
        cursor.execute(
            'SELECT * FROM catalogo.producto WHERE categoria = %s',
            (categoria,)
        )
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    def obtener_por_id(self, id_producto):
        cursor = self.conexion.cursor()
        cursor.execute(
            'SELECT * FROM catalogo.producto WHERE id = %s',
            (id_producto,)
        )
        producto = cursor.fetchone()
        cursor.close()
        return producto
    
    def agregar_producto(self, nombre, descripcion, categoria, precio, cantidad, ruta_imagen):
        """Inserta un producto en la base de datos y devuelve un dict con el resultado.

        Retorna: {'ok': True} o {'ok': False, 'error': 'mensaje'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                INSERT INTO catalogo.producto (nombre, descripcion, categoria, precio, cantidad, foto)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, descripcion, categoria, precio, cantidad, ruta_imagen))
            self.conexion.commit()
            return {"ok": True}
        except Exception as e:
            # Intentar cerrar el cursor si existe
            try:
                if cursor:
                    cursor.close()
            except:
                pass
            return {"ok": False, "error": str(e)}
        finally:
            try:
                if cursor:
                    cursor.close()
            except:
                pass
    
    def editar_producto(self, id_producto, nombre, descripcion, categoria, precio, cantidad, ruta_imagen):
        cursor = self.conexion.cursor()
        if ruta_imagen is not None:
            consulta = """
                UPDATE catalogo.producto
                SET nombre=%s, descripcion=%s, categoria=%s, precio=%s, cantidad=%s, foto=%s
                WHERE id=%s
            """
            valores = (nombre, descripcion, categoria, precio, cantidad, ruta_imagen, id_producto)
        else:
            consulta = """
                UPDATE catalogo.producto
                SET nombre=%s, descripcion=%s, categoria=%s, precio=%s, cantidad=%s
                WHERE id=%s
            """
            valores = (nombre, descripcion, categoria, precio, cantidad, id_producto)

        cursor.execute(consulta, valores)
        self.conexion.commit()
        cursor.close()
        return True
    
    def eliminar_producto(self, id_producto):
        cursor = self.conexion.cursor()
        try:
            # Primero eliminar los items del pedido que hacen referencia a este producto
            cursor.execute('DELETE FROM catalogo.pedido_items WHERE producto_id = %s', (id_producto,))
            # Luego eliminar el producto
            cursor.execute('DELETE FROM catalogo.producto WHERE id= %s', (id_producto,))
            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            self.conexion.rollback()
            cursor.close()
            raise e
    
    def buscar_productos(self, termino):
        cursor = self.conexion.cursor()
        like = f"%{termino}%"
        consulta = """
            SELECT *
            FROM catalogo.producto
            WHERE nombre LIKE %s
                OR descripcion LIKE %s
                OR categoria LIKE %s
        """
        cursor.execute(consulta, (like, like, like))
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    def restar_stock(self, id_producto, cantidad):
        """Resta stock de un producto"""
        cursor = self.conexion.cursor()
        try:
            consulta = """
                UPDATE catalogo.producto
                SET cantidad = cantidad - %s
                WHERE id = %s AND cantidad >= %s
            """
            cursor.execute(consulta, (cantidad, id_producto, cantidad))
            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            cursor.close()
            return False