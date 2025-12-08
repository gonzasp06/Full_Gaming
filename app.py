from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import mysql.connector

from database import conectar_base_datos

#Subir foto tipo archivo al servidor
import os
from werkzeug.utils import secure_filename #wsi
from math import ceil
import bcrypt #incripta contraseña 
from services.producto_service import ProductoService
from services.usuario_service import UsuarioService 

print("ProductoService:", ProductoService)


app = Flask(__name__)

# Carpeta para imágenes
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = '5x7#YI6+W<i{n^$V5y4ZHf7' #clave secreta para sesiones

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


def obtener_productos(): #obtiene los datos de la base de datos
    cursor= conexion.cursor()
    consulta= 'SELECT * FROM catalogo.producto;'
    cursor.execute(consulta) 
    productos=cursor.fetchall() #obtine el resultado de la consulta
    cursor.close()
    return productos

productos_por_pagina = 9

#paginado 
def obtener_productos_paginados(pagina): #paremetro de la "pagina" obtine subconjunto paginado
    inicio = (pagina - 1) * productos_por_pagina
    fin = inicio + productos_por_pagina
    cursor = conexion.cursor() 
    consulta = 'SELECT * FROM catalogo.producto LIMIT %s, %s;' 
    cursor.execute(consulta, (inicio, productos_por_pagina))
    productos = cursor.fetchall() 
    cursor.close()
    return productos

# Ruta raíz
@app.route('/') #define ruta principal 
@app.route('/<int:pagina>')
def mostrar_catalogo(pagina=1): 
    service = ProductoService()
    productos = service.obtener_paginados(pagina, 9)
    total_productos = len(obtener_productos())
    total_paginas = ceil(total_productos / 9)
    return render_template('index.html', productos=productos, pagina=pagina, total_paginas=total_paginas)

def filtrar_categoria(categoria_seleccionada):
    cursor = conexion.cursor()
    consulta = 'SELECT * FROM catalogo.producto WHERE categoria = %s;'
    cursor.execute(consulta, (categoria_seleccionada, ))
    productos = cursor.fetchall()
    cursor.close()
    return productos

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
    productos = filtrar_categoria(categoria)
    return render_template('categoria.html', productos=productos, categoria=categoria)


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



# BUSCAR USUARIO POR EMAIL (USADO PARA TEST)

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
            session['usuario'] = usuario ['email']  # Guardar email en sesión 
            session['nombre'] = usuario ['nombre']  # Guardar nombre en sesión
            session['es_admin'] = usuario.get('es_admin', 0)  # Guardar si es admin en sesión
            return redirect(url_for('index'))
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401

    return render_template('f_acceso.html')

def es_admin_logueado():
    return session.get('es_admin') == 0
# -----------------------------------------
# FORM LOGIN (VISTA SIMPLE)
# -----------------------------------------
@app.route('/acceso')
def render_acceso():
    return render_template('acceso.html')
# Ruta para cargar un nuevo producto
@app.route('/formulario')
def carga_producto():
    return render_template('formulario_carga_producto.html')

@app.route('/gestion_productos')
def gestion_productos():
    service = ProductoService()
    productos = service.obtener_todos()
    return render_template('gestion_productos.html', productos=productos)

@app.route('/eliminar_producto/<int:id_producto>')
def eliminar_producto(id_producto):
    service = ProductoService()
    service.eliminar_producto(id_producto)
    return redirect('/gestion_productos')

@app.route('/editar_producto/<int:id_producto>')
def editar_producto(id_producto):
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    return render_template('editar_producto.html', producto=producto)

@app.route('/actualizar_producto/<int:id_producto>', methods=['POST'])
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


@app.route('/cargar_producto', methods=['POST'])
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)