"""
Endpoints para el módulo de estadísticas del administrador
"""
from flask import request, jsonify, render_template, session
from services.estadisticas_service import EstadisticasService
from services.admin_manager import AdminManager


def registrar_endpoints_estadisticas(app):
    """Registra todos los endpoints de estadísticas en la aplicación Flask"""
    
    admin_manager = AdminManager()
    estadisticas_service = EstadisticasService()
    
    # ====================== ENDPOINTS DE ESTADÍSTICAS ======================
    
    @app.route('/estadisticas')
    @admin_manager.requerir_admin
    def ver_estadisticas():
        """Página principal del dashboard de estadísticas"""
        estadisticas_service = EstadisticasService()
        resultado = estadisticas_service.obtener_resumen_dashboard()
        
        if not resultado['ok']:
            return render_template('estadisticas.html', 
                                 error=resultado.get('error', 'Error desconocido'),
                                 resumen=None)
        
        return render_template('estadisticas.html', resumen=resultado['resumen'])
    
    @app.route('/api/estadisticas/resumen')
    @admin_manager.requerir_admin
    def api_resumen_estadisticas():
        """API para obtener el resumen de estadísticas en JSON"""
        estadisticas_service = EstadisticasService()
        resultado = estadisticas_service.obtener_resumen_dashboard()
        
        if resultado['ok']:
            return jsonify(resultado['resumen'])
        else:
            return jsonify({"error": resultado['error']}), 500
    
    @app.route('/api/estadisticas/ventas-totales')
    @admin_manager.requerir_admin
    def api_ventas_totales():
        """API: Total de ventas"""
        resultado = estadisticas_service.obtener_ventas_totales()
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/pedidos')
    @admin_manager.requerir_admin
    def api_cantidad_pedidos():
        """API: Cantidad de pedidos"""
        resultado = estadisticas_service.obtener_cantidad_pedidos()
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/ingresos/<int:dias>')
    @admin_manager.requerir_admin
    def api_ingresos_periodo(dias):
        """API: Ingresos por período"""
        resultado = estadisticas_service.obtener_ingresos_por_periodo(dias)
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/ticket-promedio')
    @admin_manager.requerir_admin
    def api_ticket_promedio():
        """API: Ticket promedio"""
        resultado = estadisticas_service.obtener_ticket_promedio()
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/productos-vendidos/<int:limite>')
    @admin_manager.requerir_admin
    def api_productos_vendidos(limite=10):
        """API: Productos más vendidos"""
        resultado = estadisticas_service.obtener_productos_mas_vendidos(limite)
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/productos-bajo-stock/<int:limite>')
    @admin_manager.requerir_admin
    def api_productos_bajo_stock(limite=10):
        """API: Productos con bajo stock"""
        resultado = estadisticas_service.obtener_productos_bajo_stock(limite)
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/usuarios')
    @admin_manager.requerir_admin
    def api_cantidad_usuarios():
        """API: Cantidad de usuarios"""
        resultado = estadisticas_service.obtener_cantidad_usuarios()
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/usuarios-activos/<int:limite>')
    @admin_manager.requerir_admin
    def api_usuarios_activos(limite=10):
        """API: Usuarios más activos"""
        resultado = estadisticas_service.obtener_usuarios_mas_activos(limite)
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/nuevos-usuarios/<int:dias>')
    @admin_manager.requerir_admin
    def api_nuevos_usuarios(dias=30):
        """API: Nuevos usuarios por período"""
        resultado = estadisticas_service.obtener_nuevos_usuarios(dias)
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/por-categoria')
    @admin_manager.requerir_admin
    def api_estadisticas_categoria():
        """API: Estadísticas por categoría"""
        resultado = estadisticas_service.obtener_estadisticas_categoria()
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/ingresos-vs-egresos')
    @admin_manager.requerir_admin
    def api_ingresos_vs_egresos():
        """API: Ingresos vs Egresos por mes (últimos 12 meses)"""
        resultado = estadisticas_service.obtener_ingresos_vs_egresos_por_mes(12)
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    
    @app.route('/api/estadisticas/evolucion-ingresos')
    @admin_manager.requerir_admin
    def api_evolucion_ingresos():
        """API: Evolución de ingresos por mes (últimos 12 meses)"""
        resultado = estadisticas_service.obtener_evolucion_ingresos_mensual()
        
        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
