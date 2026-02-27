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


def crear_tabla_marca_si_no_existe():
    """Crea la tabla marca para categorizar productos por fabricante"""
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        if _tabla_existe(cursor, 'marca'):
            print("✓ La tabla 'marca' ya existe")
            cursor.close()
            conexion.close()
            return True

        print("Creando tabla 'marca'...")
        create_query = """
            CREATE TABLE marca (
                id_marca INT NOT NULL AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                PRIMARY KEY (id_marca),
                UNIQUE KEY unique_nombre_marca (nombre)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        cursor.execute(create_query)
        conexion.commit()
        print("✓ Tabla 'marca' creada exitosamente")

        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"⚠ Error al crear tabla 'marca': {str(e)}")
        return False


def agregar_columna_id_marca_producto_si_no_existe():
    """Agrega la columna id_marca (nullable) a producto y crea la FK"""
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        # Primero verificar que exista la tabla marca
        if not _tabla_existe(cursor, 'marca'):
            print("⚠ La tabla 'marca' no existe. Ejecutá primero crear_tabla_marca_si_no_existe()")
            cursor.close()
            conexion.close()
            return False

        # Verificar si la columna ya existe
        if _columna_existe(cursor, 'producto', 'id_marca'):
            print("✓ La columna 'id_marca' ya existe en 'producto'")
            cursor.close()
            conexion.close()
            return True

        print("Agregando columna 'id_marca' a tabla 'producto'...")
        
        # Agregar columna nullable
        alter_query = """
            ALTER TABLE producto 
            ADD COLUMN id_marca INT DEFAULT NULL
        """
        cursor.execute(alter_query)
        conexion.commit()
        print("✓ Columna 'id_marca' agregada")

        # Agregar índice
        print("Agregando índice en 'id_marca'...")
        index_query = """
            ALTER TABLE producto 
            ADD INDEX idx_producto_marca (id_marca)
        """
        cursor.execute(index_query)
        conexion.commit()
        print("✓ Índice creado")

        # Agregar FK
        print("Agregando clave foránea producto → marca...")
        fk_query = """
            ALTER TABLE producto 
            ADD CONSTRAINT fk_producto_marca 
            FOREIGN KEY (id_marca) REFERENCES marca(id_marca)
            ON DELETE SET NULL
        """
        cursor.execute(fk_query)
        conexion.commit()
        print("✓ Clave foránea creada exitosamente")

        cursor.close()
        conexion.close()
        return True

    except Exception as e:
        print(f"⚠ Error al agregar columna 'id_marca': {str(e)}")
        return False


def agregar_columnas_recuperacion_usuario_si_no_existen():
    """
    Agrega columnas para recuperación de contraseña en la tabla usuario.
    - codigo_recuperacion: código de 6 dígitos para verificación
    - codigo_expiracion: fecha/hora de expiración del código
    Ambas columnas son nullable para no afectar usuarios existentes.
    """
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        # Verificar y agregar codigo_recuperacion
        if not _columna_existe(cursor, 'usuario', 'codigo_recuperacion'):
            print("Agregando columna 'codigo_recuperacion' a tabla 'usuario'...")
            cursor.execute("""
                ALTER TABLE usuario 
                ADD COLUMN codigo_recuperacion VARCHAR(10) DEFAULT NULL
            """)
            conexion.commit()
            print("✓ Columna 'codigo_recuperacion' agregada")
        else:
            print("✓ La columna 'codigo_recuperacion' ya existe")

        # Verificar y agregar codigo_expiracion
        if not _columna_existe(cursor, 'usuario', 'codigo_expiracion'):
            print("Agregando columna 'codigo_expiracion' a tabla 'usuario'...")
            cursor.execute("""
                ALTER TABLE usuario 
                ADD COLUMN codigo_expiracion DATETIME DEFAULT NULL
            """)
            conexion.commit()
            print("✓ Columna 'codigo_expiracion' agregada")
        else:
            print("✓ La columna 'codigo_expiracion' ya existe")

        cursor.close()
        conexion.close()
        return True

    except Exception as e:
        print(f"⚠ Error al agregar columnas de recuperación: {str(e)}")
        return False


def agregar_columna_token_eliminacion_si_no_existe():
    """
    Agrega columna para token de eliminación de cuenta.
    Permite que usuarios eliminen su cuenta desde el email de bienvenida.
    """
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        if not _columna_existe(cursor, 'usuario', 'token_eliminacion'):
            print("Agregando columna 'token_eliminacion' a tabla 'usuario'...")
            cursor.execute("""
                ALTER TABLE usuario 
                ADD COLUMN token_eliminacion VARCHAR(64) DEFAULT NULL
            """)
            conexion.commit()
            print("✓ Columna 'token_eliminacion' agregada")
        else:
            print("✓ La columna 'token_eliminacion' ya existe")

        cursor.close()
        conexion.close()
        return True

    except Exception as e:
        print(f"⚠ Error al agregar columna token_eliminacion: {str(e)}")
        return False


def crear_tabla_egresos_reales_si_no_existe():
    """
    Crea la tabla egresos_reales para registrar pérdidas no recuperables del negocio:
    fallas de producto, devoluciones, roturas, errores, etc.
    Separada de stock_compras (que es inversión, no pérdida).
    """
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        if _tabla_existe(cursor, 'egresos_reales'):
            print("✓ La tabla 'egresos_reales' ya existe")
            cursor.close()
            conexion.close()
            return True

        print("Creando tabla 'egresos_reales'...")
        create_query = """
            CREATE TABLE egresos_reales (
                id INT NOT NULL AUTO_INCREMENT,
                producto_id INT DEFAULT NULL,
                pedido_id INT DEFAULT NULL,
                tipo ENUM('falla', 'devolucion', 'rotura', 'error', 'otro') NOT NULL DEFAULT 'otro',
                monto DECIMAL(12,2) NOT NULL,
                cantidad INT NOT NULL DEFAULT 1,
                descripcion VARCHAR(500) DEFAULT NULL,
                fecha TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                usuario_id INT DEFAULT NULL,
                PRIMARY KEY (id),
                KEY idx_egresos_reales_producto (producto_id),
                KEY idx_egresos_reales_pedido (pedido_id),
                KEY idx_egresos_reales_tipo (tipo),
                KEY idx_egresos_reales_fecha (fecha),
                CONSTRAINT fk_egresos_reales_producto
                    FOREIGN KEY (producto_id) REFERENCES producto (id)
                    ON DELETE SET NULL,
                CONSTRAINT fk_egresos_reales_usuario
                    FOREIGN KEY (usuario_id) REFERENCES usuario (idusuario)
                    ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        cursor.execute(create_query)
        conexion.commit()
        print("✓ Tabla 'egresos_reales' creada exitosamente")

        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"⚠ Error al crear tabla 'egresos_reales': {str(e)}")
        return False


def crear_tabla_devoluciones_si_no_existe():
    """
    Crea la tabla devoluciones para gestionar solicitudes de devolución/reembolso.
    Relacionada con pedidos, usuarios y administradores.
    """
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        if _tabla_existe(cursor, 'devoluciones'):
            print("✓ La tabla 'devoluciones' ya existe")
            cursor.close()
            conexion.close()
            return True

        print("Creando tabla 'devoluciones'...")
        create_query = """
            CREATE TABLE devoluciones (
                id INT NOT NULL AUTO_INCREMENT,
                pedido_id INT NOT NULL,
                usuario_id INT NOT NULL,
                motivo ENUM('producto_defectuoso','no_coincide','arrepentimiento','otro') NOT NULL DEFAULT 'otro',
                comentarios TEXT DEFAULT NULL,
                estado ENUM('pendiente','aprobada','rechazada') NOT NULL DEFAULT 'pendiente',
                monto_devolucion DECIMAL(12,2) NOT NULL DEFAULT 0,
                fecha_solicitud TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                fecha_resolucion TIMESTAMP NULL DEFAULT NULL,
                admin_id INT DEFAULT NULL,
                motivo_rechazo VARCHAR(500) DEFAULT NULL,
                PRIMARY KEY (id),
                KEY idx_devoluciones_pedido (pedido_id),
                KEY idx_devoluciones_usuario (usuario_id),
                KEY idx_devoluciones_estado (estado),
                KEY idx_devoluciones_fecha (fecha_solicitud),
                CONSTRAINT fk_devoluciones_pedido
                    FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
                    ON DELETE CASCADE,
                CONSTRAINT fk_devoluciones_usuario
                    FOREIGN KEY (usuario_id) REFERENCES usuario (idusuario)
                    ON DELETE CASCADE,
                CONSTRAINT fk_devoluciones_admin
                    FOREIGN KEY (admin_id) REFERENCES usuario (idusuario)
                    ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        cursor.execute(create_query)
        conexion.commit()
        print("✓ Tabla 'devoluciones' creada exitosamente")

        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"⚠ Error al crear tabla 'devoluciones': {str(e)}")
        return False


def crear_tabla_carrito_usuario_si_no_existe():
    """Crea la tabla 'carrito_usuario' para carritos persistentes por usuario"""
    try:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        if _tabla_existe(cursor, 'carrito_usuario'):
            print("✓ La tabla 'carrito_usuario' ya existe")
            cursor.close()
            conexion.close()
            return True

        print("Creando tabla 'carrito_usuario'...")
        create_query = """
            CREATE TABLE carrito_usuario (
                id INT NOT NULL AUTO_INCREMENT,
                usuario_id INT NOT NULL,
                producto_id INT NOT NULL,
                cantidad INT NOT NULL DEFAULT 1,
                fecha_agregado TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizado TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                UNIQUE KEY uk_carrito_usuario_producto (usuario_id, producto_id),
                KEY idx_carrito_usuario (usuario_id),
                CONSTRAINT fk_carrito_usuario
                    FOREIGN KEY (usuario_id) REFERENCES usuario (idusuario)
                    ON DELETE CASCADE,
                CONSTRAINT fk_carrito_producto
                    FOREIGN KEY (producto_id) REFERENCES producto (id)
                    ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        cursor.execute(create_query)
        conexion.commit()
        print("✓ Tabla 'carrito_usuario' creada exitosamente")

        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"⚠ Error al crear tabla 'carrito_usuario': {str(e)}")
        return False


if __name__ == "__main__":
    agregar_columna_costo_si_no_existe()
    agregar_columna_fecha_creacion_usuario_si_no_existe()
    crear_tabla_stock_compras_si_no_existe()
    agregar_columnas_costos_pedido_items_si_no_existen()
    agregar_columnas_recuperacion_usuario_si_no_existen()
    agregar_columna_token_eliminacion_si_no_existe()
    crear_tabla_egresos_reales_si_no_existe()
    crear_tabla_devoluciones_si_no_existe()
    crear_tabla_carrito_usuario_si_no_existe()
