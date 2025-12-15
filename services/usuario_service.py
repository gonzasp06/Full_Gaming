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
                "contraseña": usuario[4],  # cifrada
                "is_admin": usuario[5]  # agregar is_admin
            }
        else:
            return None

    
    # LOGIN
    
    def login(self, email, contraseña):

        usuario = self.buscar_usuario(email)

        if not usuario:
            return None

        # Obtener el hash de la contraseña guardada
        hash_guardado = usuario["contraseña"]
        
        print(f"DEBUG - Tipo de hash_guardado: {type(hash_guardado)}")
        print(f"DEBUG - Valor: {hash_guardado}")
        
        # Asegurar que hash_guardado es bytes
        if isinstance(hash_guardado, bytes):
            pass  # Ya es bytes
        elif isinstance(hash_guardado, str):
            hash_guardado = hash_guardado.encode('utf-8')
        else:
            print(f"Tipo desconocido: {type(hash_guardado)}")
            return None
        
        try:
            # Verificar contraseña
            resultado = bcrypt.checkpw(contraseña.encode('utf-8'), hash_guardado)
            if resultado:
                return usuario
            else:
                return None
        except Exception as e:
            # Si falla bcrypt, es que el hash es inválido
            print(f"Error en bcrypt.checkpw: {e}")
            print(f"Hash type: {type(hash_guardado)}, Hash value: {hash_guardado}")
            return None
    
    
