"""
Endpoints para el perfil de usuario
"""
from flask import request, jsonify, session
from services.usuario_service import UsuarioService
from services.direccion_service import DireccionService
import bcrypt


def registrar_endpoints_perfil(app):
    """Registra todos los endpoints del perfil en la aplicación Flask"""

    # ====================== ENDPOINTS DEL PERFIL ======================

    @app.route('/api/perfil/actualizar', methods=['POST'])
    def actualizar_perfil():
        """Actualizar datos del perfil del usuario"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401
        
        try:
            datos = request.get_json()
            usuario_id = session.get('usuario_id')
            
            service = UsuarioService()
            resultado = service.actualizar_perfil(
                usuario_id,
                datos.get('nombre'),
                datos.get('apellido'),
                datos.get('email'),
                datos.get('telefono'),
                datos.get('dni')
            )
            
            if resultado['ok']:
                session['usuario_nombre'] = datos.get('nombre')
                session['usuario_email'] = datos.get('email')
                session['usuario_telefono'] = datos.get('telefono', '')
                session['usuario_dni'] = datos.get('dni', '')
            
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/perfil/cambiar-contraseña', methods=['POST'])
    def cambiar_contraseña():
        """Cambiar contraseña del usuario"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401
        
        try:
            datos = request.get_json()
            usuario_id = session.get('usuario_id')
            
            service = UsuarioService()
            
            # Verificar contraseña actual
            usuario = service.buscar_usuario(session.get('usuario_email'))
            if not usuario:
                return jsonify({"ok": False, "error": "Usuario no encontrado"}), 404
            
            hash_guardado = usuario['contraseña']
            if isinstance(hash_guardado, str):
                hash_guardado = hash_guardado.encode('utf-8')
            
            if not bcrypt.checkpw(
                datos.get('contraseña_actual', '').encode('utf-8'),
                hash_guardado
            ):
                return jsonify({"ok": False, "error": "Contraseña actual incorrecta"}), 401
            
            # Cambiar contraseña
            resultado = service.cambiar_contraseña(usuario_id, datos.get('contraseña_nueva'))
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    # ====================== ENDPOINTS DE DIRECCIONES ======================

    @app.route('/api/direcciones', methods=['GET'])
    def obtener_direcciones():
        """Obtener todas las direcciones del usuario"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401
        
        try:
            usuario_id = session.get('usuario_id')
            service = DireccionService()
            direcciones = service.obtener_direcciones(usuario_id)
            
            return jsonify({"ok": True, "direcciones": direcciones})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/direcciones/crear', methods=['POST'])
    def crear_direccion():
        """Crear nueva dirección"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401
        
        try:
            datos = request.get_json()
            usuario_id = session.get('usuario_id')
            
            service = DireccionService()
            resultado = service.crear_direccion(
                usuario_id,
                datos.get('calle'),
                datos.get('numero'),
                datos.get('codigo_postal'),
                datos.get('provincia'),
                datos.get('municipio'),
                datos.get('piso_departamento'),
                datos.get('es_principal', False)
            )
            
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/direcciones/<int:direccion_id>', methods=['PUT'])
    def actualizar_direccion(direccion_id):
        """Actualizar dirección existente"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401
        
        try:
            datos = request.get_json()
            usuario_id = session.get('usuario_id')
            
            service = DireccionService()
            resultado = service.actualizar_direccion(
                direccion_id,
                usuario_id,
                datos.get('calle'),
                datos.get('numero'),
                datos.get('codigo_postal'),
                datos.get('provincia'),
                datos.get('municipio'),
                datos.get('piso_departamento'),
                datos.get('es_principal', False)
            )
            
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/direcciones/<int:direccion_id>', methods=['DELETE'])
    def eliminar_direccion(direccion_id):
        """Eliminar dirección"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401
        
        try:
            usuario_id = session.get('usuario_id')
            
            service = DireccionService()
            resultado = service.eliminar_direccion(direccion_id, usuario_id)
            
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/direcciones/<int:direccion_id>', methods=['GET'])
    def obtener_direccion_detalles(direccion_id):
        """Obtener detalles de una dirección específica"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401
        
        try:
            usuario_id = session.get('usuario_id')
            service = DireccionService()
            direccion = service.obtener_direccion(direccion_id, usuario_id)
            
            if direccion:
                return jsonify({"ok": True, "direccion": direccion})
            else:
                return jsonify({"ok": False, "error": "Dirección no encontrada"}), 404
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/direcciones/<int:direccion_id>/principal', methods=['PUT'])
    def establecer_principal(direccion_id):
        """Establecer dirección como principal"""
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "error": "No autorizado"}), 401
        
        try:
            usuario_id = session.get('usuario_id')
            service = DireccionService()
            resultado = service.establecer_como_principal(direccion_id, usuario_id)
            
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/provincias', methods=['GET'])
    def obtener_provincias():
        """Obtener lista de provincias"""
        try:
            service = DireccionService()
            provincias = service.obtener_provincias()
            
            return jsonify({"ok": True, "provincias": provincias})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/municipios/<provincia>', methods=['GET'])
    def obtener_municipios(provincia):
        """Obtener lista de municipios por provincia"""
        try:
            service = DireccionService()
            municipios = service.obtener_municipios_por_provincia(provincia)
            
            return jsonify({"ok": True, "municipios": municipios})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500


    @app.route('/api/codigo-postal/<provincia>/<municipio>', methods=['GET'])
    def obtener_codigo_postal(provincia, municipio):
        """Obtener código postal por provincia y municipio"""
        try:
            service = DireccionService()
            codigo = service.obtener_codigo_postal(provincia, municipio)
            
            return jsonify({"ok": True, "codigo_postal": codigo if codigo else municipio})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e), "codigo_postal": municipio}), 500
