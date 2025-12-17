# 📚 DOCUMENTACIÓN COMPLETA DEL SISTEMA FULL GAMING

## Índice
1. [Introducción](#introducción)
2. [Arquitectura General](#arquitectura-general)
3. [Base de Datos](#base-de-datos)
4. [Servicios y Clases](#servicios-y-clases)
5. [Sistema de Autenticación](#sistema-de-autenticación)
6. [Flujo de Usuario](#flujo-de-usuario)
7. [Flujo de Administrador](#flujo-de-administrador)
8. [Sistema de Carrito de Compras](#sistema-de-carrito-de-compras)
9. [Manejo de Sesiones](#manejo-de-sesiones)
10. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Introducción

**Full Gaming** es un e-commerce desarrollado para la venta de hardware y software de computación. El sistema permite a los usuarios navegar productos, realizar compras, y a los administradores gestionar el catálogo.

### Tecnologías Utilizadas
- **Backend**: Python con Flask (framework web)
- **Base de Datos**: MySQL
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Seguridad**: bcrypt (encriptación de contraseñas)
- **Gestión de Archivos**: werkzeug (manejo seguro de uploads)

---

## Arquitectura General

El sistema sigue el patrón **MVC (Modelo-Vista-Controlador)** adaptado:

```
Full_Gaming/
│
├── app.py                    # Controlador principal (rutas y lógica)
├── database.py              # Configuración de conexión a BD
├── crear_admin.py           # Script para crear usuarios admin
│
├── services/                # Capa de Servicios (lógica de negocio)
│   ├── producto_service.py
│   ├── usuario_service.py
│   ├── carrito_service.py
│   ├── pedido_service.py
│   └── admin_manager.py
│
├── templates/               # Vistas (HTML)
│   ├── index.html
│   ├── acceso.html
│   ├── carrito.html
│   └── ...
│
└── static/                  # Archivos estáticos
    ├── uploads/            # Imágenes de productos
    └── ...
```

### Flujo de Datos

```
Usuario → Flask (app.py) → Service → Base de Datos → Service → Flask → Usuario
         [Controlador]    [Modelo]    [MySQL]      [Modelo]  [Vista]
```

---

## Base de Datos

### Estructura de Tablas

#### 1. Tabla `producto`
Almacena el catálogo de productos disponibles para la venta.

```sql
CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `categoria` varchar(100) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `foto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
```

**Ejemplo de registro:**
```
id: 18
nombre: "Android TV Philips LED 4K 50\" HDR+"
descripcion: "Ya sea que veas una película hoy, programas y partidos mañana..."
categoria: "TV_Video"
precio: 524699.00
cantidad: 9
foto: "static/uploads/55PUD7406-77.webp"
```

#### 2. Tabla `usuario`
Almacena información de usuarios registrados.

```sql
CREATE TABLE `usuario` (
  `idusuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `is_admin` tinyint DEFAULT 0,
  PRIMARY KEY (`idusuario`),
  UNIQUE KEY `email_UNIQUE` (`email`)
);
```

**Ejemplo de registro:**
```
idusuario: 14
nombre: "Juan"
apellido: "Perez"
email: "juan@example.com"
contraseña: "$2b$12$VBLLKIlD4P4aLZn3Po18n..." (encriptada con bcrypt)
is_admin: 0
```

#### 3. Tabla `pedidos`
Registra las compras realizadas.

```sql
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` varchar(20) DEFAULT 'completado',
  `fecha` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);
```

#### 4. Tabla `pedido_items`
Detalle de productos en cada pedido.

```sql
CREATE TABLE `pedido_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
);
```

### Relaciones entre Tablas

```
usuario (1) ----< (*) pedidos
                        |
                        |
                        v
                  pedido_items >---- (*) producto
```

---

## Servicios y Clases

El sistema utiliza **clases de servicio** para separar la lógica de negocio de las rutas.

### 1. ProductoService

**Ubicación**: `services/producto_service.py`

**Responsabilidad**: Gestionar todas las operaciones relacionadas con productos.

#### Métodos principales:

```python
class ProductoService:
    def __init__(self):
        self.conexion = conectar_base_datos()
    
    # Obtener todos los productos
    def obtener_todos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM catalogo.producto")
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    # Obtener productos con paginación
    def obtener_paginados(self, pagina, por_pagina):
        inicio = (pagina - 1) * por_pagina
        cursor = self.conexion.cursor()
        cursor.execute(
            'SELECT * FROM catalogo.producto LIMIT %s, %s',
            (inicio, por_pagina)
        )
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    # Buscar productos por término
    def buscar_productos(self, termino):
        cursor = self.conexion.cursor()
        like = f"%{termino}%"
        consulta = """
            SELECT * FROM catalogo.producto
            WHERE nombre LIKE %s OR descripcion LIKE %s OR categoria LIKE %s
        """
        cursor.execute(consulta, (like, like, like))
        productos = cursor.fetchall()
        cursor.close()
        return productos
```

**Ejemplo de uso en app.py:**
```python
@app.route('/')
@app.route('/<int:pagina>')
def mostrar_catalogo(pagina=1):
    service = ProductoService()
    productos = service.obtener_paginados(pagina, 9)
    total_productos = len(service.obtener_todos())
    total_paginas = ceil(total_productos / 9)
    return render_template('index.html', 
                         productos=productos, 
                         pagina=pagina, 
                         total_paginas=total_paginas)
```

### 2. UsuarioService

**Ubicación**: `services/usuario_service.py`

**Responsabilidad**: Gestionar usuarios, autenticación y registro.

#### Características de Seguridad:

1. **Encriptación de contraseñas con bcrypt**:
```python
def crear_usuario(self, nombre, apellido, email, contraseña):
    # Cifrar contraseña antes de guardarla
    hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    
    cursor = self.conexion.cursor()
    query = """
        INSERT INTO usuario (nombre, apellido, email, contraseña)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, apellido, email, hashed))
    self.conexion.commit()
```

**¿Por qué bcrypt?**
- Genera un "salt" único para cada contraseña
- Es computacionalmente costoso (protege contra fuerza bruta)
- Nunca almacena la contraseña en texto plano

2. **Login seguro**:
```python
def login(self, email, contraseña):
    usuario = self.buscar_usuario(email)
    
    if not usuario:
        return None
    
    # Verificar contraseña sin desencriptarla
    hash_guardado = usuario["contraseña"]
    resultado = bcrypt.checkpw(contraseña.encode('utf-8'), hash_guardado)
    
    if resultado:
        return usuario
    else:
        return None
```

**Ejemplo de flujo completo:**
```python
# En app.py - Ruta de login
@app.route('/cuenta', methods=['GET', 'POST'])
def acceso_cuentas():
    if request.method == 'POST':
        service = UsuarioService()
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        usuario = service.login(email, contraseña)
        
        if usuario:
            # Guardar datos en sesión
            session['usuario_id'] = usuario['id']
            session['usuario_email'] = usuario['email']
            session['usuario_nombre'] = usuario['nombre']
            session['es_admin'] = usuario['is_admin']
            session.permanent = True
            return jsonify({"mensaje": "Login exitoso"}), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
```

### 3. CarritoService

**Ubicación**: `services/carrito_service.py`

**Responsabilidad**: Gestionar el carrito de compras en sesión.

**Importante**: El carrito se almacena en la **sesión de Flask**, no en base de datos.

```python
class CarritoService:
    def obtener_carrito(self):
        """Retorna: dict con {producto_id: cantidad}"""
        return session.get('carrito', {})
    
    def agregar_item(self, producto_id, cantidad=1):
        """Agrega un producto al carrito"""
        if 'carrito' not in session:
            session['carrito'] = {}
        
        carrito = session['carrito']
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            carrito[producto_id_str] += cantidad
        else:
            carrito[producto_id_str] = cantidad
        
        session.modified = True
```

**Estructura del carrito en sesión:**
```python
session['carrito'] = {
    '18': 2,   # TV Philips - 2 unidades
    '19': 1,   # Parlante Bluetooth - 1 unidad
    '20': 3    # Monitor Curvo - 3 unidades
}
```

### 4. PedidoService

**Ubicación**: `services/pedido_service.py`

**Responsabilidad**: Crear pedidos en la base de datos cuando se confirma una compra.

```python
def crear_pedido(self, usuario_id, email, total, items):
    cursor = self.conexion.cursor()
    
    # 1. Insertar pedido principal
    query_pedido = """
        INSERT INTO pedidos (usuario_id, email, total, estado)
        VALUES (%s, %s, %s, 'completado')
    """
    cursor.execute(query_pedido, (usuario_id, email, total))
    self.conexion.commit()
    
    pedido_id = cursor.lastrowid
    
    # 2. Insertar cada item del pedido
    for item in items:
        query_item = """
            INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_item, (
            pedido_id,
            item['producto_id'],
            item['cantidad'],
            item['precio'],
            item['subtotal']
        ))
    
    self.conexion.commit()
    return {"ok": True, "pedido_id": pedido_id}
```

### 5. AdminManager

**Ubicación**: `services/admin_manager.py`

**Responsabilidad**: Controlar permisos y proteger rutas administrativas.

#### Decoradores de seguridad:

```python
class AdminManager:
    def es_admin(self):
        """Verifica si el usuario actual es admin"""
        return session.get('es_admin') == 1
    
    def requerir_admin(self, f):
        """Decorador: Solo admin puede acceder"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.es_admin():
                return abort(403)  # Acceso denegado
            return f(*args, **kwargs)
        return decorated_function
```

**Uso en rutas protegidas:**
```python
admin_manager = AdminManager()

@app.route('/formulario')
@admin_manager.requerir_admin  # Solo admins pueden acceder
def carga_producto():
    return render_template('formulario_carga_producto.html')

@app.route('/eliminar_producto/<int:id_producto>')
@admin_manager.requerir_admin  # Solo admins pueden eliminar
def eliminar_producto(id_producto):
    service = ProductoService()
    service.eliminar_producto(id_producto)
    return redirect('/gestion_productos')
```

---

## Sistema de Autenticación

### Flujo de Registro

```
Usuario → Formulario de Registro → POST /cargar_usuario
                                         ↓
                                   UsuarioService.crear_usuario()
                                         ↓
                                   Encriptar contraseña (bcrypt)
                                         ↓
                                   INSERT INTO usuario
                                         ↓
                                   Respuesta JSON
```

**Código del formulario (f_nuevo_usuario.html):**
```html
<form id="formRegistro">
    <input type="text" name="nombre" required>
    <input type="text" name="apellido" required>
    <input type="email" name="email" required>
    <input type="password" name="contraseña" required>
    <button type="submit">Registrarse</button>
</form>
```

**JavaScript para envío:**
```javascript
document.getElementById('formRegistro').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const response = await fetch('/cargar_usuario', {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    if (response.ok) {
        alert('Cuenta creada exitosamente');
        window.location.href = '/acceso';
    } else {
        alert('Error: ' + data.error);
    }
});
```

### Flujo de Login

```
Usuario → Formulario de Login → POST /cuenta
                                      ↓
                                UsuarioService.login(email, password)
                                      ↓
                                Buscar usuario por email
                                      ↓
                                Verificar contraseña con bcrypt
                                      ↓
                                Crear sesión (session['usuario_id'], etc.)
                                      ↓
                                Respuesta JSON (éxito/error)
```

---

## Flujo de Usuario

### 1. Navegación y Búsqueda

#### Catálogo Principal
**Ruta**: `/` o `/<int:pagina>`

```python
@app.route('/')
@app.route('/<int:pagina>')
def mostrar_catalogo(pagina=1):
    service = ProductoService()
    productos = service.obtener_paginados(pagina, 9)  # 9 productos por página
    total_productos = len(service.obtener_todos())
    total_paginas = ceil(total_productos / 9)
    return render_template('index.html', 
                         productos=productos, 
                         pagina=pagina, 
                         total_paginas=total_paginas)
```

**Ejemplo**: Usuario accede a `http://127.0.0.1:5000/2`
- Muestra productos 10-18 (página 2)

#### Búsqueda de Productos
**Ruta**: `/buscar?q=termino`

```python
@app.route('/buscar')
def buscar_productos():
    termino = request.args.get('q', '').strip()
    
    if not termino:
        return redirect(url_for('mostrar_catalogo'))
    
    service = ProductoService()
    productos = service.buscar_productos(termino)
    
    return render_template('resultado_busqueda.html', 
                         productos=productos, 
                         termino=termino)
```

**Ejemplo**: Usuario busca "samsung"
- URL: `/buscar?q=samsung`
- Busca en: nombre, descripción y categoría
- Retorna: Smart TV Samsung, Aspiradora Robot Samsung, Barra de Sonido Samsung

#### Filtro por Categoría
**Ruta**: `/<categoria>`

```python
@app.route('/<categoria>')
def mostrar_catalogo_categoria(categoria):
    service = ProductoService()
    productos = service.filtrar_categoria(categoria)
    return render_template('categoria.html', 
                         productos=productos, 
                         categoria=categoria)
```

**Ejemplo**: Usuario accede a `/Electrodomésticos`
- Muestra todos los productos de categoría "Electrodomésticos"

### 2. Ver Detalle de Producto

**Ruta**: `/producto/<int:producto_id>`

```python
@app.route('/producto/<int:producto_id>')
def ver_producto(producto_id):
    service = ProductoService()
    producto = service.obtener_por_id(producto_id)
    
    if not producto:
        return abort(404)
    
    return render_template('producto_detalle.html', producto=producto)
```

**Ejemplo**: Usuario accede a `/producto/18`
- Muestra: Android TV Philips LED 4K 50" con descripción completa, precio, stock

---

## Flujo de Administrador

### Protección de Rutas

Todas las rutas administrativas están protegidas con el decorador `@admin_manager.requerir_admin`:

```python
@app.route('/formulario')
@admin_manager.requerir_admin  # ← Verificación de permisos
def carga_producto():
    return render_template('formulario_carga_producto.html')
```

Si un usuario sin permisos intenta acceder:
- HTTP 403 (Forbidden)

### 1. Crear Producto

**Flujo completo:**

```
Admin → GET /formulario → formulario_carga_producto.html
                               ↓
                          Completa formulario
                               ↓
                          POST /cargar_producto
                               ↓
                          Guardar imagen (werkzeug.secure_filename)
                               ↓
                          ProductoService.agregar_producto()
                               ↓
                          INSERT INTO producto
                               ↓
                          Respuesta JSON
```

**Código de la ruta:**
```python
@app.route('/cargar_producto', methods=['POST'])
@admin_manager.requerir_admin
def cargar_producto():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    categoria = request.form.get('categoria')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    foto = request.files.get('foto')
    
    # Guardar imagen de forma segura
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
        # Eliminar imagen si la inserción falló
        if ruta_imagen and os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
        return jsonify({"error": resultado.get("error")}), 500
```

### 2. Editar Producto

**Ruta**: GET `/editar_producto/<int:id_producto>` (formulario)
**Ruta**: POST `/actualizar_producto/<int:id_producto>` (actualización)

```python
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
    
    service.editar_producto(id_producto, nombre, descripcion, 
                          categoria, precio, cantidad, ruta)
    
    return redirect('/gestion_productos')
```

### 3. Eliminar Producto

```python
@app.route('/eliminar_producto/<int:id_producto>')
@admin_manager.requerir_admin
def eliminar_producto(id_producto):
    service = ProductoService()
    service.eliminar_producto(id_producto)
    return redirect('/gestion_productos')
```

**SQL ejecutado:**
```sql
DELETE FROM catalogo.producto WHERE id = 18;
```

### 4. Gestión de Productos

**Ruta**: `/gestion_productos`

Lista todos los productos con opciones de editar/eliminar:

```python
@app.route('/gestion_productos')
@admin_manager.requerir_admin
def gestion_productos():
    service = ProductoService()
    productos = service.obtener_todos()
    return render_template('gestion_productos.html', productos=productos)
```

---

## Sistema de Carrito de Compras

### Arquitectura del Carrito

El carrito se almacena en la **sesión de Flask** (en memoria, cookies cifradas):

```python
session['carrito'] = {
    '18': 2,    # producto_id: cantidad
    '19': 1,
    '20': 3
}
```

### 1. Agregar al Carrito

**Ruta**: POST `/agregar_carrito/<int:id_producto>`

```python
@app.route('/agregar_carrito/<int:id_producto>', methods=['POST'])
def agregar_carrito(id_producto):
    datos = request.get_json() or request.form
    cantidad = int(datos.get('cantidad', 1))
    
    # Validar que exista el producto
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    
    if not producto:
        return jsonify({"ok": False, "error": "Producto no existe"}), 404
    
    # Validar stock
    stock = producto[5]
    if stock <= 0:
        return jsonify({"ok": False, "error": "Producto agotado"}), 400
    
    # Agregar usando CarritoService
    carrito_service.agregar_item(id_producto, cantidad)
    
    return jsonify({"ok": True, "mensaje": "Producto agregado"}), 200
```

**Ejemplo de llamada desde JavaScript:**
```javascript
async function agregarAlCarrito(productoId) {
    const response = await fetch(`/agregar_carrito/${productoId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cantidad: 1 })
    });
    
    const data = await response.json();
    if (response.ok) {
        alert('Producto agregado al carrito');
    }
}
```

### 2. Ver Carrito

**Ruta**: GET `/carrito`

```python
@app.route('/carrito')
def ver_carrito():
    producto_service = ProductoService()
    
    # Obtener items con detalles completos
    items = carrito_service.obtener_items_detalle(producto_service)
    total = carrito_service.calcular_total(producto_service)
    
    return render_template('carrito.html', 
                         items=items, 
                         total=total, 
                         usuario_logueado=usuario_logueado())
```

**Lo que hace `obtener_items_detalle`:**
```python
def obtener_items_detalle(self, producto_service):
    carrito = self.obtener_carrito()  # {'18': 2, '19': 1}
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
```

**Ejemplo de resultado:**
```python
items = [
    {
        'id': 18,
        'nombre': 'Android TV Philips LED 4K 50" HDR+',
        'precio': 524699.00,
        'cantidad': 2,
        'subtotal': 1049398.00,
        'foto': 'static/uploads/55PUD7406-77.webp'
    },
    {
        'id': 19,
        'nombre': 'Parlante deportivo Bluetooth',
        'precio': 128959.00,
        'cantidad': 1,
        'subtotal': 128959.00,
        'foto': 'static/uploads/Parlante_deportivo_Bluetooth.webp'
    }
]
total = 1178357.00
```

### 3. Actualizar Cantidad

**Ruta**: POST `/actualizar_carrito/<int:id_producto>`

```python
@app.route('/actualizar_carrito/<int:id_producto>', methods=['POST'])
def actualizar_carrito(id_producto):
    datos = request.get_json() or request.form
    cantidad = int(datos.get('cantidad', 1))
    
    if cantidad <= 0:
        return jsonify({"ok": False, "error": "Cantidad inválida"}), 400
    
    # Validar stock
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    if not producto or cantidad > producto[5]:
        return jsonify({"ok": False, "error": "Stock insuficiente"}), 400
    
    if carrito_service.actualizar_cantidad(id_producto, cantidad):
        return jsonify({"ok": True}), 200
    else:
        return jsonify({"ok": False, "error": "Error al actualizar"}), 400
```

### 4. Procesar Compra

**Ruta**: POST `/procesar_compra`

**Flujo completo:**

```
Usuario → Confirma compra → POST /procesar_compra
                                  ↓
                            Obtener carrito de sesión
                                  ↓
                            Validar carrito no vacío
                                  ↓
                            Calcular total
                                  ↓
                            PedidoService.crear_pedido()
                                  ↓
                            Restar stock de productos
                                  ↓
                            Vaciar carrito
                                  ↓
                            Retornar pedido_id
```

**Código completo:**
```python
@app.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    carrito = carrito_service.obtener_carrito()
    
    if not carrito:
        return jsonify({"ok": False, "error": "Carrito vacío"}), 400
    
    try:
        service_producto = ProductoService()
        service_pedido = PedidoService()
        
        # Obtener items formateados para compra
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

**Ejemplo de items_compra:**
```python
items_compra = [
    {
        'producto_id': 18,
        'cantidad': 2,
        'precio': 524699.00,
        'subtotal': 1049398.00
    },
    {
        'producto_id': 19,
        'cantidad': 1,
        'precio': 128959.00,
        'subtotal': 128959.00
    }
]
```

---

## Manejo de Sesiones

Flask utiliza **cookies firmadas** para almacenar sesiones de forma segura.

### Configuración de Sesiones

```python
app.secret_key = '5x7#YI6+W<i{n^$V5y4ZHf7'  # Clave para firmar cookies

# Configuración de sesiones persistentes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False  # False en desarrollo
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No accesible desde JS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)
```

### Datos Almacenados en Sesión

```python
session = {
    'usuario_id': 14,                    # ID del usuario
    'usuario_email': 'juan@example.com', # Email
    'usuario_nombre': 'Juan',            # Nombre
    'es_admin': 0,                       # ¿Es administrador?
    'carrito': {                         # Carrito de compras
        '18': 2,
        '19': 1
    }
}
```

### Verificar Estado de Usuario

```python
def usuario_logueado():
    return 'usuario_id' in session

def es_admin_logueado():
    return session.get('es_admin') == 1
```

### Cerrar Sesión

```python
@app.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de sesión
    return redirect(url_for('mostrar_catalogo'))
```

---

## Ejemplos Prácticos

### Ejemplo 1: Usuario Registra y Compra

**Paso 1: Registro**
```
Usuario accede a: /nuevo_usuario
Completa formulario:
  - Nombre: María
  - Apellido: García
  - Email: maria@example.com
  - Contraseña: miPassword123

POST → /cargar_usuario
UsuarioService cifra contraseña: $2b$12$ibFZeOov2ZZZKtRkleQfJu...
INSERT INTO usuario...
Respuesta: {"mensaje": "Cuenta creada"}
```

**Paso 2: Login**
```
Usuario accede a: /cuenta
POST → email: maria@example.com, contraseña: miPassword123

UsuarioService.login():
  1. Busca usuario por email
  2. Verifica contraseña con bcrypt.checkpw()
  3. Retorna datos del usuario

session['usuario_id'] = 17
session['usuario_email'] = 'maria@example.com'
session['usuario_nombre'] = 'María'
session['es_admin'] = 0

Respuesta: {"mensaje": "Login exitoso"}
```

**Paso 3: Agregar al carrito**
```
Usuario ve producto ID 18 (TV Philips - $524,699)
Click en "Agregar al carrito"

JavaScript:
  fetch('/agregar_carrito/18', {
    method: 'POST',
    body: JSON.stringify({cantidad: 1})
  })

CarritoService.agregar_item(18, 1)
session['carrito'] = {'18': 1}

Respuesta: {"ok": true, "mensaje": "Producto agregado"}
```

**Paso 4: Ver carrito**
```
Usuario accede a: /carrito

CarritoService.obtener_items_detalle():
  1. Lee session['carrito'] = {'18': 1}
  2. Busca producto 18 en BD
  3. Calcula subtotal: 524699 * 1 = 524699

Renderiza carrito.html con:
  items = [{id: 18, nombre: 'TV Philips...', cantidad: 1, subtotal: 524699}]
  total = 524699
```

**Paso 5: Procesar compra**
```
Usuario click en "Confirmar compra"

POST → /procesar_compra

1. PedidoService.crear_pedido():
   INSERT INTO pedidos (usuario_id=17, email='maria@...', total=524699)
   pedido_id = 42

2. INSERT INTO pedido_items (pedido_id=42, producto_id=18, cantidad=1, ...)

3. ProductoService.restar_stock(18, 1):
   UPDATE producto SET cantidad = cantidad - 1 WHERE id = 18

4. CarritoService.vaciar_carrito():
   session['carrito'] = {}

Respuesta: {
  "ok": true,
  "pedido_id": 42,
  "total": 524699,
  "mensaje": "Compra realizada exitosamente"
}
```

### Ejemplo 2: Admin Agrega Producto

**Paso 1: Login como admin**
```
Usuario: admin@example.com
Contraseña: admin123

session['es_admin'] = 1
```

**Paso 2: Acceder a formulario**
```
Admin accede a: /formulario

AdminManager.requerir_admin() verifica:
  if session.get('es_admin') != 1:
    abort(403)  ← Rechaza usuarios normales

Renderiza: formulario_carga_producto.html
```

**Paso 3: Cargar producto**
```
Admin completa formulario:
  - Nombre: Notebook Lenovo IdeaPad 3
  - Descripción: Notebook con procesador Intel Core i5...
  - Categoría: Tecnología
  - Precio: 599999
  - Cantidad: 10
  - Foto: notebook-lenovo.jpg

POST → /cargar_producto

1. Guardar imagen:
   filename = secure_filename('notebook-lenovo.jpg')
   ruta = 'static/uploads/notebook-lenovo.jpg'
   foto.save(ruta)

2. ProductoService.agregar_producto():
   INSERT INTO producto (nombre, descripcion, categoria, precio, cantidad, foto)
   VALUES ('Notebook Lenovo IdeaPad 3', '...', 'Tecnología', 599999, 10, 'static/uploads/notebook-lenovo.jpg')

Respuesta: {"mensaje": "Producto cargado correctamente"}
```

### Ejemplo 3: Búsqueda de Productos

```
Usuario busca: "samsung"

GET → /buscar?q=samsung

ProductoService.buscar_productos('samsung'):
  SELECT * FROM producto
  WHERE nombre LIKE '%samsung%'
     OR descripcion LIKE '%samsung%'
     OR categoria LIKE '%samsung%'

Resultados encontrados:
  - Smart TV 65 Pulgadas 4K Samsung (id: 28)
  - Aspiradora Robot Samsung (id: 27)
  - Barra De Sonido Samsung (id: 30)

Renderiza: resultado_busqueda.html con 3 productos
```

---

## Conceptos Clave para el Examen

### 1. Arquitectura MVC
- **Modelo**: Services (ProductoService, UsuarioService) + MySQL
- **Vista**: Templates HTML (index.html, carrito.html, etc.)
- **Controlador**: app.py (rutas de Flask)

### 2. Seguridad
- **Contraseñas**: bcrypt (hash + salt)
- **Sesiones**: Cookies firmadas con secret_key
- **Upload de archivos**: secure_filename() para evitar inyección
- **SQL**: Consultas parametrizadas (%s) para evitar SQL injection
- **Autorización**: Decoradores (@admin_manager.requerir_admin)

### 3. Base de Datos
- **Relacional**: MySQL con tablas relacionadas
- **CRUD**: Create, Read, Update, Delete en ProductoService
- **Transacciones**: commit() después de INSERT/UPDATE/DELETE

### 4. Manejo de Estado
- **Sesiones**: Datos temporales del usuario (login, carrito)
- **Persistencia**: Base de datos para datos permanentes (usuarios, productos, pedidos)

### 5. Arquitectura de Servicios
- **Separación de responsabilidades**: Cada servicio gestiona una entidad
- **Reutilización**: Los servicios se pueden usar en múltiples rutas
- **Conexión a BD**: Cada servicio tiene su propia conexión

---

## Preguntas de Examen Frecuentes

### ¿Por qué usar servicios en lugar de poner todo en app.py?
**Respuesta**: 
- **Mantenibilidad**: Código organizado y fácil de encontrar
- **Reutilización**: Un servicio puede usarse en múltiples rutas
- **Testeo**: Más fácil probar lógica de negocio aislada
- **Escalabilidad**: Fácil agregar nuevas funcionalidades

**Ejemplo**: ProductoService.obtener_por_id() se usa en:
- `/producto/<id>` (ver detalle)
- `/agregar_carrito/<id>` (validar existencia)
- `/editar_producto/<id>` (obtener datos actuales)

### ¿Cómo funciona la autenticación?
**Respuesta**:
1. Usuario envía email + contraseña
2. UsuarioService busca usuario en BD
3. bcrypt.checkpw() compara contraseña con hash guardado
4. Si coincide: crea sesión con datos del usuario
5. Sesión persiste durante 7 días (configurable)
6. Cada request verifica session['usuario_id'] si necesita autenticación

### ¿Por qué el carrito está en sesión y no en BD?
**Respuesta**:
- **Velocidad**: No requiere consultas a BD en cada operación
- **Simplicidad**: No requiere tabla adicional ni relaciones
- **Anonimato**: Usuarios no logueados también pueden usar carrito
- **Temporal**: El carrito es un estado temporal, no un registro permanente

**Nota**: En producción real, se suele guardar en BD para:
- Recuperar carrito entre dispositivos
- Analítica de carritos abandonados
- Persistir si el usuario cierra el navegador

### ¿Cómo se protegen las rutas de admin?
**Respuesta**:
1. AdminManager.requerir_admin es un decorador
2. Se coloca antes de la función de ruta: `@admin_manager.requerir_admin`
3. Verifica `session.get('es_admin') == 1`
4. Si no es admin: `abort(403)` (HTTP Forbidden)
5. Si es admin: ejecuta la función normalmente

**Código**:
```python
@app.route('/eliminar_producto/<int:id>')
@admin_manager.requerir_admin  # ← Aquí se protege
def eliminar_producto(id):
    # Solo se ejecuta si es admin
    service = ProductoService()
    service.eliminar_producto(id)
    return redirect('/gestion_productos')
```

---

## Diagrama General del Sistema

```
                          ┌─────────────────┐
                          │   NAVEGADOR     │
                          │   (Usuario)     │
                          └────────┬────────┘
                                   │
                                   │ HTTP Request
                                   ▼
                          ┌─────────────────┐
                          │   FLASK APP     │
                          │   (app.py)      │
                          └────────┬────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
          ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
          │ ProductoSvc  │ │ UsuarioSvc   │ │ CarritoSvc   │
          └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                 │                │                │
                 │                │                │
                 ▼                ▼                ▼
          ┌────────────────────────────────────────────┐
          │            MySQL Database                  │
          │  ┌──────────┐  ┌──────────┐  ┌──────────┐│
          │  │ producto │  │ usuario  │  │ pedidos  ││
          │  └──────────┘  └──────────┘  └──────────┘│
          └────────────────────────────────────────────┘
```

---

## Conclusión

Este sistema Full Gaming es un **e-commerce completo** que implementa:

✅ **CRUD** de productos
✅ **Autenticación** segura con bcrypt
✅ **Autorización** por roles (admin/usuario)
✅ **Carrito de compras** en sesión
✅ **Procesamiento de pedidos** con manejo de stock
✅ **Búsqueda y filtrado** de productos
✅ **Paginación** de catálogo
✅ **Upload seguro** de imágenes
✅ **Arquitectura limpia** con servicios

**Tecnologías clave:**
- Flask (web framework)
- MySQL (base de datos relacional)
- bcrypt (encriptación)
- Jinja2 (templates)
- Bootstrap (UI)

**Patrones de diseño:**
- MVC (Modelo-Vista-Controlador)
- Service Layer (capa de servicios)
- Decorator (para autorización)

---

¡Buena suerte en tu examen! 🚀
