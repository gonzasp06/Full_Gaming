from database import conectar_base_datos

class ProductoService:
    def __init__(self):
        self.conexion = conectar_base_datos()
    
    def obtener_todos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM catalogo.productos")
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