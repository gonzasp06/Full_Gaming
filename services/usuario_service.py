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
    
    # OBTENER TODOS LOS USUARIOS
    def obtener_todos(self):

        try:
            cursor = self.conexion.cursor()
            query = "SELECT idusuario, nombre, apellido, email, is_admin FROM usuario"
            cursor.execute(query)
            usuarios = cursor.fetchall()
            cursor.close()
            return usuarios
        except Exception as e:
            return []

    # OBTENER USUARIO POR ID
    def obtener_usuario_por_id(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT idusuario, nombre, apellido, email, is_admin, telefono FROM usuario WHERE idusuario = %s"
            cursor.execute(query, (usuario_id,))
            usuario = cursor.fetchone()
            cursor.close()
            if usuario:
                return {
                    "id": usuario[0],
                    "nombre": usuario[1],
                    "apellido": usuario[2],
                    "email": usuario[3],
                    "is_admin": usuario[4],
                    "telefono": usuario[5]
                }
            return None
        except Exception as e:
            return None

    # ACTUALIZAR ROL DE USUARIO
    def actualizar_rol(self, user_id, is_admin):
        try:
            cursor = self.conexion.cursor()
            query = "UPDATE usuario SET is_admin = %s WHERE idusuario = %s"
            cursor.execute(query, (is_admin, user_id))
            self.conexion.commit()
            cursor.close()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ELIMINAR USUARIO
    def eliminar_usuario(self, user_id):
        try:
            cursor = self.conexion.cursor()
            query = "DELETE FROM usuario WHERE idusuario = %s"
            cursor.execute(query, (user_id,))
            self.conexion.commit()
            cursor.close()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # OBTENER PERFIL COMPLETO DEL USUARIO
    def obtener_perfil(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT idusuario, nombre, apellido, email, telefono FROM usuario WHERE idusuario = %s"
            cursor.execute(query, (usuario_id,))
            usuario = cursor.fetchone()
            cursor.close()
            if usuario:
                return {
                    "id": usuario[0],
                    "nombre": usuario[1],
                    "apellido": usuario[2],
                    "email": usuario[3],
                    "telefono": usuario[4]
                }
            return None
        except Exception as e:
            print(f"Error obtener_perfil: {e}")
            return None

    # ACTUALIZAR PERFIL DEL USUARIO
    def actualizar_perfil(self, usuario_id, nombre, apellido, email, telefono):
        try:
            cursor = self.conexion.cursor()
            query = """
                UPDATE usuario 
                SET nombre = %s, apellido = %s, email = %s, telefono = %s 
                WHERE idusuario = %s
            """
            cursor.execute(query, (nombre, apellido, email, telefono, usuario_id))
            self.conexion.commit()
            cursor.close()
            return {"ok": True, "mensaje": "Perfil actualizado correctamente"}
        except mysql.connector.Error as e:
            if e.errno == 1062:  # Duplicate entry
                return {"ok": False, "error": "El email ya está en uso"}
            return {"ok": False, "error": str(e)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # CAMBIAR CONTRASEÑA
    def cambiar_contraseña(self, usuario_id, contraseña_nueva):
        try:
            # Cifrar nueva contraseña
            hashed = bcrypt.hashpw(contraseña_nueva.encode('utf-8'), bcrypt.gensalt())
            
            cursor = self.conexion.cursor()
            query = "UPDATE usuario SET contraseña = %s WHERE idusuario = %s"
            cursor.execute(query, (hashed, usuario_id))
            self.conexion.commit()
            cursor.close()
            return {"ok": True, "mensaje": "Contraseña actualizada correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    