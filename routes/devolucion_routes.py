"""
Rutas para el sistema de devoluciones y reembolsos.
Incluye endpoints para usuarios (solicitar, consultar) y admin (aprobar, rechazar, listar).
"""
from flask import request, jsonify, session
from services.devolucion_service import DevolucionService
from services.email_service import EmailService
from services.admin_manager import AdminManager


def registrar_endpoints_devoluciones(app):
    """Registra todos los endpoints de devoluciones en la app Flask"""

    admin_manager = AdminManager()

    # ======================== ENDPOINTS DE USUARIO ========================

    @app.route('/api/devoluciones/solicitar', methods=['POST'])
    def solicitar_devolucion():
        """Crear solicitud de devolución (usuario autenticado)"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401

        try:
            datos = request.get_json()
            pedido_id = datos.get('pedido_id')
            motivo = datos.get('motivo', 'otro')
            comentarios = datos.get('comentarios', '').strip()

            if not pedido_id:
                return jsonify({"ok": False, "error": "Falta el ID del pedido"}), 400

            usuario_id = session.get('usuario_id')
            service = DevolucionService()
            resultado = service.solicitar_devolucion(pedido_id, usuario_id, motivo, comentarios)

            if resultado.get("ok"):
                return jsonify(resultado)
            else:
                return jsonify(resultado), 400

        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route('/api/devoluciones/mis-devoluciones', methods=['GET'])
    def mis_devoluciones():
        """Obtener devoluciones del usuario actual"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401

        try:
            usuario_id = session.get('usuario_id')
            service = DevolucionService()
            devoluciones = service.obtener_devoluciones_usuario(usuario_id)
            return jsonify({"ok": True, "devoluciones": devoluciones})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route('/api/devoluciones/estado-pedido/<int:pedido_id>', methods=['GET'])
    def estado_devolucion_pedido(pedido_id):
        """Verificar si un pedido tiene devolución"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401

        try:
            service = DevolucionService()
            devolucion = service.obtener_devolucion_por_pedido(pedido_id)
            return jsonify({"ok": True, "devolucion": devolucion})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    # ======================== ENDPOINTS DE ADMIN ========================

    @app.route('/api/devoluciones/contador-pendientes', methods=['GET'])
    def contador_devoluciones_pendientes():
        """Obtener cantidad de devoluciones pendientes (para badge de notificación)"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401

        try:
            admin = AdminManager()
            if not admin.es_admin(session.get('usuario_id')):
                return jsonify({"ok": False, "error": "No autorizado"}), 403

            service = DevolucionService()
            cantidad = service.contar_pendientes()
            return jsonify({"ok": True, "cantidad": cantidad})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route('/api/devoluciones/pendientes', methods=['GET'])
    @admin_manager.requerir_admin
    def devoluciones_pendientes():
        """Listar devoluciones pendientes (admin)"""
        try:
            service = DevolucionService()
            devoluciones = service.obtener_devoluciones_pendientes()
            return jsonify({"ok": True, "devoluciones": devoluciones})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route('/api/devoluciones/todas', methods=['GET'])
    @admin_manager.requerir_admin
    def todas_devoluciones():
        """Listar todas las devoluciones (historial admin)"""
        try:
            service = DevolucionService()
            devoluciones = service.obtener_todas_devoluciones()
            return jsonify({"ok": True, "devoluciones": devoluciones})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route('/api/devoluciones/aprobar/<int:devolucion_id>', methods=['POST'])
    @admin_manager.requerir_admin
    def aprobar_devolucion(devolucion_id):
        """Aprobar una devolución (admin)"""
        try:
            admin_id = session.get('usuario_id')
            service = DevolucionService()
            resultado = service.aprobar_devolucion(devolucion_id, admin_id)

            if resultado.get("ok"):
                # Enviar email al usuario
                try:
                    email_service = EmailService()
                    email_service.enviar_devolucion_aprobada(
                        email_destino=resultado.get("email_usuario"),
                        nombre_usuario=resultado.get("nombre_usuario"),
                        pedido_id=resultado.get("pedido_id"),
                        monto=resultado.get("monto")
                    )
                except Exception as email_error:
                    print(f"⚠ Error al enviar email de aprobación: {email_error}")

                return jsonify(resultado)
            else:
                return jsonify(resultado), 400

        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.route('/api/devoluciones/rechazar/<int:devolucion_id>', methods=['POST'])
    @admin_manager.requerir_admin
    def rechazar_devolucion(devolucion_id):
        """Rechazar una devolución (admin)"""
        try:
            admin_id = session.get('usuario_id')
            datos = request.get_json() or {}
            motivo_rechazo = datos.get('motivo_rechazo', '').strip()

            service = DevolucionService()
            resultado = service.rechazar_devolucion(devolucion_id, admin_id, motivo_rechazo)

            if resultado.get("ok"):
                # Enviar email al usuario
                try:
                    email_service = EmailService()
                    email_service.enviar_devolucion_rechazada(
                        email_destino=resultado.get("email_usuario"),
                        nombre_usuario=resultado.get("nombre_usuario"),
                        pedido_id=resultado.get("pedido_id"),
                        motivo_rechazo=motivo_rechazo
                    )
                except Exception as email_error:
                    print(f"⚠ Error al enviar email de rechazo: {email_error}")

                return jsonify(resultado)
            else:
                return jsonify(resultado), 400

        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500
