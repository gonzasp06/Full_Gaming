from flask import Flask, request, jsonify, render_template, session, redirect, url_for, abort
import mysql.connector
from datetime import timedelta

from database import conectar_base_datos
from services.admin_manager import AdminManager
from services.carrito_service import CarritoService

#Subir foto tipo archivo al servidor
import os
from werkzeug.utils import secure_filename #wsi
from math import ceil
import bcrypt #incripta contraseña 
from services.producto_service import ProductoService
from services.usuario_service import UsuarioService
from services.pedido_service import PedidoService 

# print("ProductoService:", ProductoService)

app = Flask(__name__)

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
    return render_template('index.html', productos=productos, pagina=pagina, total_paginas=total_paginas)

@app.route('/buscar')
def buscar_productos():
    termino = request.args.get('q', '').strip()

    if not termino:
        return redirect(url_for('mostrar_catalogo'))

    service = ProductoService()
    productos = service.buscar_productos(termino)

    return render_template('resultado_busqueda.html', productos=productos, termino=termino)

@app.route('/<categoria>')
def mostrar_catalogo_categoria(categoria):
    service = ProductoService()
    productos = service.filtrar_categoria(categoria)
    return render_template('categoria.html', productos=productos, categoria=categoria)

# Producto en detalle 
@app.route('/producto/<int:producto_id>')
def ver_producto(producto_id):
    service = ProductoService()
    producto = service.obtener_por_id(producto_id)

    if not producto:
        return abort(404)

    return render_template('producto_detalle.html', producto=producto)

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
        return jsonify({"mensaje": "Cuenta creada"}), 200
    else:
        return jsonify({"error": resultado["error"]}), 400



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
        email = request.form['email']
        contraseña = request.form['contraseña']
        usuario = service.login(email, contraseña)
        if usuario:
            session['usuario_id'] = usuario['id']  # ID del usuario
            session['usuario_email'] = usuario['email']  # Email en sesión 
            session['usuario_nombre'] = usuario['nombre']  # Nombre en sesión
            session['es_admin'] = usuario['is_admin']  # Si es admin
            session.permanent = True  # Mantener sesión
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
    return render_template('formulario_carga_producto.html')

@app.route('/gestion_productos')
@admin_manager.requerir_admin
def gestion_productos():
    service = ProductoService()
    productos = service.obtener_todos()
    return render_template('gestion_productos.html', productos=productos)

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
    producto = service.obtener_por_id(id_producto)
    return render_template('editar_producto.html', producto=producto)

@app.route('/actualizar_producto/<int:id_producto>', methods=['POST'])
@admin_manager.requerir_admin
def actualizar_producto(id_producto):
    service = ProductoService()

    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    categoria = request.form['categoria']
    precio = request.form['precio']
    cantidad = request.form['cantidad']

    foto = request.files.get('foto')
    ruta = None

    if foto and foto.filename:
        filename = secure_filename(foto.filename)
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(ruta)

    service.editar_producto(id_producto, nombre, descripcion, categoria, precio, cantidad, ruta)

    return redirect('/gestion_productos')


# ==================== GESTION DE USUARIOS ====================
@app.route('/usuarios')
@admin_manager.requerir_admin
def gestion_usuarios():
    service = UsuarioService()
    usuarios = service.obtener_todos()
    return render_template('gestion_usuarios.html', usuarios=usuarios)


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
        precio=precio,
        cantidad=cantidad,
        ruta_imagen=ruta_imagen
    )

    if resultado.get("ok"):
        return jsonify({"mensaje": "Producto cargado correctamente"}), 200
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


@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('mostrar_catalogo'))


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
        
        # Crear pedido en BD
        resultado = service_pedido.crear_pedido(usuario_id, email, total, items_compra)
        
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