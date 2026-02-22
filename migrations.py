"""
Script para manejar migraciones de base de datos
Ejecutar una sola vez al inicio de la aplicación
"""
from database import conectar_base_datos


def _columna_existe(cursor, tabla, columna):
    query = """
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'catalogo'
        AND TABLE_NAME = %s
        AND COLUMN_NAME = %s
    """
    cursor.execute(query, (tabla, columna))
    return cursor.fetchone() is not None


def _tabla_existe(cursor, tabla):
    query = """
        SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'catalogo'
        AND TABLE_NAME = %s
    """
    cursor.execute(query, (tabla,))
    return cursor.fetchone() is not None

def agregar_columna_costo_si_no_existe():
    """Agrega la columna 'costo' a la tabla producto si no existe"""
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()
        
        # Verificar si la columna existe
        verificar_query = """
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'catalogo' 
            AND TABLE_NAME = 'producto' 
            AND COLUMN_NAME = 'costo'
        """
        
        cursor.execute(verificar_query)
        resultado = cursor.fetchone()
        
        if not resultado:
            # La columna no existe, la agregamos
            print("Agregando columna 'costo' a tabla 'producto'...")
            alter_query = """
                ALTER TABLE producto ADD COLUMN costo DECIMAL(10,2) DEFAULT 0
            """
            cursor.execute(alter_query)
            conexion.commit()
            print("✓ Columna 'costo' agregada exitosamente")
        else:
            print("✓ La columna 'costo' ya existe en la tabla 'producto'")
        
        cursor.close()
        conexion.close()
        return True
        
    except Exception as e:
        print(f"⚠ Error al agregar columna 'costo': {str(e)}")
        print("⚠ Por favor ejecuta manualmente este SQL:")
        print("  ALTER TABLE producto ADD COLUMN costo DECIMAL(10,2) DEFAULT 0;")
        return False


def crear_tabla_stock_compras_si_no_existe():
    """Crea la tabla de compras de stock (egresos) con FKs a producto y usuario"""
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        if _tabla_existe(cursor, 'stock_compras'):
            print("✓ La tabla 'stock_compras' ya existe")
            cursor.close()
            conexion.close()
            return True

        print("Creando tabla 'stock_compras'...")
        create_query = """
            CREATE TABLE stock_compras (
                id INT NOT NULL AUTO_INCREMENT,
                producto_id INT NOT NULL,
                usuario_id INT DEFAULT NULL,
                inversion_total DECIMAL(12,2) NOT NULL,
                cantidad_unidades INT NOT NULL,
                costo_unitario DECIMAL(12,2) NOT NULL,
                precio_venta_sugerido DECIMAL(12,2) DEFAULT NULL,
                porcentaje_ganancia DECIMAL(8,2) DEFAULT 0,
                observacion VARCHAR(255) DEFAULT NULL,
                creado_en TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                KEY idx_stock_compras_producto (producto_id),
                KEY idx_stock_compras_usuario (usuario_id),
                CONSTRAINT fk_stock_compras_producto
                    FOREIGN KEY (producto_id) REFERENCES producto (id),
                CONSTRAINT fk_stock_compras_usuario
                    FOREIGN KEY (usuario_id) REFERENCES usuario (idusuario)
                    ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        cursor.execute(create_query)
        conexion.commit()
        print("✓ Tabla 'stock_compras' creada exitosamente")

        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"⚠ Error al crear tabla 'stock_compras': {str(e)}")
        return False


def agregar_columnas_costos_pedido_items_si_no_existen():
    """Agrega columnas de costos reales por ítem vendido"""
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        cambios = []
        if not _columna_existe(cursor, 'pedido_items', 'costo_unitario_aplicado'):
            cambios.append("ADD COLUMN costo_unitario_aplicado DECIMAL(12,2) DEFAULT NULL")
        if not _columna_existe(cursor, 'pedido_items', 'costo_total'):
            cambios.append("ADD COLUMN costo_total DECIMAL(12,2) DEFAULT NULL")
        if not _columna_existe(cursor, 'pedido_items', 'ganancia_item'):
            cambios.append("ADD COLUMN ganancia_item DECIMAL(12,2) DEFAULT NULL")

        if cambios:
            print("Agregando columnas de costos a 'pedido_items'...")
            alter_query = "ALTER TABLE pedido_items " + ", ".join(cambios)
            cursor.execute(alter_query)
            conexion.commit()
            print("✓ Columnas de costos agregadas en 'pedido_items'")
        else:
            print("✓ Las columnas de costos ya existen en 'pedido_items'")

        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"⚠ Error al agregar columnas de costos en pedido_items: {str(e)}")
        return False

def agregar_columna_fecha_creacion_usuario_si_no_existe():
    """Agrega la columna 'fecha_creacion' a la tabla usuario si no existe"""
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        verificar_query = """
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'catalogo'
            AND TABLE_NAME = 'usuario'
            AND COLUMN_NAME = 'fecha_creacion'
        """

        cursor.execute(verificar_query)
        resultado = cursor.fetchone()

        if not resultado:
            print("Agregando columna 'fecha_creacion' a tabla 'usuario'...")
            alter_query = """
                ALTER TABLE usuario
                ADD COLUMN fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            """
            cursor.execute(alter_query)
            conexion.commit()
            print("✓ Columna 'fecha_creacion' agregada exitosamente")
        else:
            print("✓ La columna 'fecha_creacion' ya existe en la tabla 'usuario'")

        cursor.close()
        conexion.close()
        return True

    except Exception as e:
        print(f"⚠ Error al agregar columna 'fecha_creacion': {str(e)}")
        print("⚠ Por favor ejecuta manualmente este SQL:")
        print("  ALTER TABLE usuario ADD COLUMN fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP;")
        return False

if __name__ == "__main__":
    agregar_columna_costo_si_no_existe()
    agregar_columna_fecha_creacion_usuario_si_no_existe()
    crear_tabla_stock_compras_si_no_existe()
    agregar_columnas_costos_pedido_items_si_no_existen()
