from flask import session
from database import conectar_base_datos


class CarritoService:
    """
    Servicio para gestionar el carrito de compras.
    
    Usa la sesión como capa rápida de lectura/escritura.
    Cuando hay un usuario logueado, sincroniza los cambios
    con la tabla carrito_usuario en la BD para persistencia.
    """
    
    def __init__(self):
        pass

    # ============================================================
    #  HELPERS INTERNOS
    # ============================================================

    def _usuario_id(self):
        """Devuelve el ID del usuario logueado o None."""
        return session.get('usuario_id')

    def _sincronizar_a_bd(self):
        """
        Graba el carrito de la sesión en la BD.
        Solo opera si hay usuario logueado.
        Usa INSERT … ON DUPLICATE KEY UPDATE para evitar duplicados.
        """
        uid = self._usuario_id()
        if not uid:
            return

        carrito = session.get('carrito', {})
        conexion = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            # Limpiar carrito viejo del usuario en BD
            cursor.execute("DELETE FROM carrito_usuario WHERE usuario_id = %s", (uid,))

            # Insertar items actuales
            if carrito:
                query = """
                    INSERT INTO carrito_usuario (usuario_id, producto_id, cantidad)
                    VALUES (%s, %s, %s)
                """
                valores = [(uid, int(pid), int(cant)) for pid, cant in carrito.items() if int(cant) > 0]
                if valores:
                    cursor.executemany(query, valores)

            conexion.commit()
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"⚠ Error sincronizando carrito a BD: {e}")
            if conexion:
                try:
                    conexion.close()
                except:
                    pass

    def cargar_carrito_desde_bd(self, usuario_id):
        """
        Lee el carrito persistente de la BD y lo carga en la sesión.
        Llamar justo después del login.
        """
        conexion = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT producto_id, cantidad FROM carrito_usuario WHERE usuario_id = %s",
                (usuario_id,)
            )
            rows = cursor.fetchall()
            cursor.close()
            conexion.close()

            carrito_bd = {}
            for producto_id, cantidad in rows:
                carrito_bd[str(producto_id)] = int(cantidad)

            # Si el usuario ya tenía items en la sesión (anónima), mergearlos
            carrito_sesion = session.get('carrito', {})
            for pid, cant in carrito_sesion.items():
                if pid in carrito_bd:
                    carrito_bd[pid] = max(carrito_bd[pid], cant)
                else:
                    carrito_bd[pid] = cant

            session['carrito'] = carrito_bd
            session.modified = True
        except Exception as e:
            print(f"⚠ Error cargando carrito desde BD: {e}")
            if conexion:
                try:
                    conexion.close()
                except:
                    pass

    def guardar_carrito_en_bd(self, usuario_id):
        """
        Persiste el carrito de la sesión en la BD.
        Llamar antes de cerrar sesión.
        """
        carrito = session.get('carrito', {})
        if not carrito:
            return

        conexion = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM carrito_usuario WHERE usuario_id = %s", (usuario_id,))

            query = """
                INSERT INTO carrito_usuario (usuario_id, producto_id, cantidad)
                VALUES (%s, %s, %s)
            """
            valores = [(usuario_id, int(pid), int(cant)) for pid, cant in carrito.items() if int(cant) > 0]
            if valores:
                cursor.executemany(query, valores)

            conexion.commit()
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"⚠ Error guardando carrito en BD: {e}")
            if conexion:
                try:
                    conexion.close()
                except:
                    pass

    def vaciar_carrito_bd(self, usuario_id):
        """Elimina todos los items del carrito persistente del usuario."""
        conexion = None
        try:
            conexion = conectar_base_datos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM carrito_usuario WHERE usuario_id = %s", (usuario_id,))
            conexion.commit()
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"⚠ Error vaciando carrito en BD: {e}")
            if conexion:
                try:
                    conexion.close()
                except:
                    pass

    # ============================================================
    #  API PÚBLICA — misma interfaz que antes
    # ============================================================

    def obtener_carrito(self):
        """
        Obtiene el carrito de la sesión.
        
        Retorna: dict con {producto_id_str: cantidad}
        """
        return session.get('carrito', {})
    
    def agregar_item(self, producto_id, cantidad=1):
        """
        Agrega un producto al carrito (sesión + BD si logueado).
        """
        if 'carrito' not in session:
            session['carrito'] = {}
        
        carrito = session['carrito']
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            carrito[producto_id_str] += cantidad
        else:
            carrito[producto_id_str] = cantidad
        
        session.modified = True
        self._sincronizar_a_bd()
    
    def eliminar_item(self, producto_id):
        """
        Elimina un producto del carrito (sesión + BD si logueado).
        """
        if 'carrito' in session:
            carrito = session['carrito']
            producto_id_str = str(producto_id)
            
            if producto_id_str in carrito:
                del carrito[producto_id_str]
                session.modified = True
                self._sincronizar_a_bd()
    
    def actualizar_cantidad(self, producto_id, cantidad):
        """
        Actualiza la cantidad de un producto en el carrito.
        
        Retorna: True si se actualizó, False si falló
        """
        if cantidad <= 0:
            return False
        
        if 'carrito' not in session:
            return False
        
        carrito = session['carrito']
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            carrito[producto_id_str] = cantidad
            session.modified = True
            self._sincronizar_a_bd()
            return True
        
        return False
    
    def vaciar_carrito(self):
        """Vacía completamente el carrito (sesión + BD si logueado)."""
        uid = self._usuario_id()
        if uid:
            self.vaciar_carrito_bd(uid)

        if 'carrito' in session:
            session['carrito'] = {}
            session.modified = True  
    
    def calcular_total(self, producto_service):
        """
        Calcula el total del carrito.
        
        Retorna: float con el total
        """
        carrito = self.obtener_carrito()
        total = 0
        
        for producto_id, cantidad in carrito.items():
            producto = producto_service.obtener_por_id(int(producto_id))
            if producto:
                precio = float(producto[4])
                total += precio * cantidad
        
        return total
    
    def obtener_items_detalle(self, producto_service):
        """
        Obtiene carrito con detalles completos de cada producto.
        
        Retorna: lista de dicts con info completa de cada item
        """
        carrito = self.obtener_carrito()
        items = []
        
        for producto_id, cantidad in carrito.items():
            producto = producto_service.obtener_por_id(int(producto_id))
            if producto:
                precio = float(producto[4])
                items.append({
                    'id': producto[0],
                    'nombre': producto[1],
                    'precio': precio,
                    'cantidad': cantidad,
                    'subtotal': precio * cantidad,
                    'foto': producto[6]
                })
        
        return items
    
    def obtener_items_para_compra(self, producto_service):
        """
        Obtiene items del carrito formateados para procesar compra.
        
        Retorna: lista de dicts con {producto_id, cantidad, precio, subtotal}
        """
        carrito = self.obtener_carrito()
        items_compra = []
        
        for producto_id, cantidad in carrito.items():
            producto = producto_service.obtener_por_id(int(producto_id))
            if producto:
                precio = float(producto[4])
                items_compra.append({
                    'producto_id': int(producto_id),
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': precio * cantidad
                })
        
        return items_compra
