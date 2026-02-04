# 📦 BASE DE DATOS, CARRITO Y APP - Guía Técnica Completa

## 📚 Índice
1. [Base de Datos](#base-de-datos)
2. [Cómo Funciona el Carrito](#cómo-funciona-el-carrito)
3. [Cómo Funciona la App](#cómo-funciona-la-app)
4. [Flujos Completos](#flujos-completos)

---

## 📊 Base de Datos

### **Ubicación y Configuración**
```
DATABASE: catalogo
HOST: localhost
USER: root
PASSWORD: 12345
```

### **Conexión desde Python**
```python
# database.py
import mysql.connector

def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="catalogo"
    )
```

---

### **Tabla 1: PRODUCTO**

**Propósito:** Almacenar todos los productos disponibles en la tienda

```sql
CREATE TABLE `producto` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(100),
    `descripcion` TEXT,
    `categoria` VARCHAR(100),
    `precio` DECIMAL(10,2),
    `cantidad` INT,              -- Stock disponible
    `foto` VARCHAR(255),         -- Ruta a imagen
    PRIMARY KEY (`id`)
)
```

**Estructura de datos:**
```
id      | nombre              | descripcion | categoria    | precio  | cantidad | foto
--------|---------------------|-------------|--------------|---------|----------|----------
13      | Lavarropas...       | Disfrutá... | Electrodómésticos | 89249 | 5 | /static/uploads/...
15      | Microondas...       | El botón... | Electrodómésticos | 744999 | 9 | /static/uploads/...
18      | Android TV Philips  | Ya sea... | TV_Video       | 524699 | 9 | /static/uploads/...
28      | Smart TV 65" 4K...  | El Smart... | TV_Video       | 1099999 | 2 | /static/uploads/...
```

**Campos importantes:**
- `id`: Identificador único (AUTO_INCREMENT)
- `precio`: Decimal con 2 decimales (99999.99)
- `cantidad`: Stock disponible (se resta al comprar)
- `foto`: Ruta donde se guardó la imagen

**Operaciones principales:**
```sql
-- Obtener todos los productos
SELECT * FROM producto;

-- Obtener producto por ID
SELECT * FROM producto WHERE id = 28;

-- Filtrar por categoría
SELECT * FROM producto WHERE categoria = 'Electrodómésticos';

-- Buscar por nombre (LIKE)
SELECT * FROM producto WHERE nombre LIKE '%Smart%';

-- Paginar (9 productos por página)
SELECT * FROM producto LIMIT 0, 9;    -- Página 1
SELECT * FROM producto LIMIT 9, 9;    -- Página 2

-- Restar stock al comprar
UPDATE producto SET cantidad = cantidad - 2 WHERE id = 28;

-- Insertar nuevo producto
INSERT INTO producto (nombre, descripcion, categoria, precio, cantidad, foto)
VALUES ('Nuevo TV', 'Descripción', 'TV_Video', 5000, 10, '/path/foto.jpg');
```

---

### **Tabla 2: USUARIO**

**Propósito:** Almacenar usuarios registrados de la aplicación

```sql
CREATE TABLE `usuario` (
    `idusuario` INT NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(50) NOT NULL,
    `apellido` VARCHAR(50) NOT NULL,
    `email` VARCHAR(50) NOT NULL UNIQUE,
    `contraseña` VARCHAR(255) NOT NULL,    -- Cifrada con bcrypt
    PRIMARY KEY (`idusuario`),
    UNIQUE KEY `email_UNIQUE` (`email`)
)
```

**Estructura de datos:**
```
idusuario | nombre   | apellido    | email              | contraseña (cifrada)
----------|----------|-------------|--------------------|-----------------------------------------
14        | Juan     | Perez       | juan@example.com   | $2b$12$VBLLKIlD4P4aLZn3Po18n...
17        | María    | García      | maria@example.com  | $2b$12$ibFZeOov2ZZZKtRkleQfJuu...
20        | Carlos   | Martínez    | carlos@example.com | $2b$12$/JGvnWbOwa9En8yNN1WkRO...
```

**Campos importantes:**
- `idusuario`: ID del usuario (AUTO_INCREMENT)
- `email`: UNIQUE (no pueden haber dos usuarios con el mismo email)
- `contraseña`: Cifrada con bcrypt (NO se puede desencriptar, solo verificar)

**Operaciones principales:**
```sql
-- Crear usuario
INSERT INTO usuario (nombre, apellido, email, contraseña)
VALUES ('Juan', 'Perez', 'juan@example.com', '$2b$12$...');

-- Buscar usuario por email
SELECT * FROM usuario WHERE email = 'juan@example.com';

-- Obtener por ID
SELECT * FROM usuario WHERE idusuario = 14;

-- Actualizar información
UPDATE usuario SET nombre = 'Juan Carlos' WHERE idusuario = 14;
```

---

### **Tabla 3: PEDIDOS** (Opcional, no está en tu código actual)

**Propósito:** Guardar histórico de compras

```sql
CREATE TABLE `pedidos` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `usuario_id` INT,
    `email` VARCHAR(150),
    `total` DECIMAL(10, 2),
    `estado` VARCHAR(50),           -- 'completado', 'pendiente'
    `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`usuario_id`) REFERENCES usuario(idusuario)
)
```

---

### **Tabla 4: PEDIDO_ITEMS** (Opcional, no está en tu código actual)

**Propósito:** Detalle de cada producto en una compra

```sql
CREATE TABLE `pedido_items` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `pedido_id` INT,
    `producto_id` INT,
    `cantidad` INT,
    `precio` DECIMAL(10, 2),
    `subtotal` DECIMAL(10, 2),
    FOREIGN KEY (`pedido_id`) REFERENCES pedidos(id),
    FOREIGN KEY (`producto_id`) REFERENCES producto(id)
)
```

---

## 🛒 Cómo Funciona el Carrito

### **¿Dónde se guarda el carrito?**

**En la SESSION del navegador**, no en base de datos.

```
[Navegador del Usuario]
    │
    └─> session['carrito'] = {
            '28': 2,      # Producto ID 28, cantidad 2
            '15': 1,      # Producto ID 15, cantidad 1
            '40': 3       # Producto ID 40, cantidad 3
        }
```

---

### **Estructura del Carrito**

```python
# Es un diccionario Python/JSON
session['carrito'] = {
    'producto_id': cantidad,
    'producto_id': cantidad,
    # ...
}

# Ejemplo real:
session['carrito'] = {
    '28': 2,     # Smart TV (ID 28), cantidad 2
    '15': 1,     # Microondas (ID 15), cantidad 1
}
```

---

### **Métodos del CarritoService**

#### 1️⃣ **obtener_carrito()**
```python
def obtener_carrito(self):
    """Obtiene el carrito actual de session"""
    return session.get('carrito', {})

# Retorna: {'28': 2, '15': 1} o {} si está vacío
```

---

#### 2️⃣ **agregar_item(producto_id, cantidad)**
```python
def agregar_item(self, producto_id, cantidad=1):
    """Agrega un producto al carrito"""
    
    # Paso 1: Si no existe carrito, lo crea
    if 'carrito' not in session:
        session['carrito'] = {}
    
    # Paso 2: Convierte el ID a string (para usar como clave)
    producto_id_str = str(producto_id)
    
    # Paso 3: Si ya está el producto, suma cantidad
    if producto_id_str in session['carrito']:
        session['carrito'][producto_id_str] += cantidad
    # Paso 4: Si no está, lo agrega
    else:
        session['carrito'][producto_id_str] = cantidad
    
    # Paso 5: Marca la sesión como modificada (para guardar en cookie)
    session.modified = True

# Ejemplo:
# Antes: session['carrito'] = {'28': 1}
# carrito_service.agregar_item(28, 1)
# Después: session['carrito'] = {'28': 2}
```

---

#### 3️⃣ **eliminar_item(producto_id)**
```python
def eliminar_item(self, producto_id):
    """Elimina un producto del carrito"""
    
    if 'carrito' in session:
        carrito = session['carrito']
        producto_id_str = str(producto_id)
        
        # Si existe, lo elimina
        if producto_id_str in carrito:
            del carrito[producto_id_str]
            session.modified = True

# Ejemplo:
# Antes: session['carrito'] = {'28': 2, '15': 1}
# carrito_service.eliminar_item(28)
# Después: session['carrito'] = {'15': 1}
```

---

#### 4️⃣ **actualizar_cantidad(producto_id, cantidad)**
```python
def actualizar_cantidad(self, producto_id, cantidad):
    """Cambia la cantidad de un producto"""
    
    # Validar que cantidad > 0
    if cantidad <= 0:
        return False
    
    if 'carrito' not in session:
        return False
    
    producto_id_str = str(producto_id)
    
    # Si existe, actualiza la cantidad
    if producto_id_str in session['carrito']:
        session['carrito'][producto_id_str] = cantidad
        session.modified = True
        return True
    
    return False

# Ejemplo:
# Antes: session['carrito'] = {'28': 2}
# carrito_service.actualizar_cantidad(28, 5)
# Después: session['carrito'] = {'28': 5}
```

---

#### 5️⃣ **calcular_total(producto_service)**
```python
def calcular_total(self, producto_service):
    """Calcula el total a pagar"""
    
    carrito = self.obtener_carrito()
    total = 0
    
    # Por cada producto en el carrito
    for producto_id, cantidad in carrito.items():
        # Obtiene los datos del producto de la BD
        producto = producto_service.obtener_por_id(int(producto_id))
        
        if producto:
            # producto[4] es el precio (índice de la tupla)
            precio = float(producto[4])
            # Suma al total
            total += precio * cantidad
    
    return total

# Ejemplo:
# session['carrito'] = {'28': 2, '15': 1}
# Smart TV (28) cuesta $1,099,999
# Microondas (15) cuesta $744,999
# Total = (1,099,999 * 2) + (744,999 * 1) = $2,944,997
```

---

#### 6️⃣ **obtener_items_detalle(producto_service)**
```python
def obtener_items_detalle(self, producto_service):
    """Obtiene carrito con información completa de cada producto"""
    
    carrito = self.obtener_carrito()
    items = []
    
    # Por cada producto en el carrito
    for producto_id, cantidad in carrito.items():
        # Obtiene datos de la BD
        producto = producto_service.obtener_por_id(int(producto_id))
        
        if producto:
            precio = float(producto[4])
            # Crea objeto con info completa
            items.append({
                'id': producto[0],              # ID del producto
                'nombre': producto[1],          # Nombre
                'precio': precio,               # Precio unitario
                'cantidad': cantidad,           # Cantidad en carrito
                'subtotal': precio * cantidad,  # Subtotal
                'foto': producto[6]             # Foto
            })
    
    return items

# Retorna:
[
    {
        'id': 28,
        'nombre': 'Smart TV 65" 4K...',
        'precio': 1099999,
        'cantidad': 2,
        'subtotal': 2199998,
        'foto': '/static/uploads/Smart_Tv_65_...'
    },
    {
        'id': 15,
        'nombre': 'Microondas de Integración...',
        'precio': 744999,
        'cantidad': 1,
        'subtotal': 744999,
        'foto': '/static/uploads/Microondas_...'
    }
]
```

---

#### 7️⃣ **vaciar_carrito()**
```python
def vaciar_carrito(self):
    """Limpia todo el carrito"""
    
    if 'carrito' in session:
        session['carrito'] = {}
        session.modified = True

# Antes: session['carrito'] = {'28': 2, '15': 1}
# carrito_service.vaciar_carrito()
# Después: session['carrito'] = {}
```

---

## 🚀 Cómo Funciona la App

### **Estructura de app.py**

```
app.py
├── Importaciones de librerías
├── Crear instancia de Flask
├── Configurar Flask (secret_key, session, etc)
├── Instanciar servicios globales
├── Rutas de Producto (mostrar, buscar, detalles)
├── Rutas de Usuario (registro, login, logout)
├── Rutas de Carrito (agregar, ver, actualizar, comprar)
├── Rutas de Admin (gestión de productos)
└── Ejecutar app
```

---

### **1. Inicialización**

```python
from flask import Flask, session, render_template, redirect, url_for
from services.carrito_service import CarritoService
from services.admin_manager import AdminManager
from datetime import timedelta

# Crear aplicación Flask
app = Flask(__name__)

# Configurar contraseña de sesión (clave secreta)
app.secret_key = '5x7#YI6+W<i{n^$V5y4ZHf7'

# Sesiones persistan 7 días
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No accesible desde JS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Seguridad CSRF

# Hacer permanentes todas las sesiones
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)

# Instanciar servicios GLOBALES (sin conexión a BD)
admin_manager = AdminManager()
carrito_service = CarritoService()

# Carpeta para subir archivos
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
```

---

### **2. Rutas de PRODUCTO**

#### **GET / - Página Principal (Catálogo)**
```python
@app.route('/')
@app.route('/<int:pagina>')
def mostrar_catalogo(pagina=1):
    """Muestra productos paginados (9 por página)"""
    
    # Crear instancia LOCAL
    service = ProductoService()
    
    # Obtener productos de esta página
    productos = service.obtener_paginados(pagina, 9)
    
    # Obtener cantidad total para calcular páginas
    total_productos = len(service.obtener_todos())
    total_paginas = ceil(total_productos / 9)
    
    # Renderizar template
    return render_template('index.html',
        productos=productos,
        pagina=pagina,
        total_paginas=total_paginas
    )
```

#### **GET /buscar - Buscar Productos**
```python
@app.route('/buscar')
def buscar_productos():
    """Busca productos por término"""
    
    # Obtener parámetro de URL ?q=termino
    termino = request.args.get('q', '').strip()
    
    # Si no hay término, volver a catálogo
    if not termino:
        return redirect(url_for('mostrar_catalogo'))
    
    service = ProductoService()
    productos = service.buscar_productos(termino)
    
    return render_template('resultado_busqueda.html',
        productos=productos,
        termino=termino
    )
```

#### **GET /<categoria> - Productos por Categoría**
```python
@app.route('/<categoria>')
def mostrar_catalogo_categoria(categoria):
    """Filtra productos por categoría"""
    
    service = ProductoService()
    productos = service.filtrar_categoria(categoria)
    
    return render_template('categoria.html',
        productos=productos,
        categoria=categoria
    )
```

#### **GET /producto/<id> - Detalle del Producto**
```python
@app.route('/producto/<int:producto_id>')
def ver_producto(producto_id):
    """Muestra detalle completo de un producto"""
    
    service = ProductoService()
    producto = service.obtener_por_id(producto_id)
    
    # Si no existe, error 404
    if not producto:
        return abort(404)
    
    return render_template('producto_detalle.html', producto=producto)
```

---

### **3. Rutas de USUARIO**

#### **GET /nuevo_usuario - Formulario Registro**
```python
@app.route('/nuevo_usuario')
def crear_usuario():
    """Mostrar formulario de registro"""
    return render_template('f_nuevo_usuario.html')
```

#### **POST /cargar_usuario - Procesar Registro**
```python
@app.route('/cargar_usuario', methods=['POST'])
def cargar_usuario():
    """Crea nuevo usuario en BD"""
    
    service = UsuarioService()
    datos = request.form
    
    # Llamar al servicio para crear usuario
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
```

#### **GET /cuenta - Formulario Login**
```python
@app.route('/cuenta', methods=['GET', 'POST'])
def acceso_cuentas():
    """Mostrar formulario o procesar login"""
    
    if request.method == 'POST':
        service = UsuarioService()
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        # Llamar a login
        usuario = service.login(email, contraseña)
        
        if usuario:
            # Guardar en sesión
            session['usuario_id'] = usuario['id']
            session['usuario_email'] = usuario['email']
            session['usuario_nombre'] = usuario['nombre']
            session['es_admin'] = usuario['is_admin']
            session.permanent = True
            
            return jsonify({"mensaje": "Login exitoso"}), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    
    return render_template('acceso.html')
```

#### **GET /logout - Cerrar Sesión**
```python
@app.route('/logout')
def logout():
    """Limpia la sesión y redirige"""
    session.clear()
    return redirect(url_for('mostrar_catalogo'))
```

---

### **4. Rutas de CARRITO**

#### **GET /carrito - Ver Carrito**
```python
@app.route('/carrito')
def ver_carrito():
    """Muestra el carrito con detalles"""
    
    producto_service = ProductoService()
    
    # Obtener items del carrito con info completa
    items = carrito_service.obtener_items_detalle(producto_service)
    
    # Calcular total
    total = carrito_service.calcular_total(producto_service)
    
    return render_template('carrito.html',
        items=items,
        total=total,
        usuario_logueado=usuario_logueado()
    )
```

#### **POST /agregar_carrito/<id> - Agregar al Carrito**
```python
@app.route('/agregar_carrito/<int:id_producto>', methods=['POST'])
def agregar_carrito(id_producto):
    """Agrega un producto al carrito"""
    
    # Obtener cantidad del form
    datos = request.get_json() or request.form
    cantidad = int(datos.get('cantidad', 1))
    
    # Validar que existe el producto
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    
    if not producto:
        return jsonify({"ok": False, "error": "Producto no existe"}), 404
    
    # Validar que hay stock
    stock = producto[5]  # Índice 5 es cantidad
    if stock <= 0:
        return jsonify({"ok": False, "error": "Producto agotado"}), 400
    
    # Agregar usando CarritoService
    carrito_service.agregar_item(id_producto, cantidad)
    
    return jsonify({"ok": True, "mensaje": "Producto agregado"}), 200
```

#### **POST /eliminar_carrito/<id> - Eliminar del Carrito**
```python
@app.route('/eliminar_carrito/<int:id_producto>', methods=['POST'])
def eliminar_carrito(id_producto):
    """Elimina un producto del carrito"""
    
    carrito_service.eliminar_item(id_producto)
    return jsonify({"ok": True}), 200
```

#### **POST /actualizar_carrito/<id> - Actualizar Cantidad**
```python
@app.route('/actualizar_carrito/<int:id_producto>', methods=['POST'])
def actualizar_carrito(id_producto):
    """Actualiza la cantidad de un producto"""
    
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
    
    # Actualizar
    if carrito_service.actualizar_cantidad(id_producto, cantidad):
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"ok": False, "error": "Error al actualizar"}), 400
```

#### **POST /procesar_compra - Finalizar Compra**
```python
@app.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    """Procesa la compra y guarda en BD"""
    
    # Obtener carrito
    carrito = carrito_service.obtener_carrito()
    
    if not carrito:
        return jsonify({"ok": False, "error": "Carrito vacío"}), 400
    
    try:
        service_producto = ProductoService()
        service_pedido = PedidoService()
        
        # Obtener items formateados para compra
        items_compra = carrito_service.obtener_items_para_compra(service_producto)
        total = carrito_service.calcular_total(service_producto)
        
        # Datos del usuario
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
        
        # Vaciar carrito
        carrito_service.vaciar_carrito()
        
        return jsonify({
            "ok": True,
            "pedido_id": pedido_id,
            "total": total,
            "mensaje": "Compra realizada exitosamente"
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
```

---

### **5. Rutas de ADMIN**

#### **GET /gestion_productos - Ver Todos los Productos (ADMIN)**
```python
@app.route('/gestion_productos')
@admin_manager.requerir_admin  # ← Solo ADMIN
def gestion_productos():
    """Mostrar todos los productos para gestionar"""
    
    service = ProductoService()
    productos = service.obtener_todos()
    
    return render_template('gestion_productos.html', productos=productos)
```

#### **POST /cargar_producto - Crear Producto (ADMIN)**
```python
@app.route('/cargar_producto', methods=['POST'])
@admin_manager.requerir_admin  # ← Solo ADMIN
def cargar_producto():
    """Inserta nuevo producto en BD"""
    
    # Obtener datos del form
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    categoria = request.form.get('categoria')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    
    # Procesar foto
    foto = request.files.get('foto')
    
    if foto and foto.filename:
        filename = secure_filename(foto.filename)
        ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(ruta_imagen)
    else:
        ruta_imagen = None
    
    # Insertar en BD
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
        return jsonify({"mensaje": "Producto cargado"}), 200
    else:
        # Si falló, borrar la imagen para no dejar basura
        if ruta_imagen and os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
        return jsonify({"error": resultado.get("error")}), 500
```

#### **GET /editar_producto/<id> - Editar Producto (ADMIN)**
```python
@app.route('/editar_producto/<int:id_producto>')
@admin_manager.requerir_admin  # ← Solo ADMIN
def editar_producto(id_producto):
    """Mostrar formulario para editar producto"""
    
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    
    return render_template('editar_producto.html', producto=producto)
```

#### **POST /actualizar_producto/<id> - Guardar Cambios (ADMIN)**
```python
@app.route('/actualizar_producto/<int:id_producto>', methods=['POST'])
@admin_manager.requerir_admin  # ← Solo ADMIN
def actualizar_producto(id_producto):
    """Actualiza producto en BD"""
    
    service = ProductoService()
    
    # Obtener datos
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    categoria = request.form['categoria']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    
    # Procesar foto (opcional)
    foto = request.files.get('foto')
    ruta = None
    
    if foto and foto.filename:
        filename = secure_filename(foto.filename)
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(ruta)
    
    # Actualizar
    service.editar_producto(id_producto, nombre, descripcion, categoria, precio, cantidad, ruta)
    
    return redirect('/gestion_productos')
```

#### **GET /eliminar_producto/<id> - Borrar Producto (ADMIN)**
```python
@app.route('/eliminar_producto/<int:id_producto>')
@admin_manager.requerir_admin  # ← Solo ADMIN
def eliminar_producto(id_producto):
    """Elimina producto de BD"""
    
    service = ProductoService()
    service.eliminar_producto(id_producto)
    
    return redirect('/gestion_productos')
```

---

## 📈 Flujos Completos

### **FLUJO 1: Usuario se Registra**

```
1. Usuario accede a /nuevo_usuario
   └─> Ve formulario HTML

2. Usuario completa formulario y envía (POST /cargar_usuario)
   ├─> UsuarioService.crear_usuario(nombre, apellido, email, contraseña)
   ├─> Cifra contraseña con bcrypt
   ├─> Valida que email sea único
   ├─> INSERT INTO usuario (nombre, apellido, email, contraseña_cifrada)
   └─> Retorna {"ok": True}

3. JavaScript redirige a /cuenta (formulario login)
```

---

### **FLUJO 2: Usuario se Loguea**

```
1. Usuario accede a /cuenta
   └─> Ve formulario login

2. Usuario entra email/contraseña (POST /cuenta)
   ├─> UsuarioService.login(email, contraseña)
   ├─> SELECT * FROM usuario WHERE email = ?
   ├─> bcrypt.checkpw(contraseña, hash_guardado) → True/False
   └─> Si válido, retorna datos del usuario

3. App guarda en SESSION:
   ├─> session['usuario_id'] = 14
   ├─> session['usuario_email'] = 'juan@example.com'
   ├─> session['usuario_nombre'] = 'Juan'
   ├─> session['es_admin'] = 0
   └─> session.permanent = True

4. JavaScript redirige a /
   └─> Usuario logueado ✅
```

---

### **FLUJO 3: Usuario Agrega Producto al Carrito**

```
1. Usuario en /producto/28 hace click "Agregar al Carrito"
   └─> Envía POST a /agregar_carrito/28

2. App valida:
   ├─> ProductoService.obtener_por_id(28) → Obtiene de BD
   ├─> Si no existe → ERROR
   ├─> Si stock <= 0 → ERROR "Agotado"
   └─> Si todo ok → continúa

3. App agrega al carrito:
   ├─> CarritoService.agregar_item(28, cantidad=2)
   ├─> Si no existe session['carrito'], lo crea
   ├─> session['carrito']['28'] = 2
   ├─> session.modified = True
   └─> Retorna {"ok": True}

4. Session del navegador se actualiza
   └─> Cookie se envía al cliente

5. Usuario accede a /carrito
   ├─> CarritoService.obtener_items_detalle(producto_service)
   ├─> Por cada item en session['carrito']:
   │   ├─> ProductoService.obtener_por_id(id)
   │   └─> Obtiene nombre, precio, foto, etc
   ├─> Retorna lista con info completa
   └─> Renderiza HTML con los items
```

---

### **FLUJO 4: Usuario Compra**

```
1. Usuario en /carrito hace click "Comprar"
   └─> POST a /procesar_compra

2. App valida:
   ├─> Obtiene session['carrito']
   ├─> Si vacío → ERROR
   └─> Si tiene items → continúa

3. App crea pedido:
   ├─> PedidoService.crear_pedido(usuario_id, email, total, items)
   ├─> INSERT INTO pedidos (usuario_id, email, total, estado)
   ├─> Obtiene pedido_id = último ID insertado
   ├─> Por cada item:
   │   └─> INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio, subtotal)
   └─> Retorna {"ok": True, "pedido_id": X}

4. App reduce stock:
   ├─> Por cada producto en carrito:
   │   └─> ProductoService.restar_stock(producto_id, cantidad)
   │       └─> UPDATE producto SET cantidad = cantidad - X WHERE id = Y
   └─> Todos los productos actualizados

5. App vacía carrito:
   ├─> CarritoService.vaciar_carrito()
   ├─> session['carrito'] = {}
   ├─> session.modified = True
   └─> Carrito limpio

6. JavaScript redirige a página de confirmación
   └─> Compra exitosa ✅
```

---

### **FLUJO 5: Admin Crea Producto**

```
1. Admin accede a /formulario
   ├─> @admin_manager.requerir_admin valida
   ├─> Si es_admin() == False → ERROR 403
   └─> Si es_admin() == True → Ver formulario

2. Admin completa y envía (POST /cargar_producto)
   ├─> @admin_manager.requerir_admin valida nuevamente
   ├─> Obtiene datos del form
   ├─> Obtiene archivo de foto
   ├─> secure_filename(foto.filename) → Nombre seguro
   ├─> foto.save('/static/uploads/nombre.jpg')
   └─> Foto guardada en servidor

3. App inserta en BD:
   ├─> ProductoService.agregar_producto(datos)
   ├─> INSERT INTO producto (nombre, descripcion, categoria, precio, cantidad, foto)
   └─> Retorna {"ok": True}

4. Admin ve en /gestion_productos
   └─> SELECT * FROM producto
       └─> Aparece el nuevo producto
```

---

## 📋 Resumen: Todo Conectado

```
USUARIO
  │
  └─> SESSION
      ├─> usuario_id
      ├─> usuario_email
      ├─> es_admin
      └─> carrito = {'28': 2, '15': 1}

CARRITO (Session)
  │
  └─> Cuando compra:
      ├─> Obtiene items con obtener_items_para_compra()
      ├─> PedidoService crea orden en BD
      ├─> ProductoService resta stock
      └─> session['carrito'] = {}

BASE DE DATOS
  ├─> PRODUCTO: Almacena todos los artículos
  ├─> USUARIO: Usuarios registrados
  ├─> PEDIDOS: Órdenes completadas (opcional)
  └─> PEDIDO_ITEMS: Detalles de cada orden (opcional)

APP.PY
  ├─> Rutas de PRODUCTO
  ├─> Rutas de USUARIO
  ├─> Rutas de CARRITO
  └─> Rutas de ADMIN (protegidas)
```

---

**Última actualización:** 18 de diciembre de 2025
