import bcrypt
import mysql.connector
from database import conectar_base_datos

# Datos del admin
email = "bauti@admin.com"
contraseña = "12345"
nombre = "Bautista"
apellido = "Riveira"

# Encriptar contraseña
hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

# Conectar a BD
conexion = conectar_base_datos()
cursor = conexion.cursor()

try:
    # Insertar admin
    query = """
        INSERT INTO usuario (nombre, apellido, email, contraseña, is_admin)
        VALUES (%s, %s, %s, %s, 1)
    """
    cursor.execute(query, (nombre, apellido, email, hashed))
    conexion.commit()
    print("✅ Admin creado correctamente")
    print(f"Email: {email}")
    print(f"Contraseña: {contraseña}")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    cursor.close()
    conexion.close()
