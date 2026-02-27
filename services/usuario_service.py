import mysql.connector
import bcrypt
import random
from datetime import datetime, timedelta
from database import conectar_base_datos


class UsuarioService:

    def __init__(self):
        # Cada vez que se crea el servicio, se crea la conexión a la BD
        self.conexion = conectar_base_datos()

    
    # CREAR USUARIO
    
    def crear_usuario(self, nombre, apellido, email, contraseña):
        email = email.strip().lower()
        # Validar que el email no exista ya
        usuario_existente = self.buscar_usuario(email)
        if usuario_existente:
            return {"ok": False, "error": "El correo ingresado ya existe como cliente, por favor iniciá sesión."}

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
            if error.errno == 1062:  # Duplicate entry
                return {"ok": False, "error": "El correo ingresado ya existe como cliente, por favor iniciá sesión."}
            return {"ok": False, "error": str(error)}

    
    # BUSCAR USUARIO POR EMAIL
    def buscar_usuario(self, email):
        email = email.strip().lower()

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
        email = email.strip().lower()
        usuario = self.buscar_usuario(email)

        if not usuario:
            return None

        # Obtener el hash de la contraseña guardada
        hash_guardado = usuario["contraseña"]

        # Asegurar que hash_guardado es bytes
        if isinstance(hash_guardado, bytes):
            hash_bytes = hash_guardado
            hash_texto = hash_guardado.decode('utf-8', errors='ignore')
        elif isinstance(hash_guardado, str):
            hash_texto = hash_guardado
            hash_bytes = hash_guardado.encode('utf-8')
        else:
            return None

        try:
            # Verificar contraseña con bcrypt si el valor tiene formato hash
            if hash_texto.startswith('$2a$') or hash_texto.startswith('$2b$') or hash_texto.startswith('$2y$'):
                if bcrypt.checkpw(contraseña.encode('utf-8'), hash_bytes):
                    return usuario
                return None

            # Compatibilidad con claves legacy en texto plano + migración automática
            if hash_texto == contraseña:
                nuevo_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
                cursor = self.conexion.cursor()
                query = "UPDATE usuario SET contraseña = %s WHERE idusuario = %s"
                cursor.execute(query, (nuevo_hash, usuario['id']))
                self.conexion.commit()
                cursor.close()
                return usuario

            return None
        except Exception as e:
            return None
    
    # OBTENER TODOS LOS USUARIOS (con fechas)
    def obtener_todos(self):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT idusuario, nombre, apellido, email, is_admin, fecha_creacion, ultimo_acceso FROM usuario"
            cursor.execute(query)
            usuarios = cursor.fetchall()
            cursor.close()
            return usuarios
        except Exception as e:
            return []

    # OBTENER PEDIDOS DE UN USUARIO
    def obtener_pedidos_usuario(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            query = """SELECT id, fecha, total, estado 
                       FROM pedidos 
                       WHERE usuario_id = %s 
                       ORDER BY fecha DESC"""
            cursor.execute(query, (usuario_id,))
            pedidos = cursor.fetchall()
            cursor.close()
            resultado = []
            for p in pedidos:
                resultado.append({
                    'id': p[0],
                    'fecha': p[1].strftime('%d/%m/%Y - %H:%M') if p[1] else 'Sin fecha',
                    'total': int(p[2]) if p[2] else 0,
                    'estado': p[3] or 'completado'
                })
            return resultado
        except Exception as e:
            print(f"Error obtener_pedidos_usuario: {e}")
            return []

    # ESTADÍSTICAS DE UN USUARIO (para info rápida)
    def obtener_estadisticas_usuario(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            # Datos del usuario
            cursor.execute(
                "SELECT fecha_creacion, ultimo_acceso FROM usuario WHERE idusuario = %s",
                (usuario_id,)
            )
            usuario_data = cursor.fetchone()

            # Cantidad y monto total de pedidos
            cursor.execute(
                "SELECT COUNT(*), COALESCE(SUM(total), 0) FROM pedidos WHERE usuario_id = %s",
                (usuario_id,)
            )
            pedido_data = cursor.fetchone()
            cursor.close()

            fecha_creacion = usuario_data[0].strftime('%d/%m/%Y - %H:%M') if usuario_data and usuario_data[0] else 'No registrada'
            ultimo_acceso = usuario_data[1].strftime('%d/%m/%Y - %H:%M') if usuario_data and usuario_data[1] else 'Nunca'

            return {
                'fecha_creacion': fecha_creacion,
                'ultimo_acceso': ultimo_acceso,
                'cantidad_pedidos': int(pedido_data[0]) if pedido_data else 0,
                'monto_total': int(pedido_data[1]) if pedido_data else 0
            }
        except Exception as e:
            print(f"Error obtener_estadisticas_usuario: {e}")
            return {
                'fecha_creacion': 'Error',
                'ultimo_acceso': 'Error',
                'cantidad_pedidos': 0,
                'monto_total': 0
            }

    # ACTUALIZAR ÚLTIMO ACCESO
    def actualizar_ultimo_acceso(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(
                "UPDATE usuario SET ultimo_acceso = NOW() WHERE idusuario = %s",
                (usuario_id,)
            )
            self.conexion.commit()
            cursor.close()
        except Exception as e:
            print(f"Error actualizar_ultimo_acceso: {e}")

    # OBTENER USUARIO POR ID
    def obtener_usuario_por_id(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT idusuario, nombre, apellido, email, is_admin, telefono, direccion, provincia, codigo_postal, dni FROM usuario WHERE idusuario = %s"
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
                    "telefono": usuario[5],
                    "direccion": usuario[6],
                    "provincia": usuario[7],
                    "codigo_postal": usuario[8],
                    "dni": usuario[9]
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
            query = "SELECT idusuario, nombre, apellido, email, telefono, direccion, provincia, codigo_postal, dni FROM usuario WHERE idusuario = %s"
            cursor.execute(query, (usuario_id,))
            usuario = cursor.fetchone()
            cursor.close()
            if usuario:
                return {
                    "id": usuario[0],
                    "nombre": usuario[1],
                    "apellido": usuario[2],
                    "email": usuario[3],
                    "telefono": usuario[4],
                    "direccion": usuario[5],
                    "provincia": usuario[6],
                    "codigo_postal": usuario[7],
                    "dni": usuario[8]
                }
            return None
        except Exception as e:
            print(f"Error obtener_perfil: {e}")
            return None

    # ACTUALIZAR PERFIL DEL USUARIO
    def actualizar_perfil(self, usuario_id, nombre, apellido, email, telefono, direccion=None, provincia=None, codigo_postal=None, dni=None):
        try:
            cursor = self.conexion.cursor()
            query = """
                UPDATE usuario 
                SET nombre = %s, apellido = %s, email = %s, telefono = %s, 
                    direccion = %s, provincia = %s, codigo_postal = %s, dni = %s
                WHERE idusuario = %s
            """
            cursor.execute(query, (nombre, apellido, email, telefono, direccion, provincia, codigo_postal, dni, usuario_id))
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
    
    # =====================================================================
    # RECUPERACIÓN DE CONTRASEÑA
    # =====================================================================
    
    def generar_codigo_recuperacion(self, email):
        """
        Genera un código de 6 dígitos para recuperación de contraseña.
        El código expira en 10 minutos.
        
        Args:
            email: Email del usuario
            
        Returns:
            dict con ok=True y el código, o ok=False y error
        """
        email = email.strip().lower()
        
        # Verificar que exista el usuario
        usuario = self.buscar_usuario(email)
        if not usuario:
            # Por seguridad, no revelar si el email existe o no
            # Pero internamente retornamos error para no enviar email
            return {"ok": False, "error": "email_no_existe", "mostrar": "Si el email existe, recibirás un código."}
        
        try:
            # Generar código de 6 dígitos
            codigo = str(random.randint(100000, 999999))
            
            # Fecha de expiración: 10 minutos desde ahora
            expiracion = datetime.now() + timedelta(minutes=10)
            
            # Guardar en BD
            cursor = self.conexion.cursor()
            query = """
                UPDATE usuario 
                SET codigo_recuperacion = %s, codigo_expiracion = %s 
                WHERE email = %s
            """
            cursor.execute(query, (codigo, expiracion, email))
            self.conexion.commit()
            cursor.close()
            
            return {
                "ok": True, 
                "codigo": codigo,
                "nombre": usuario.get("nombre", "Usuario"),
                "user_id": usuario.get("id")
            }
            
        except Exception as e:
            print(f"⚠ Error al generar código: {str(e)}")
            return {"ok": False, "error": str(e)}
    
    def validar_codigo_recuperacion(self, email, codigo):
        """
        Valida si el código ingresado es correcto y no ha expirado.
        
        Args:
            email: Email del usuario
            codigo: Código de 6 dígitos ingresado
            
        Returns:
            dict con ok=True si es válido, o ok=False con error
        """
        email = email.strip().lower()
        codigo = codigo.strip()
        
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
                SELECT idusuario, nombre, codigo_recuperacion, codigo_expiracion 
                FROM usuario 
                WHERE email = %s
            """
            cursor.execute(query, (email,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if not resultado:
                return {"ok": False, "error": "Usuario no encontrado"}
            
            codigo_guardado = resultado.get('codigo_recuperacion')
            expiracion = resultado.get('codigo_expiracion')
            
            # Verificar que existe código
            if not codigo_guardado:
                return {"ok": False, "error": "No hay solicitud de recuperación pendiente"}
            
            # Verificar que no expiró
            if expiracion and datetime.now() > expiracion:
                return {"ok": False, "error": "El código ha expirado. Solicitá uno nuevo."}
            
            # Verificar que coincide
            if codigo != codigo_guardado:
                return {"ok": False, "error": "Código incorrecto"}
            
            return {
                "ok": True, 
                "user_id": resultado.get('idusuario'),
                "nombre": resultado.get('nombre')
            }
            
        except Exception as e:
            print(f"⚠ Error al validar código: {str(e)}")
            return {"ok": False, "error": "Error al validar código"}
    
    def restablecer_contraseña(self, email, codigo, nueva_contraseña):
        """
        Restablece la contraseña después de validar el código.
        Invalida el código después del cambio.
        
        Args:
            email: Email del usuario
            codigo: Código de verificación
            nueva_contraseña: Nueva contraseña en texto plano
            
        Returns:
            dict con ok=True si se cambió, o ok=False con error
        """
        # Primero validar el código
        validacion = self.validar_codigo_recuperacion(email, codigo)
        if not validacion.get("ok"):
            return validacion
        
        try:
            # Hashear nueva contraseña
            hashed = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt())
            
            # Actualizar contraseña y limpiar código
            cursor = self.conexion.cursor()
            query = """
                UPDATE usuario 
                SET contraseña = %s, codigo_recuperacion = NULL, codigo_expiracion = NULL 
                WHERE email = %s
            """
            cursor.execute(query, (hashed, email.strip().lower()))
            self.conexion.commit()
            cursor.close()
            
            return {
                "ok": True, 
                "mensaje": "Contraseña actualizada correctamente",
                "nombre": validacion.get("nombre")
            }
            
        except Exception as e:
            print(f"⚠ Error al restablecer contraseña: {str(e)}")
            return {"ok": False, "error": "Error al actualizar contraseña"}
    
    def invalidar_codigo_recuperacion(self, email):
        """Limpia el código de recuperación (uso manual o por seguridad)."""
        try:
            cursor = self.conexion.cursor()
            query = "UPDATE usuario SET codigo_recuperacion = NULL, codigo_expiracion = NULL WHERE email = %s"
            cursor.execute(query, (email.strip().lower(),))
            self.conexion.commit()
            cursor.close()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}
