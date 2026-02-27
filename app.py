from flask import Flask, request, jsonify, render_template, render_template_string, session, redirect, url_for, abort
import mysql.connector
from datetime import timedelta

from database import conectar_base_datos
from services.admin_manager import AdminManager
from services.carrito_service import CarritoService
from migrations import (
    agregar_columna_costo_si_no_existe,
    agregar_columna_fecha_creacion_usuario_si_no_existe,
    crear_tabla_stock_compras_si_no_existe,
    agregar_columnas_costos_pedido_items_si_no_existen,
    crear_tabla_marca_si_no_existe,
    agregar_columna_id_marca_producto_si_no_existe,
    agregar_columnas_recuperacion_usuario_si_no_existen,
    agregar_columna_token_eliminacion_si_no_existe,
    crear_tabla_egresos_reales_si_no_existe,
    crear_tabla_devoluciones_si_no_existe,
    crear_tabla_carrito_usuario_si_no_existe,
)

#Subir foto tipo archivo al servidor
import os
from werkzeug.utils import secure_filename #wsi
from math import ceil
import bcrypt #incripta contraseña 
from services.producto_service import ProductoService
from services.usuario_service import UsuarioService
from services.pedido_service import PedidoService
from services.stock_service import StockService
from services.marca_service import MarcaService
from services.email_service import EmailService
from services.negocio_models import IngresoStock
from routes.perfil_routes import registrar_endpoints_perfil
from routes.estadisticas_routes import registrar_endpoints_estadisticas
from routes.devolucion_routes import registrar_endpoints_devoluciones

# print("ProductoService:", ProductoService)

app = Flask(__name__)

# ==================== MIGRACIONES ====================
# Ejecutar migraciones al iniciar la app
agregar_columna_costo_si_no_existe()
agregar_columna_fecha_creacion_usuario_si_no_existe()
crear_tabla_stock_compras_si_no_existe()
agregar_columnas_costos_pedido_items_si_no_existen()
crear_tabla_marca_si_no_existe()
agregar_columna_id_marca_producto_si_no_existe()
agregar_columnas_recuperacion_usuario_si_no_existen()
agregar_columna_token_eliminacion_si_no_existe()
crear_tabla_egresos_reales_si_no_existe()
crear_tabla_devoluciones_si_no_existe()
crear_tabla_carrito_usuario_si_no_existe()
# ============================================
# INSTANCIAR SERVICIOS
# ============================================
admin_manager = AdminManager()
carrito_service = CarritoService()

# Carpeta para imágenes
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = '5x7#YI6+W<i{n^$V5y4ZHf7' #clave secreta para sesiones

# Configuración de sesiones para que persistan
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Sesión dura 7 días
app.config['SESSION_COOKIE_SECURE'] = False  # False en desarrollo, True en producción
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Evita acceso desde JS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Importante para cookies cross-site

# Hacer que TODAS las sesiones sean permanentes por defecto
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)

# Registrar endpoints del perfil
registrar_endpoints_perfil(app)

# Registrar endpoints de estadísticas
registrar_endpoints_estadisticas(app)

# Registrar endpoints de devoluciones
registrar_endpoints_devoluciones(app)

# conexión a base de datos
conexion = conectar_base_datos()

# Verificar conexión
# http://127.0.0.1:5000/verificar_conexion
@app.route('/verificar_conexion')
def verificar_conexion():
    if conexion.is_connected():
        return 'Conexión exitosa'
    else:
        return 'Error de conexión'


productos_por_pagina = 9

# Ruta raíz
@app.route('/') #define ruta principal 
@app.route('/<int:pagina>')
def mostrar_catalogo(pagina=1): 
    service = ProductoService()
    productos = service.obtener_paginados(pagina, 9)
    total_productos = len(service.obtener_todos())
    total_paginas = ceil(total_productos / 9)
    es_admin = session.get('es_admin', False)
    return render_template('index.html', productos=productos, pagina=pagina, total_paginas=total_paginas, es_admin=es_admin)

@app.route('/buscar')
def buscar_productos():
    termino = request.args.get('q', '').strip()

    if not termino:
        return redirect(url_for('mostrar_catalogo'))

    service = ProductoService()
    productos = service.buscar_productos(termino)
    es_admin = session.get('es_admin', False)

    return render_template('resultado_busqueda.html', productos=productos, termino=termino, es_admin=es_admin)

@app.route('/terminos')
def terminos_condiciones():
    return render_template('terminos.html')

@app.route('/ayuda')
def ayuda_soporte():
    return render_template('ayuda.html')

@app.route('/<categoria>')
def mostrar_catalogo_categoria(categoria):
    service = ProductoService()
    productos = service.filtrar_categoria(categoria)
    es_admin = session.get('es_admin', False)
    return render_template('categoria.html', productos=productos, categoria=categoria, es_admin=es_admin)

# Producto en detalle 
@app.route('/producto/<int:producto_id>')
def ver_producto(producto_id):
    service = ProductoService()
    producto = service.obtener_por_id(producto_id)

    if not producto:
        return abort(404)

    es_admin = session.get('es_admin', False)
    return render_template('producto_detalle.html', producto=producto, es_admin=es_admin)

# FORMULARIO DE REGISTRO

@app.route('/nuevo_usuario')
def crear_usuario():
    return render_template('f_nuevo_usuario.html')


# CREAR USUARIO (POST)

@app.route('/cargar_usuario', methods=['POST'])
def cargar_usuario():
    service = UsuarioService()
    datos = request.form
    
    resultado = service.crear_usuario(
        nombre=datos['nombre'],
        apellido=datos['apellido'],
        email=datos['email'],
        contraseña=datos['contraseña']
    )

    if resultado["ok"]:
        # Obtener los datos del usuario recién creado
        usuario = service.buscar_usuario(datos['email'])
        if usuario:
            # Marcar sesión como permanente PRIMERO
            session.permanent = True
            # Luego inicializar sesión automáticamente
            session['usuario_id'] = usuario['id']
            session['usuario_email'] = usuario['email']
            session['usuario_nombre'] = usuario['nombre']
            session['es_admin'] = usuario['is_admin']
            # Cargar carrito persistente del usuario nuevo
            carrito_service.cargar_carrito_desde_bd(usuario['id'])
            
            # Enviar email de bienvenida con opción de eliminar cuenta
            try:
                email_service = EmailService()
                token = service.generar_token_eliminacion(usuario['id'])
                if token:
                    url_base = request.host_url.rstrip('/')
                    email_service.enviar_bienvenida(
                        email_destino=usuario['email'],
                        nombre_usuario=usuario['nombre'],
                        token_eliminacion=token,
                        url_base=url_base
                    )
            except Exception as e:
                print(f"⚠ Error enviando email de bienvenida: {e}")
                # No bloqueamos el registro si falla el email
                
        return jsonify({"ok": True, "mensaje": "Cuenta creada"}), 200
    else:
        return jsonify({"ok": False, "error": resultado["error"]}), 400



# BUSCAR USUARIO POR EMAIL 

@app.route('/verificar', methods=['POST'])
def verificar_usuario():
    service = UsuarioService()
    email = request.form['email']
    usuario = service.buscar_usuario(email)
    if usuario:
        return jsonify({"mensaje": "Usuario encontrado", "usuario": usuario}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404


# LOGIN DE USUARIO

@app.route('/cuenta', methods=['GET', 'POST'])
def acceso_cuentas():
    if request.method == 'POST':
        service = UsuarioService()
        # .strip() elimina espacios que agregan los teclados de celulares
        email = request.form.get('email', '').strip().lower()
        contraseña = request.form.get('contraseña', '').strip()
        
        usuario = service.login(email, contraseña)
        if usuario:
            session['usuario_id'] = usuario['id']  # ID del usuario
            session['usuario_email'] = usuario['email']  # Email en sesión 
            session['usuario_nombre'] = usuario['nombre']  # Nombre en sesión
            session['es_admin'] = usuario['is_admin']  # Si es admin
            session.permanent = True  # Mantener sesión
            service.actualizar_ultimo_acceso(usuario['id'])  # Registrar último acceso
            # Cargar carrito persistente del usuario
            carrito_service.cargar_carrito_desde_bd(usuario['id'])
            return jsonify({"mensaje": "Login exitoso"}), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401

    return render_template('acceso.html')

def es_admin_logueado():
    return session.get('es_admin') == 1

def usuario_logueado():
    return 'usuario_id' in session

# -----------------------------------------
# FORM LOGIN (VISTA SIMPLE)
# -----------------------------------------
@app.route('/acceso')
def render_acceso():
    return render_template('acceso.html')

# Ruta para cargar un nuevo producto
@app.route('/formulario')
@admin_manager.requerir_admin
def carga_producto():
    marca_service = MarcaService()
    marcas = marca_service.obtener_todas()
    return render_template('formulario_carga_producto.html', marcas=marcas)

@app.route('/gestion_productos')
@admin_manager.requerir_admin
def gestion_productos():
    service = ProductoService()
    productos = service.obtener_todos()
    return render_template('gestion_productos.html', productos=productos)

@app.route('/admin/devoluciones')
@admin_manager.requerir_admin
def admin_devoluciones():
    """Página de administración de devoluciones"""
    return render_template('admin_devoluciones.html')

@app.route('/eliminar_producto/<int:id_producto>')
@admin_manager.requerir_admin
def eliminar_producto(id_producto):
    try:
        service = ProductoService()
        service.eliminar_producto(id_producto)
        return redirect('/gestion_productos')
    except Exception as e:
        print(f"Error al eliminar producto: {str(e)}")
        return redirect('/gestion_productos')

@app.route('/editar_producto/<int:id_producto>')
@admin_manager.requerir_admin
def editar_producto(id_producto):
    service = ProductoService()
    marca_service = MarcaService()
    producto = service.obtener_por_id_con_marca(id_producto)
    marcas = marca_service.obtener_todas()
    return render_template('editar_producto.html', producto=producto, marcas=marcas)

@app.route('/actualizar_producto/<int:id_producto>', methods=['POST'])
@admin_manager.requerir_admin
def actualizar_producto(id_producto):
    service = ProductoService()

    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    categoria = request.form['categoria']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    costo = request.form.get('costo', 0)
    marca_nombre = request.form.get('marca', '').strip()

    # Obtener o crear marca si se especificó
    id_marca = None
    if marca_nombre:
        marca_service = MarcaService()
        id_marca = marca_service.obtener_o_crear(marca_nombre)

    foto = request.files.get('foto')
    ruta = None

    if foto and foto.filename:
        filename = secure_filename(foto.filename)
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(ruta)

    service.editar_producto(id_producto, nombre, descripcion, categoria, precio, cantidad, ruta, costo, id_marca)

    return redirect('/gestion_productos')


# ==================== GESTION DE USUARIOS ====================
@app.route('/usuarios')
@admin_manager.requerir_admin
def gestion_usuarios():
    service = UsuarioService()
    usuarios = service.obtener_todos()
    return render_template('gestion_usuarios.html', usuarios=usuarios)


@app.route('/api/usuarios/<int:user_id>/pedidos')
@admin_manager.requerir_admin
def api_pedidos_usuario(user_id):
    service = UsuarioService()
    pedidos = service.obtener_pedidos_usuario(user_id)
    return jsonify({'ok': True, 'pedidos': pedidos})


@app.route('/api/usuarios/<int:user_id>/info')
@admin_manager.requerir_admin
def api_info_usuario(user_id):
    service = UsuarioService()
    stats = service.obtener_estadisticas_usuario(user_id)
    return jsonify({'ok': True, 'info': stats})


@app.route('/actualizar_rol/<int:user_id>', methods=['POST'])
@admin_manager.requerir_admin
def actualizar_rol(user_id):
    data = request.get_json() or {}
    is_admin = data.get('isAdmin', False)

    # Evitar autodescenso: un admin no puede quitarse permisos mientras esté logueado
    try:
        if int(session.get('usuario_id', 0)) == int(user_id) and not is_admin:
            return jsonify({"ok": False, "error": "No puedes quitarte los permisos de administrador mientras estás logueado."}), 400
    except Exception:
        pass

    service = UsuarioService()
    resultado = service.actualizar_rol(user_id, 1 if is_admin else 0)
    if resultado.get('ok'):
        try:
            if int(session.get('usuario_id', 0)) == int(user_id):
                session['es_admin'] = 1 if is_admin else 0
        except Exception:
            pass
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"ok": False, "error": resultado.get('error')}), 400


@app.route('/eliminar/<int:user_id>', methods=['POST'])
@admin_manager.requerir_admin
def eliminar_usuario(user_id):
    # Evitar que un admin se elimine a sí mismo mientras está logueado
    try:
        if int(session.get('usuario_id', 0)) == int(user_id):
            return jsonify({"ok": False, "error": "No puedes eliminar tu propia cuenta mientras estás logueado."}), 400
    except Exception:
        pass

    service = UsuarioService()
    resultado = service.eliminar_usuario(user_id)
    if resultado.get('ok'):
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"ok": False, "error": resultado.get('error')}), 400


@app.route('/cargar_producto', methods=['POST'])
@admin_manager.requerir_admin
def cargar_producto():
    # Esta ruta procesa el formulario de carga de producto (POST)
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    categoria = request.form.get('categoria')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    inversion_total_form = request.form.get('inversion_total')
    costo = request.form.get('costo', 0)
    porcentaje_ganancia = request.form.get('porcentaje_ganancia', 0)
    marca_nombre = request.form.get('marca', '').strip()

    # Obtener o crear marca si se especificó
    id_marca = None
    if marca_nombre:
        marca_service = MarcaService()
        id_marca = marca_service.obtener_o_crear(marca_nombre)

    try:
        cantidad_int = int(cantidad or 0)
    except (TypeError, ValueError):
        cantidad_int = 0

    try:
        inversion_total = float((inversion_total_form if inversion_total_form not in (None, '') else costo) or 0)
    except (TypeError, ValueError):
        inversion_total = 0

    try:
        porcentaje_ganancia_float = float(porcentaje_ganancia or 0)
    except (TypeError, ValueError):
        porcentaje_ganancia_float = 0

    ingreso_stock = IngresoStock(
        producto_id=None,
        inversion_total=inversion_total,
        cantidad_unidades=cantidad_int,
        porcentaje_ganancia=porcentaje_ganancia_float,
    )

    costo_unitario = ingreso_stock.costo_unitario() if inversion_total > 0 and cantidad_int > 0 else 0
    precio_sugerido = ingreso_stock.precio_venta_sugerido() if costo_unitario > 0 else 0

    try:
        precio_form = float(precio or 0)
    except (TypeError, ValueError):
        precio_form = 0

    precio_final = precio_form if precio_form > 0 else precio_sugerido

    foto = request.files.get('foto')

    # Guardar la imagen en el sistema de archivos
    if foto and foto.filename:
        filename = secure_filename(foto.filename)
        ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(ruta_imagen)
    else:
        ruta_imagen = None


    service = ProductoService()
    resultado = service.agregar_producto(
        nombre=nombre,
        descripcion=descripcion,
        categoria=categoria,
        precio=precio_final,
        cantidad=cantidad,
        ruta_imagen=ruta_imagen,
        costo=costo_unitario,
        id_marca=id_marca
    )

    if resultado.get("ok"):
        producto_id = resultado.get("producto_id")
        if producto_id and inversion_total > 0 and cantidad_int > 0:
            stock_service = StockService()
            stock_service.registrar_compra_stock(
                producto_id=producto_id,
                inversion_total=inversion_total,
                cantidad_unidades=cantidad_int,
                costo_unitario=costo_unitario,
                precio_venta_sugerido=precio_sugerido if precio_sugerido > 0 else None,
                porcentaje_ganancia=porcentaje_ganancia_float,
                usuario_id=session.get('usuario_id'),
                observacion='Carga inicial de producto',
            )

        return jsonify({
            "ok": True,
            "mensaje": "🎉 ¡Producto agregado exitosamente!",
            "submensaje": f"'{nombre}' ha sido añadido a tu catálogo",
            "producto_id": producto_id,
            "precio_calculado": round(precio_final, 2) if precio_final else 0,
            "costo_unitario": round(costo_unitario, 2) if costo_unitario else 0
        }), 200
    else:
        # Si hubo un archivo guardado y la inserción falló, eliminar el archivo para no dejar basura
        try:
            if ruta_imagen and os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
        except Exception:
            pass
        return jsonify({"error": resultado.get("error", "Error al insertar producto")}), 500


# ==================== CARRITO ====================

@app.route('/carrito')
def ver_carrito():
    """Mostrar carrito con detalles de productos"""
    producto_service = ProductoService()
    items = carrito_service.obtener_items_detalle(producto_service)
    total = carrito_service.calcular_total(producto_service)
    
    return render_template('carrito.html', items=items, total=total, usuario_logueado=usuario_logueado())


@app.route('/agregar_carrito/<int:id_producto>', methods=['POST'])
def agregar_carrito(id_producto):
    """Agregar producto al carrito"""
    
    datos = request.get_json() or request.form
    cantidad = int(datos.get('cantidad', 1))
    
    # Validar que exista el producto
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    
    if not producto:
        return jsonify({"ok": False, "error": "Producto no existe"}), 404
    
    # Validar que hay stock
    stock = producto[5]
    if stock <= 0:
        return jsonify({"ok": False, "error": "Producto agotado"}), 400
    
    # Agregar al carrito usando CarritoService
    carrito_service.agregar_item(id_producto, cantidad)
    
    return jsonify({"ok": True, "mensaje": "Producto agregado"}), 200


@app.route('/eliminar_carrito/<int:id_producto>', methods=['POST'])
def eliminar_carrito(id_producto):
    """Eliminar producto del carrito"""
    carrito_service.eliminar_item(id_producto)
    return jsonify({"ok": True}), 200


@app.route('/actualizar_carrito/<int:id_producto>', methods=['POST'])
def actualizar_carrito(id_producto):
    """Actualizar cantidad de producto en carrito"""
    
    datos = request.get_json() or request.form
    cantidad = int(datos.get('cantidad', 1))
    
    # Validar cantidad
    if cantidad <= 0:
        return jsonify({"ok": False, "error": "Cantidad inválida"}), 400
    
    # Validar stock
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    if not producto or cantidad > producto[5]:
        return jsonify({"ok": False, "error": "Stock insuficiente"}), 400
    
    # Actualizar usando CarritoService
    if carrito_service.actualizar_cantidad(id_producto, cantidad):
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"ok": False, "error": "Error al actualizar"}), 400


@app.route('/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    """Vaciar todo el carrito"""
    carrito_service.vaciar_carrito()
    return jsonify({"ok": True}), 200


@app.route('/api/carrito/cantidad', methods=['GET'])
def obtener_cantidad_carrito():
    """Obtener la cantidad total de items en el carrito"""
    carrito = carrito_service.obtener_carrito()
    
    # Sumar todas las cantidades de los productos
    cantidad_total = sum(carrito.values()) if carrito else 0
    
    return jsonify({"ok": True, "cantidad": cantidad_total}), 200


# ==================== API MARCAS ====================
@app.route('/api/marcas', methods=['GET'])
def obtener_marcas():
    """Obtener todas las marcas disponibles"""
    marca_service = MarcaService()
    marcas = marca_service.obtener_todas()
    return jsonify({"ok": True, "marcas": marcas}), 200


@app.route('/api/marcas/en-uso', methods=['GET'])
def obtener_marcas_en_uso():
    """Obtener solo las marcas que tienen productos asociados"""
    marca_service = MarcaService()
    marcas = marca_service.obtener_marcas_en_uso()
    return jsonify({"ok": True, "marcas": marcas}), 200


@app.route('/logout')
def logout():
    """Cerrar sesión"""
    # Guardar carrito en BD antes de limpiar la sesión
    uid = session.get('usuario_id')
    if uid:
        carrito_service.guardar_carrito_en_bd(uid)
    session.clear()
    return redirect(url_for('mostrar_catalogo'))


# ==================== ELIMINAR CUENTA PROPIA ====================

@app.route('/api/eliminar-cuenta', methods=['POST'])
def eliminar_cuenta_propia():
    """
    Elimina la cuenta del usuario autenticado.
    Requiere contraseña actual para confirmar identidad.
    """
    # Verificar que está logueado
    if 'usuario_id' not in session:
        return jsonify({"ok": False, "error": "No estás autenticado"}), 401
    
    datos = request.get_json()
    if not datos:
        return jsonify({"ok": False, "error": "Datos no proporcionados"}), 400
    
    contraseña = datos.get('contraseña', '').strip()
    if not contraseña:
        return jsonify({"ok": False, "error": "Debés ingresar tu contraseña"}), 400
    
    usuario_id = session['usuario_id']
    
    # No permitir que el admin elimine su cuenta desde acá
    if session.get('es_admin') == 1:
        return jsonify({"ok": False, "error": "Las cuentas de administrador no se pueden eliminar desde el perfil"}), 403
    
    service = UsuarioService()
    resultado = service.eliminar_cuenta_propia(usuario_id, contraseña)
    
    if resultado.get("ok"):
        # Limpiar sesión completamente
        session.clear()
        return jsonify({
            "ok": True,
            "mensaje": "Tu cuenta fue eliminada correctamente"
        }), 200
    else:
        return jsonify(resultado), 400


# ==================== RECUPERACIÓN DE CONTRASEÑA ====================

@app.route('/recuperar-contraseña')
def render_recuperar_contraseña():
    """Muestra el formulario para solicitar recuperación de contraseña"""
    return render_template('recuperar_contraseña.html')


@app.route('/api/recuperar/solicitar', methods=['POST'])
def solicitar_recuperacion():
    """
    Solicita un código de recuperación de contraseña.
    Genera código de 6 dígitos y lo envía por email.
    """
    datos = request.get_json()
    email = datos.get('email', '').strip().lower()
    
    if not email:
        return jsonify({"ok": False, "error": "Ingresá tu email"}), 400
    
    service = UsuarioService()
    resultado = service.generar_codigo_recuperacion(email)
    
    if resultado.get("ok"):
        # Enviar email con el código
        email_service = EmailService()
        codigo = resultado.get("codigo")
        envio = email_service.enviar_codigo_recuperacion(
            email_destino=email,
            nombre_usuario=resultado.get("nombre", "Usuario"),
            codigo=codigo
        )
        
        # Por seguridad, siempre responder igual (no revelar si existe el email)
        respuesta = {
            "ok": True, 
            "mensaje": "Si el email está registrado, recibirás un código de verificación.",
            "dev_mode": envio.get("dev_mode", False)  # Solo para desarrollo
        }
        
        # En modo desarrollo, incluir el código en la respuesta para testing
        if envio.get("dev_mode"):
            respuesta["codigo_dev"] = codigo
            
        return jsonify(respuesta)
    else:
        # Si el email no existe, igual mostrar mensaje genérico por seguridad
        return jsonify({
            "ok": True,
            "mensaje": "Si el email está registrado, recibirás un código de verificación."
        })


@app.route('/api/recuperar/validar', methods=['POST'])
def validar_codigo_recuperacion():
    """
    Valida el código de recuperación ingresado.
    Si es válido, permite cambiar la contraseña.
    """
    datos = request.get_json()
    email = datos.get('email', '').strip().lower()
    codigo = datos.get('codigo', '').strip()
    
    if not email or not codigo:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400
    
    service = UsuarioService()
    resultado = service.validar_codigo_recuperacion(email, codigo)
    
    return jsonify(resultado)


@app.route('/api/recuperar/restablecer', methods=['POST'])
def restablecer_contraseña():
    """
    Restablece la contraseña después de validar el código.
    """
    datos = request.get_json()
    email = datos.get('email', '').strip().lower()
    codigo = datos.get('codigo', '').strip()
    nueva_contraseña = datos.get('nueva_contraseña', '')
    confirmar = datos.get('confirmar_contraseña', '')
    
    # Validaciones
    if not email or not codigo or not nueva_contraseña:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400
    
    if len(nueva_contraseña) < 6:
        return jsonify({"ok": False, "error": "La contraseña debe tener al menos 6 caracteres"}), 400
    
    if nueva_contraseña != confirmar:
        return jsonify({"ok": False, "error": "Las contraseñas no coinciden"}), 400
    
    # Restablecer
    service = UsuarioService()
    resultado = service.restablecer_contraseña(email, codigo, nueva_contraseña)
    
    if resultado.get("ok"):
        # Enviar confirmación por email (opcional, no bloquea el flujo)
        email_service = EmailService()
        email_service.enviar_confirmacion_cambio(email, resultado.get("nombre", "Usuario"))
    
    return jsonify(resultado)


# ==================== ELIMINAR CUENTA POR TOKEN ====================

@app.route('/eliminar-cuenta/<token>')
def eliminar_cuenta_por_token(token):
    """
    Elimina una cuenta usando el token enviado en el email de bienvenida.
    Para usuarios que no se registraron ellos mismos.
    """
    if not token or len(token) < 20:
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Link Inválido - Full Gaming</title>
                <style>
                    body { font-family: Arial, sans-serif; background: #1a1a2e; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
                    .card { background: #252540; padding: 40px; border-radius: 20px; text-align: center; max-width: 400px; border: 1px solid #3C308C; }
                    h2 { color: #e74c3c; }
                    p { color: #bbb; }
                    a { color: #6A44F2; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>❌ Link Inválido</h2>
                    <p>El link que usaste no es válido o ya fue utilizado.</p>
                    <p><a href="/">Volver al inicio</a></p>
                </div>
            </body>
            </html>
        ''')
    
    service = UsuarioService()
    resultado = service.eliminar_cuenta_por_token(token)
    
    if resultado.get("ok"):
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Cuenta Eliminada - Full Gaming</title>
                <style>
                    body { font-family: Arial, sans-serif; background: #1a1a2e; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
                    .card { background: #252540; padding: 40px; border-radius: 20px; text-align: center; max-width: 450px; border: 1px solid #3C308C; }
                    h2 { color: #27ae60; }
                    p { color: #bbb; line-height: 1.6; }
                    a { display: inline-block; margin-top: 20px; background: linear-gradient(135deg, #6A44F2, #3C308C); color: #fff; text-decoration: none; padding: 12px 30px; border-radius: 10px; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>✅ Cuenta Eliminada</h2>
                    <p>La cuenta fue eliminada exitosamente.</p>
                    <p>Lamentamos las molestias. Si en el futuro querés crear una cuenta, serás bienvenido.</p>
                    <a href="/">Ir al Inicio</a>
                </div>
            </body>
            </html>
        ''')
    else:
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Error - Full Gaming</title>
                <style>
                    body { font-family: Arial, sans-serif; background: #1a1a2e; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
                    .card { background: #252540; padding: 40px; border-radius: 20px; text-align: center; max-width: 450px; border: 1px solid #3C308C; }
                    h2 { color: #e74c3c; }
                    p { color: #bbb; }
                    a { color: #6A44F2; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>⚠️ No se pudo eliminar</h2>
                    <p>{{ error }}</p>
                    <p>Es posible que el link ya haya sido usado o la cuenta ya no exista.</p>
                    <p><a href="/">Volver al inicio</a></p>
                </div>
            </body>
            </html>
        ''', error=resultado.get("error", "Error desconocido"))


@app.route('/perfil')
def perfil():
    """Mostrar página de perfil del usuario"""
    if 'usuario_id' not in session:
        return redirect('/acceso')
    
    usuario_id = session.get('usuario_id')
    usuario_nombre = session.get('usuario_nombre')
    usuario_email = session.get('usuario_email')
    
    # Obtener datos del usuario desde la BD (siempre actualizado)
    service = UsuarioService()
    usuario_datos = service.obtener_usuario_por_id(usuario_id)
    
    # Usar los datos de BD como fuente principal
    usuario_telefono = usuario_datos.get('telefono', '') if usuario_datos else ''
    usuario_dni = usuario_datos.get('dni', '') if usuario_datos else ''
    
    # Obtener últimos pedidos del usuario
    pedido_service = PedidoService()
    pedidos_recientes = pedido_service.obtener_pedidos_recientes(usuario_id, limite=5)
    
    return render_template('perfil.html', 
                         usuario=usuario_datos,
                         usuario_nombre=usuario_nombre,
                         usuario_apellido=usuario_datos.get('apellido') if usuario_datos else '',
                         usuario_email=usuario_email,
                         usuario_telefono=usuario_datos.get('telefono') if usuario_datos else '',
                         usuario_direccion=usuario_datos.get('direccion') if usuario_datos else '',
                         usuario_provincia=usuario_datos.get('provincia') if usuario_datos else '',
                         usuario_codigo_postal=usuario_datos.get('codigo_postal') if usuario_datos else '',
                         usuario_dni=usuario_datos.get('dni') if usuario_datos else '',
                         pedidos_recientes=pedidos_recientes)


@app.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    """Procesar compra y guardar en BD"""
    
    # Obtener carrito
    carrito = carrito_service.obtener_carrito()
    
    if not carrito:
        return jsonify({"ok": False, "error": "Carrito vacío"}), 400
    
    try:
        service_producto = ProductoService()
        service_pedido = PedidoService()
        
        # Obtener items de compra usando CarritoService
        items_compra = carrito_service.obtener_items_para_compra(service_producto)
        total = carrito_service.calcular_total(service_producto)
        
        # Obtener datos del usuario
        usuario_id = session.get('usuario_id')
        email = session.get('usuario_email', 'anonimo@email.com')
        
        # Inicializar variables de dirección y contacto
        direccion = None
        provincia = None
        codigo_postal = None
        dni = None
        telefono = None
        
        # Si el usuario está logueado, obtener su dirección principal y datos de contacto
        if usuario_id:
            from services.direccion_service import DireccionService
            from services.usuario_service import UsuarioService
            
            # Obtener dirección principal
            service_direccion = DireccionService()
            direcciones = service_direccion.obtener_direcciones(usuario_id)
            
            if direcciones:
                # Obtener la dirección principal o la primera
                dir_principal = next((d for d in direcciones if d.get('es_principal')), direcciones[0])
                direccion = f"{dir_principal.get('calle', '')} {dir_principal.get('numero', '')}"
                if dir_principal.get('piso_departamento'):
                    direccion += f", {dir_principal.get('piso_departamento')}"
                provincia = dir_principal.get('provincia')
                codigo_postal = dir_principal.get('codigo_postal')
            
            # Obtener datos de contacto del usuario
            service_usuario = UsuarioService()
            usuario_datos = service_usuario.obtener_usuario_por_id(usuario_id)
            if usuario_datos:
                dni = usuario_datos.get('dni')
                telefono = usuario_datos.get('telefono')
        
        # Crear pedido en BD con todos los datos
        resultado = service_pedido.crear_pedido(
            usuario_id, email, total, items_compra,
            direccion=direccion,
            provincia=provincia,
            codigo_postal=codigo_postal,
            dni=dni,
            telefono=telefono
        )
        
        if not resultado['ok']:
            return jsonify({"ok": False, "error": resultado['error']}), 500
        
        pedido_id = resultado['pedido_id']
        
        # Restar stock de cada producto
        for item in items_compra:
            service_producto.restar_stock(item['producto_id'], item['cantidad'])
        
        # Vaciar carrito usando CarritoService
        carrito_service.vaciar_carrito()
        
        return jsonify({
            "ok": True,
            "pedido_id": pedido_id,
            "total": total,
            "mensaje": "Compra realizada exitosamente"
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)