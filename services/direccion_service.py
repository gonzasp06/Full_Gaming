import mysql.connector
from database import conectar_base_datos


class DireccionService:

    def __init__(self):
        self.conexion = conectar_base_datos()

    # OBTENER TODAS LAS DIRECCIONES DEL USUARIO
    def obtener_direcciones(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT id, calle, numero, piso_departamento, codigo_postal, 
                       provincia, municipio, es_principal
                FROM direcciones 
                WHERE usuario_id = %s
                ORDER BY es_principal DESC, creado_en DESC
            """
            cursor.execute(query, (usuario_id,))
            direcciones = cursor.fetchall()
            cursor.close()
            
            resultado = []
            for dir in direcciones:
                resultado.append({
                    "id": dir[0],
                    "calle": dir[1],
                    "numero": dir[2],
                    "piso_departamento": dir[3],
                    "codigo_postal": dir[4],
                    "provincia": dir[5],
                    "municipio": dir[6],
                    "es_principal": dir[7]
                })
            return resultado
        except Exception as e:
            print(f"Error obtener_direcciones: {e}")
            return []

    # OBTENER UNA DIRECCIÓN POR ID
    def obtener_direccion(self, direccion_id, usuario_id):
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT id, calle, numero, piso_departamento, codigo_postal, 
                       provincia, municipio, es_principal
                FROM direcciones 
                WHERE id = %s AND usuario_id = %s
            """
            cursor.execute(query, (direccion_id, usuario_id))
            direccion = cursor.fetchone()
            cursor.close()
            
            if direccion:
                return {
                    "id": direccion[0],
                    "calle": direccion[1],
                    "numero": direccion[2],
                    "piso_departamento": direccion[3],
                    "codigo_postal": direccion[4],
                    "provincia": direccion[5],
                    "municipio": direccion[6],
                    "es_principal": direccion[7]
                }
            return None
        except Exception as e:
            print(f"Error obtener_direccion: {e}")
            return None

    # CREAR NUEVA DIRECCIÓN
    def crear_direccion(self, usuario_id, calle, numero, codigo_postal, provincia, municipio, piso_departamento=None, es_principal=False):
        try:
            cursor = self.conexion.cursor()
            
            # Si es principal, desmarcar otras direcciones como principal
            if es_principal:
                cursor.execute(
                    "UPDATE direcciones SET es_principal = FALSE WHERE usuario_id = %s",
                    (usuario_id,)
                )
            
            query = """
                INSERT INTO direcciones 
                (usuario_id, calle, numero, piso_departamento, codigo_postal, provincia, municipio, es_principal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (usuario_id, calle, numero, piso_departamento, codigo_postal, provincia, municipio, es_principal))
            self.conexion.commit()
            direccion_id = cursor.lastrowid
            cursor.close()
            
            return {"ok": True, "id": direccion_id, "mensaje": "Dirección creada correctamente"}
        except mysql.connector.Error as e:
            if e.errno == 1452:  # Foreign key constraint
                return {"ok": False, "error": "Código postal inválido"}
            return {"ok": False, "error": str(e)}
        except Exception as e:
            print(f"Error crear_direccion: {e}")
            return {"ok": False, "error": str(e)}

    # ACTUALIZAR DIRECCIÓN
    def actualizar_direccion(self, direccion_id, usuario_id, calle, numero, codigo_postal, provincia, municipio, piso_departamento=None, es_principal=False):
        try:
            cursor = self.conexion.cursor()
            
            # Si es principal, desmarcar otras direcciones como principal
            if es_principal:
                cursor.execute(
                    "UPDATE direcciones SET es_principal = FALSE WHERE usuario_id = %s",
                    (usuario_id,)
                )
            
            query = """
                UPDATE direcciones 
                SET calle = %s, numero = %s, piso_departamento = %s, 
                    codigo_postal = %s, provincia = %s, municipio = %s, es_principal = %s
                WHERE id = %s AND usuario_id = %s
            """
            cursor.execute(query, (calle, numero, piso_departamento, codigo_postal, provincia, municipio, es_principal, direccion_id, usuario_id))
            self.conexion.commit()
            cursor.close()
            
            return {"ok": True, "mensaje": "Dirección actualizada correctamente"}
        except Exception as e:
            print(f"Error actualizar_direccion: {e}")
            return {"ok": False, "error": str(e)}

    # ELIMINAR DIRECCIÓN
    def eliminar_direccion(self, direccion_id, usuario_id):
        try:
            cursor = self.conexion.cursor()
            query = "DELETE FROM direcciones WHERE id = %s AND usuario_id = %s"
            cursor.execute(query, (direccion_id, usuario_id))
            self.conexion.commit()
            cursor.close()
            
            return {"ok": True, "mensaje": "Dirección eliminada correctamente"}
        except Exception as e:
            print(f"Error eliminar_direccion: {e}")
            return {"ok": False, "error": str(e)}

    # OBTENER CÓDIGOS POSTALES POR PROVINCIA
    def obtener_codigos_por_provincia(self, provincia):
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT DISTINCT municipio, codigo_postal
                FROM codigos_postales
                WHERE provincia = %s
                ORDER BY municipio
            """
            cursor.execute(query, (provincia,))
            codigos = cursor.fetchall()
            cursor.close()
            
            resultado = []
            for codigo in codigos:
                resultado.append({
                    "municipio": codigo[0],
                    "codigo_postal": codigo[1]
                })
            return resultado
        except Exception as e:
            print(f"Error obtener_codigos_por_provincia: {e}")
            return []

    # OBTENER TODAS LAS PROVINCIAS
    def obtener_provincias(self):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT DISTINCT provincia FROM codigos_postales ORDER BY provincia"
            cursor.execute(query)
            provincias = cursor.fetchall()
            cursor.close()
            
            return [p[0] for p in provincias]
        except Exception as e:
            print(f"Error obtener_provincias: {e}")
            return []

    # OBTENER MUNICIPIOS POR PROVINCIA
    def obtener_municipios_por_provincia(self, provincia):
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT DISTINCT municipio
                FROM codigos_postales
                WHERE provincia = %s
                ORDER BY municipio
            """
            cursor.execute(query, (provincia,))
            municipios = cursor.fetchall()
            cursor.close()
            
            return [m[0] for m in municipios]
        except Exception as e:
            print(f"Error obtener_municipios_por_provincia: {e}")
            return []

    # OBTENER CÓDIGO POSTAL
    def obtener_codigo_postal(self, provincia, municipio):
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT codigo_postal
                FROM codigos_postales
                WHERE provincia = %s AND municipio = %s
                LIMIT 1
            """
            cursor.execute(query, (provincia, municipio))
            resultado = cursor.fetchone()
            cursor.close()
            
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error obtener_codigo_postal: {e}")
            return None

    # OBTENER DIRECCIÓN PRINCIPAL
    def obtener_direccion_principal(self, usuario_id):
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT id, calle, numero, piso_departamento, codigo_postal, 
                       provincia, municipio
                FROM direcciones 
                WHERE usuario_id = %s AND es_principal = TRUE
                LIMIT 1
            """
            cursor.execute(query, (usuario_id,))
            direccion = cursor.fetchone()
            cursor.close()
            
            if direccion:
                return {
                    "id": direccion[0],
                    "calle": direccion[1],
                    "numero": direccion[2],
                    "piso_departamento": direccion[3],
                    "codigo_postal": direccion[4],
                    "provincia": direccion[5],
                    "municipio": direccion[6]
                }
            return None
        except Exception as e:
            print(f"Error obtener_direccion_principal: {e}")
            return None

    # ESTABLECER DIRECCIÓN COMO PRINCIPAL
    def establecer_como_principal(self, direccion_id, usuario_id):
        try:
            cursor = self.conexion.cursor()
            
            # Desmarcar todas las direcciones de este usuario como principal
            cursor.execute(
                "UPDATE direcciones SET es_principal = FALSE WHERE usuario_id = %s",
                (usuario_id,)
            )
            
            # Marcar esta dirección como principal
            cursor.execute(
                "UPDATE direcciones SET es_principal = TRUE WHERE id = %s AND usuario_id = %s",
                (direccion_id, usuario_id)
            )
            
            self.conexion.commit()
            cursor.close()
            
            return {"ok": True, "mensaje": "Dirección establecida como principal"}
        except Exception as e:
            print(f"Error establecer_como_principal: {e}")
            return {"ok": False, "error": str(e)}
