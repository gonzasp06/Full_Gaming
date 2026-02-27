"""
Endpoints para el módulo de estadísticas del administrador
"""
from flask import request, jsonify, render_template, session
from services.estadisticas_service import EstadisticasService
from services.egreso_service import EgresoService
from services.producto_service import ProductoService
from services.admin_manager import AdminManager


def registrar_endpoints_estadisticas(app):
    """Registra todos los endpoints de estadísticas en la aplicación Flask"""
    
    admin_manager = AdminManager()
    estadisticas_service = EstadisticasService()
    egreso_service = EgresoService()
    
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

    # ====================== ENDPOINTS DE EGRESOS REALES ======================

    @app.route('/api/productos/listado-simple')
    @admin_manager.requerir_admin
    def api_productos_listado_simple():
        """API: Lista simple de productos (id, nombre, stock) para select"""
        try:
            producto_service = ProductoService()
            productos = producto_service.obtener_todos()
            lista = []
            for p in productos:
                lista.append({
                    "id": p[0],
                    "nombre": p[1],
                    "stock": int(p[5]) if p[5] else 0,
                    "costo": float(p[7]) if len(p) > 7 and p[7] else 0
                })
            return jsonify({"ok": True, "productos": lista})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route('/api/egresos/registrar', methods=['POST'])
    @admin_manager.requerir_admin
    def api_registrar_egreso():
        """API: Registrar un egreso real (falla, devolución, rotura, etc.)"""
        datos = request.get_json()
        if not datos:
            return jsonify({"ok": False, "error": "Datos no proporcionados"}), 400

        tipo = datos.get('tipo', 'otro')
        monto = datos.get('monto', 0)
        cantidad = datos.get('cantidad', 1)
        descripcion = datos.get('descripcion', '')
        producto_id = datos.get('producto_id')
        pedido_id = datos.get('pedido_id')
        usuario_id = session.get('usuario_id')

        try:
            monto = float(monto)
        except (ValueError, TypeError):
            return jsonify({"ok": False, "error": "Monto inválido"}), 400

        egreso_svc = EgresoService()
        resultado = egreso_svc.registrar_egreso(
            tipo=tipo, monto=monto, cantidad=int(cantidad),
            descripcion=descripcion, producto_id=producto_id,
            pedido_id=pedido_id, usuario_id=usuario_id
        )

        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 400

    @app.route('/api/egresos/listado')
    @admin_manager.requerir_admin
    def api_listado_egresos():
        """API: Obtener listado de egresos reales"""
        egreso_svc = EgresoService()
        resultado = egreso_svc.obtener_listado_egresos(50)

        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500

    @app.route('/api/egresos/por-tipo')
    @admin_manager.requerir_admin
    def api_egresos_por_tipo():
        """API: Egresos agrupados por tipo"""
        egreso_svc = EgresoService()
        resultado = egreso_svc.obtener_egresos_por_tipo()

        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500

    @app.route('/api/egresos/eliminar/<int:egreso_id>', methods=['DELETE'])
    @admin_manager.requerir_admin
    def api_eliminar_egreso(egreso_id):
        """API: Eliminar un egreso real"""
        egreso_svc = EgresoService()
        resultado = egreso_svc.eliminar_egreso(egreso_id)

        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 400

    @app.route('/api/egresos/editar/<int:egreso_id>', methods=['PUT'])
    @admin_manager.requerir_admin
    def api_editar_egreso(egreso_id):
        """API: Editar un egreso real existente"""
        datos = request.get_json()
        if not datos:
            return jsonify({"ok": False, "error": "Datos no proporcionados"}), 400

        egreso_svc = EgresoService()
        resultado = egreso_svc.actualizar_egreso(
            egreso_id=egreso_id,
            tipo=datos.get('tipo'),
            monto=datos.get('monto'),
            cantidad=datos.get('cantidad'),
            descripcion=datos.get('descripcion'),
            producto_id=datos.get('producto_id')
        )

        if resultado['ok']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 400
