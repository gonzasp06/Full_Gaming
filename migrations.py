"""
Script para manejar migraciones de base de datos
Ejecutar una sola vez al inicio de la aplicación
"""
from database import conectar_base_datos

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

if __name__ == "__main__":
    agregar_columna_costo_si_no_existe()
