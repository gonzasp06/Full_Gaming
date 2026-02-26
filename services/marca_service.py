"""
Servicio para gestión de marcas de productos.
Permite CRUD de marcas y búsqueda.
"""
from database import conectar_base_datos


class MarcaService:
    """Gestiona las marcas de productos en la base de datos."""

    def obtener_todas(self):
        """Obtiene todas las marcas ordenadas alfabéticamente."""
        conexion = conectar_base_datos()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_marca, nombre FROM marca ORDER BY nombre ASC")
        marcas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return marcas

    def obtener_por_id(self, id_marca):
        """Obtiene una marca por su ID."""
        conexion = conectar_base_datos()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_marca, nombre FROM marca WHERE id_marca = %s", (id_marca,))
        marca = cursor.fetchone()
        cursor.close()
        conexion.close()
        return marca

    def buscar_por_nombre(self, nombre):
        """Busca una marca por nombre exacto (case-insensitive)."""
        conexion = conectar_base_datos()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_marca, nombre FROM marca WHERE LOWER(nombre) = LOWER(%s)", (nombre,))
        marca = cursor.fetchone()
        cursor.close()
        conexion.close()
        return marca

    def crear_marca(self, nombre):
        """
        Crea una nueva marca. Devuelve el id_marca creado.
        Si la marca ya existe, devuelve el id existente.
        """
        # Primero verificar si ya existe
        existente = self.buscar_por_nombre(nombre)
        if existente:
            return existente['id_marca']

        conexion = conectar_base_datos()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO marca (nombre) VALUES (%s)", (nombre.strip(),))
        conexion.commit()
        id_marca = cursor.lastrowid
        cursor.close()
        conexion.close()
        return id_marca

    def obtener_o_crear(self, nombre):
        """
        Obtiene el id_marca para un nombre. Si no existe, la crea.
        Útil para el flujo de agregar/editar productos.
        """
        if not nombre or not nombre.strip():
            return None
        return self.crear_marca(nombre.strip())

    def eliminar_marca(self, id_marca):
        """
        Elimina una marca. Los productos que la tenían quedarán con id_marca = NULL.
        Esto ocurre automáticamente por ON DELETE SET NULL.
        """
        conexion = conectar_base_datos()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM marca WHERE id_marca = %s", (id_marca,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        conexion.close()
        return filas_afectadas > 0

    def actualizar_marca(self, id_marca, nuevo_nombre):
        """Actualiza el nombre de una marca existente."""
        conexion = conectar_base_datos()
        cursor = conexion.cursor()
        cursor.execute("UPDATE marca SET nombre = %s WHERE id_marca = %s", (nuevo_nombre.strip(), id_marca))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        conexion.close()
        return filas_afectadas > 0

    def obtener_marcas_en_uso(self):
        """Obtiene solo las marcas que tienen productos asociados."""
        conexion = conectar_base_datos()
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT m.id_marca, m.nombre, COUNT(p.id) as cantidad_productos
            FROM marca m
            INNER JOIN producto p ON p.id_marca = m.id_marca
            GROUP BY m.id_marca, m.nombre
            ORDER BY m.nombre ASC
        """
        cursor.execute(query)
        marcas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return marcas
