import mysql.connector
from database import conectar_base_datos
from datetime import datetime, timedelta


class EstadisticasService:
    """
    Servicio para obtener y calcular estadísticas del negocio.
    Proporciona métricas de ventas, usuarios, productos y comportamiento.
    """
    
    def __init__(self):
        """Inicializa la conexión a la base de datos"""
        self.conexion = conectar_base_datos()
    
    # =================== MÉTODOS DE VENTAS ===================
    
    def obtener_ventas_totales(self):
        """
        Calcula el total de ventas en pesos
        
        Retorna: {'ok': True, 'total': int} o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = "SELECT COALESCE(SUM(total), 0) FROM pedidos"
            cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            
            return {
                "ok": True,
                "total": int(resultado[0]) if resultado[0] else 0
            }
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    def obtener_cantidad_pedidos(self):
        """
        Obtiene el total de pedidos realizados
        
        Retorna: {'ok': True, 'cantidad': int} o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = "SELECT COUNT(*) FROM pedidos"
            cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            
            return {
                "ok": True,
                "cantidad": int(resultado[0]) if resultado[0] else 0
            }
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    def obtener_ingresos_por_periodo(self, dias=30):
        """
        Obtiene ingresos totales en los últimos N días
        
        Args:
            dias: cantidad de días a analizar (default 30)
        
        Retorna: {'ok': True, 'ingresos': int} o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            fecha_inicio = datetime.now() - timedelta(days=dias)
            
            query = """
                SELECT COALESCE(SUM(total), 0) FROM pedidos 
                WHERE fecha >= %s
            """
            cursor.execute(query, (fecha_inicio,))
            resultado = cursor.fetchone()
            cursor.close()
            
            return {
                "ok": True,
                "ingresos": int(resultado[0]) if resultado[0] else 0,
                "periodo_dias": dias
            }
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    def obtener_ticket_promedio(self):
        """
        Calcula el valor promedio de cada pedido
        
        Retorna: {'ok': True, 'promedio': float} o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT 
                    COUNT(*) as cantidad,
                    AVG(total) as promedio
                FROM pedidos
            """
            cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            
            cantidad = int(resultado[0]) if resultado[0] else 0
            promedio = float(resultado[1]) if resultado[1] else 0
            
            return {
                "ok": True,
                "promedio": round(promedio, 2),
                "cantidad_pedidos": cantidad
            }
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    # =================== MÉTODOS DE PRODUCTOS ===================
    
    def obtener_productos_mas_vendidos(self, limite=10):
        """
        Obtiene los productos más vendidos
        
        Args:
            limite: cantidad de productos a mostrar (default 10)
        
        Retorna: lista de dicts con info del producto o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT 
                    p.id,
                    p.nombre,
                    SUM(pi.cantidad) as cantidad_vendida,
                    SUM(pi.subtotal) as ingresos_generados,
                    p.precio
                FROM pedido_items pi
                JOIN producto p ON pi.producto_id = p.id
                GROUP BY p.id, p.nombre, p.precio
                ORDER BY cantidad_vendida DESC
                LIMIT %s
            """
            cursor.execute(query, (limite,))
            resultados = cursor.fetchall()
            cursor.close()
            
            productos = []
            for row in resultados:
                productos.append({
                    "id": row[0],
                    "nombre": row[1],
                    "cantidad_vendida": int(row[2]) if row[2] else 0,
                    "ingresos": int(row[3]) if row[3] else 0,
                    "precio": int(row[4]) if row[4] else 0
                })
            
            return {"ok": True, "productos": productos}
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    def obtener_productos_bajo_stock(self, limite_stock=10):
        """
        Obtiene productos con stock bajo
        
        Args:
            limite_stock: cantidad máxima de stock considerado "bajo" (default 10)
        
        Retorna: lista de dicts con info del producto o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT 
                    id,
                    nombre,
                    cantidad,
                    precio,
                    categoria
                FROM producto
                WHERE cantidad <= %s AND cantidad > 0
                ORDER BY cantidad ASC
                LIMIT 20
            """
            cursor.execute(query, (limite_stock,))
            resultados = cursor.fetchall()
            cursor.close()
            
            productos = []
            for row in resultados:
                productos.append({
                    "id": row[0],
                    "nombre": row[1],
                    "stock": int(row[2]) if row[2] else 0,
                    "precio": int(row[3]) if row[3] else 0,
                    "categoria": row[4] if row[4] else "N/A"
                })
            
            return {"ok": True, "productos": productos}
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    # =================== MÉTODOS DE USUARIOS ===================
    
    def obtener_cantidad_usuarios(self):
        """
        Obtiene el total de usuarios registrados
        
        Retorna: {'ok': True, 'cantidad': int} o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = "SELECT COUNT(*) FROM usuario"
            cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            
            return {
                "ok": True,
                "cantidad": int(resultado[0]) if resultado[0] else 0
            }
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    def obtener_usuarios_mas_activos(self, limite=10):
        """
        Obtiene los usuarios con más compras (solo usuarios registrados)
        
        Args:
            limite: cantidad de usuarios a mostrar (default 10)
        
        Retorna: lista de dicts con info del usuario o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT 
                    u.idusuario,
                    u.nombre,
                    u.apellido,
                    u.email,
                    COUNT(DISTINCT p.id) as cantidad_pedidos,
                    COALESCE(SUM(p.total), 0) as total_gastado
                FROM usuario u
                LEFT JOIN pedidos p ON u.idusuario = p.usuario_id
                WHERE u.idusuario IS NOT NULL
                AND p.id IS NOT NULL
                GROUP BY u.idusuario, u.nombre, u.apellido, u.email
                ORDER BY COALESCE(SUM(p.total), 0) DESC
                LIMIT %s
            """
            cursor.execute(query, (limite,))
            resultados = cursor.fetchall()
            cursor.close()
            
            usuarios = []
            for row in resultados:
                usuarios.append({
                    "id": row[0],
                    "nombre": row[1],
                    "apellido": row[2],
                    "email": row[3],
                    "cantidad_pedidos": int(row[4]) if row[4] else 0,
                    "total_gastado": int(row[5]) if row[5] else 0
                })
            
            return {"ok": True, "usuarios": usuarios}
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    def obtener_nuevos_usuarios(self, dias=30):
        """
        Obtiene usuarios registrados en los últimos N días
        
        Args:
            dias: cantidad de días a analizar (default 30)
        
        Retorna: {'ok': True, 'cantidad': int} o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            fecha_inicio = datetime.now() - timedelta(days=dias)
            
            query = """
                SELECT COUNT(*) FROM usuario 
                WHERE fecha_creacion >= %s
            """
            cursor.execute(query, (fecha_inicio,))
            resultado = cursor.fetchone()
            cursor.close()
            
            return {
                "ok": True,
                "cantidad": int(resultado[0]) if resultado[0] else 0,
                "periodo_dias": dias
            }
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
    
    # =================== MÉTODOS DE RESUMEN GENERAL ===================
    
    def obtener_resumen_dashboard(self):
        """
        Obtiene un resumen general de todas las estadísticas principales
        
        Retorna: dict con todas las métricas o {'ok': False, 'error': 'msg'}
        """
        try:
            # Obtener todas las métricas
            ventas_totales = self.obtener_ventas_totales()
            cantidad_pedidos = self.obtener_cantidad_pedidos()
            ticket_promedio = self.obtener_ticket_promedio()
            cantidad_usuarios = self.obtener_cantidad_usuarios()
            ingresos_mes = self.obtener_ingresos_por_periodo(30)
            nuevos_usuarios = self.obtener_nuevos_usuarios(30)
            productos_vendidos = self.obtener_productos_mas_vendidos(5)
            productos_bajo_stock = self.obtener_productos_bajo_stock(5)
            usuarios_activos = self.obtener_usuarios_mas_activos(5)
            
            # Verificar que todas las consultas fueron exitosas
            if not all([
                ventas_totales['ok'],
                cantidad_pedidos['ok'],
                ticket_promedio['ok'],
                cantidad_usuarios['ok'],
                ingresos_mes['ok'],
                nuevos_usuarios['ok'],
                productos_vendidos['ok'],
                productos_bajo_stock['ok'],
                usuarios_activos['ok']
            ]):
                return {"ok": False, "error": "Error al obtener algunos datos"}
            
            return {
                "ok": True,
                "resumen": {
                    "ventas_totales": ventas_totales['total'],
                    "cantidad_pedidos": cantidad_pedidos['cantidad'],
                    "ticket_promedio": ticket_promedio['promedio'],
                    "cantidad_usuarios": cantidad_usuarios['cantidad'],
                    "ingresos_mes": ingresos_mes['ingresos'],
                    "nuevos_usuarios": nuevos_usuarios['cantidad'],
                    "productos_mas_vendidos": productos_vendidos['productos'],
                    "productos_bajo_stock": productos_bajo_stock['productos'],
                    "usuarios_mas_activos": usuarios_activos['usuarios'],
                    "fecha_generacion": datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                }
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def obtener_estadisticas_categoria(self):
        """
        Obtiene ingresos y cantidad de vendidos por categoría
        
        Retorna: lista de dicts con info por categoría o {'ok': False, 'error': 'msg'}
        """
        cursor = None
        try:
            cursor = self.conexion.cursor()
            query = """
                SELECT 
                    p.categoria,
                    COUNT(DISTINCT pi.pedido_id) as cantidad_pedidos,
                    COALESCE(SUM(pi.cantidad), 0) as cantidad_productos,
                    COALESCE(SUM(pi.subtotal), 0) as ingresos
                FROM pedido_items pi
                JOIN producto p ON pi.producto_id = p.id
                GROUP BY p.categoria
                ORDER BY COALESCE(SUM(pi.subtotal), 0) DESC
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            
            categorias = []
            for row in resultados:
                categorias.append({
                    "categoria": row[0] if row[0] else "Sin categoría",
                    "pedidos": int(row[1]) if row[1] else 0,
                    "productos": int(row[2]) if row[2] else 0,
                    "ingresos": int(row[3]) if row[3] else 0
                })
            
            return {"ok": True, "categorias": categorias}
        except mysql.connector.Error as error:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(error)}
        except Exception as e:
            if cursor:
                cursor.close()
            return {"ok": False, "error": str(e)}
