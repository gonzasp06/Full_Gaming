from flask import session


class CarritoService:
    """Servicio para gestionar el carrito de compras"""
    
    def __init__(self):
        pass
    
    def obtener_carrito(self):
        """
        Obtiene el carrito de la sesión
        
        Retorna: dict con {producto_id: cantidad}
        """
        return session.get('carrito', {})
    
    def agregar_item(self, producto_id, cantidad=1):
        """
        Agrega un producto al carrito
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a agregar (default 1)
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
    
    def eliminar_item(self, producto_id):
        """
        Elimina un producto del carrito
        
        Args:
            producto_id: ID del producto a eliminar
        """
        if 'carrito' in session:
            carrito = session['carrito']
            producto_id_str = str(producto_id)
            
            if producto_id_str in carrito:
                del carrito[producto_id_str]
                session.modified = True
    
    def actualizar_cantidad(self, producto_id, cantidad):
        """
        Actualiza la cantidad de un producto en el carrito
        
        Args:
            producto_id: ID del producto
            cantidad: Nueva cantidad
        
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
            return True
        
        return False
    
    def vaciar_carrito(self):
        """Vacía completamente el carrito"""
        if 'carrito' in session:
            session['carrito'] = {}
            session.modified = True
    
    def calcular_total(self, producto_service):
        """
        Calcula el total del carrito
        
        Args:
            producto_service: Instancia de ProductoService para obtener precios
        
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
        Obtiene carrito con detalles completos de cada producto
        
        Args:
            producto_service: Instancia de ProductoService
        
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
        Obtiene items del carrito formateados para procesar compra
        
        Args:
            producto_service: Instancia de ProductoService
        
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
