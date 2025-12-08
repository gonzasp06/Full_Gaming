import mysql.connector
import bcrypt
from database import conectar_base_datos


class UsuarioService:

    def __init__(self):
        # Cada vez que se crea el servicio, se crea la conexión a la BD
        self.conexion = conectar_base_datos()

    
    # CREAR USUARIO
    
    def crear_usuario(self, nombre, apellido, email, contraseña):

        # Cifrar contraseña
        hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor = self.conexion.cursor()
            query = """
                INSERT INTO usuario (nombre, apellido, email, contraseña)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, apellido, email, hashed))
            self.conexion.commit()
            cursor.close()

            return {"ok": True}

        except mysql.connector.Error as error:
            return {"ok": False, "error": str(error)}

    
    # BUSCAR USUARIO POR EMAIL
   
    def buscar_usuario(self, email):

        cursor = self.conexion.cursor()
        query = "SELECT * FROM usuario WHERE email = %s"
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            return {
                "id": usuario[0],
                "nombre": usuario[1],
                "apellido": usuario[2],
                "email": usuario[3],
                "contraseña": usuario[4]  # cifrada
            }
        else:
            return None

    
    # LOGIN
    
    def login(self, email, contraseña):

        usuario = self.buscar_usuario(email)

        if not usuario:
            return None

        # Verificar contraseña cifrada
        if bcrypt.checkpw(contraseña.encode('utf-8'), usuario["contraseña"]):
            return usuario
        else:
            return None
