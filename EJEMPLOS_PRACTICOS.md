# 💡 EJEMPLOS PRÁCTICOS DEL SISTEMA FULL GAMING

## Índice
1. [Ejemplos de Código Comentado](#ejemplos-de-código-comentado)
2. [Casos de Uso Reales](#casos-de-uso-reales)
3. [Debugging y Troubleshooting](#debugging-y-troubleshooting)
4. [Consultas SQL Generadas](#consultas-sql-generadas)
5. [Interacción Frontend-Backend](#interacción-frontend-backend)

---

## Ejemplos de Código Comentado

### Ejemplo 1: Crear Usuario con Validación

```python
# En services/usuario_service.py
def crear_usuario(self, nombre, apellido, email, contraseña):
    """
    Crea un nuevo usuario en la base de datos.
    
    Args:
        nombre: Nombre del usuario (ej: "Juan")
        apellido: Apellido del usuario (ej: "Pérez")
        email: Email único (ej: "juan@example.com")
        contraseña: Contraseña en texto plano (ej: "miPassword123")
    
    Returns:
        {"ok": True} si el usuario se creó exitosamente
        {"ok": False, "error": "mensaje"} si hubo un error
    """
    
    # PASO 1: Cifrar la contraseña ANTES de guardarla
    # bcrypt.gensalt() genera un "salt" aleatorio único para este usuario
    # bcrypt.hashpw() combina contraseña + salt → hash irreversible
    hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    
    # Ejemplo de resultado:
    # contraseña: "miPassword123"
    # hashed: b'$2b$12$VBLLKIlD4P4aLZn3Po18n.3zq.rYAF6qoh3ZGC/6gT2MMIYruGTdG'
    
    try:
        # PASO 2: Preparar consulta SQL
        cursor = self.conexion.cursor()
        query = """
            INSERT INTO usuario (nombre, apellido, email, contraseña)
            VALUES (%s, %s, %s, %s)
        """
        
        # PASO 3: Ejecutar consulta con parámetros
        # %s son placeholders que MySQL reemplaza de forma segura
        # Esto previene SQL injection
        cursor.execute(query, (nombre, apellido, email, hashed))
        
        # PASO 4: Confirmar transacción
        # Sin commit(), los cambios no se guardan permanentemente
        self.conexion.commit()
        cursor.close()
        
        return {"ok": True}
        
    except mysql.connector.Error as error:
        # Si el email ya existe (UNIQUE constraint), captura el error
        # Ejemplo de error: "Duplicate entry 'juan@example.com' for key 'email_UNIQUE'"
        return {"ok": False, "error": str(error)}
```

**Ejemplo de uso desde app.py:**
```python
@app.route('/cargar_usuario', methods=['POST'])
def cargar_usuario():
    # PASO 1: Obtener datos del formulario
    service = UsuarioService()
    datos = request.form
    
    # datos['nombre'] = "Juan"
    # datos['apellido'] = "Pérez"
    # datos['email'] = "juan@example.com"
    # datos['contraseña'] = "miPassword123"
    
    # PASO 2: Llamar al servicio
    resultado = service.crear_usuario(
        nombre=datos['nombre'],
        apellido=datos['apellido'],
        email=datos['email'],
        contraseña=datos['contraseña']
    )
    
    # PASO 3: Responder según el resultado
    if resultado["ok"]:
        return jsonify({"mensaje": "Cuenta creada"}), 200
    else:
        # Si el email ya existe, retorna el error
        return jsonify({"error": resultado["error"]}), 400
```

### Ejemplo 2: Login con Verificación de Contraseña

```python
# En services/usuario_service.py
def login(self, email, contraseña):
    """
    Verifica las credenciales del usuario.
    
    Args:
        email: Email del usuario
        contraseña: Contraseña en texto plano
    
    Returns:
        Usuario (dict) si las credenciales son correctas
        None si las credenciales son incorrectas
    """
    
    # PASO 1: Buscar usuario por email
    usuario = self.buscar_usuario(email)
    
    if not usuario:
        # Usuario no existe
        return None
    
    # PASO 2: Obtener el hash guardado
    hash_guardado = usuario["contraseña"]
    # Ejemplo: b'$2b$12$VBLLKIlD4P4aLZn3Po18n.3zq.rYAF6qoh3ZGC/6gT2MMIYruGTdG'
    
    # PASO 3: Asegurar que es bytes (por compatibilidad)
    if isinstance(hash_guardado, str):
        hash_guardado = hash_guardado.encode('utf-8')
    
    try:
        # PASO 4: Verificar contraseña SIN desencriptarla
        # bcrypt.checkpw() aplica el mismo proceso de hash y compara
        resultado = bcrypt.checkpw(contraseña.encode('utf-8'), hash_guardado)
        
        if resultado:
            # Contraseña correcta
            return usuario
        else:
            # Contraseña incorrecta
            return None
            
    except Exception as e:
        # Error en la verificación (hash corrupto o inválido)
        print(f"Error en bcrypt.checkpw: {e}")
        return None
```

**¿Cómo funciona bcrypt.checkpw()?**
```
Usuario ingresa: "miPassword123"

1. bcrypt extrae el salt del hash guardado
   Hash: $2b$12$VBLLKIlD4P4aLZn3Po18n...
         ↑    ↑   ↑
         tipo cost salt

2. Aplica el mismo proceso de hash a la contraseña ingresada con ese salt

3. Compara el resultado con el hash guardado
   Si coinciden → True (contraseña correcta)
   Si no → False (contraseña incorrecta)
```

### Ejemplo 3: Agregar Producto al Carrito con Validaciones

```python
# En app.py
@app.route('/agregar_carrito/<int:id_producto>', methods=['POST'])
def agregar_carrito(id_producto):
    """
    Agrega un producto al carrito de la sesión.
    
    Args:
        id_producto: ID del producto a agregar (de la URL)
    
    Request body:
        {"cantidad": 2}  (JSON) o cantidad=2 (FormData)
    """
    
    # PASO 1: Obtener cantidad del request
    datos = request.get_json() or request.form
    cantidad = int(datos.get('cantidad', 1))
    
    # Ejemplo: cantidad = 2
    
    # PASO 2: Validar que el producto existe
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    
    if not producto:
        # Producto no encontrado
        return jsonify({"ok": False, "error": "Producto no existe"}), 404
    
    # producto = (18, 'TV Philips', 'Descripción...', 'TV_Video', 524699.00, 9, 'ruta/imagen.jpg')
    #             ↑   ↑            ↑                  ↑           ↑          ↑  ↑
    #             id  nombre       descripcion        categoria   precio    qty foto
    
    # PASO 3: Validar stock disponible
    stock = producto[5]  # Índice 5 = cantidad en stock
    
    if stock <= 0:
        return jsonify({"ok": False, "error": "Producto agotado"}), 400
    
    # PASO 4: Agregar al carrito (en sesión)
    carrito_service.agregar_item(id_producto, cantidad)
    
    # Internamente hace:
    # session['carrito']['18'] = 2
    # o si ya existía:
    # session['carrito']['18'] += 2
    
    return jsonify({"ok": True, "mensaje": "Producto agregado"}), 200
```

**Lo que pasa en CarritoService.agregar_item():**
```python
def agregar_item(self, producto_id, cantidad=1):
    # PASO 1: Verificar si existe carrito en sesión
    if 'carrito' not in session:
        session['carrito'] = {}  # Crear carrito vacío
    
    carrito = session['carrito']
    # Ejemplo antes de agregar: {'19': 1, '20': 3}
    
    # PASO 2: Convertir ID a string (las claves de dict deben ser strings en JSON)
    producto_id_str = str(producto_id)  # 18 → '18'
    
    # PASO 3: Agregar o sumar cantidad
    if producto_id_str in carrito:
        # Ya existe, sumar cantidad
        carrito[producto_id_str] += cantidad
        # {'18': 1} + cantidad 2 = {'18': 3}
    else:
        # No existe, agregar nuevo
        carrito[producto_id_str] = cantidad
        # {'18': 2}
    
    # Resultado: {'19': 1, '20': 3, '18': 2}
    
    # PASO 4: Marcar sesión como modificada para que Flask la guarde
    session.modified = True
```

### Ejemplo 4: Procesar Compra Completa

```python
@app.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    """
    Convierte el carrito en un pedido persistente.
    
    Operaciones:
    1. Crear pedido en tabla 'pedidos'
    2. Crear items en tabla 'pedido_items'
    3. Restar stock de productos
    4. Vaciar carrito
    """
    
    # PASO 1: Obtener carrito actual
    carrito = carrito_service.obtener_carrito()
    # Ejemplo: {'18': 2, '19': 1}
    
    if not carrito:
        return jsonify({"ok": False, "error": "Carrito vacío"}), 400
    
    try:
        # PASO 2: Inicializar servicios
        service_producto = ProductoService()
        service_pedido = PedidoService()
        
        # PASO 3: Preparar datos de compra
        items_compra = carrito_service.obtener_items_para_compra(service_producto)
        # items_compra = [
        #     {'producto_id': 18, 'cantidad': 2, 'precio': 524699.00, 'subtotal': 1049398.00},
        #     {'producto_id': 19, 'cantidad': 1, 'precio': 128959.00, 'subtotal': 128959.00}
        # ]
        
        total = carrito_service.calcular_total(service_producto)
        # total = 1178357.00
        
        # PASO 4: Obtener datos del usuario
        usuario_id = session.get('usuario_id')  # Puede ser None si no está logueado
        email = session.get('usuario_email', 'anonimo@email.com')
        
        # PASO 5: Crear pedido en base de datos
        resultado = service_pedido.crear_pedido(usuario_id, email, total, items_compra)
        
        if not resultado['ok']:
            return jsonify({"ok": False, "error": resultado['error']}), 500
        
        pedido_id = resultado['pedido_id']
        # Ejemplo: pedido_id = 42
        
        # PASO 6: Restar stock de cada producto
        for item in items_compra:
            service_producto.restar_stock(item['producto_id'], item['cantidad'])
            # UPDATE producto SET cantidad = cantidad - 2 WHERE id = 18
            # UPDATE producto SET cantidad = cantidad - 1 WHERE id = 19
        
        # PASO 7: Vaciar carrito
        carrito_service.vaciar_carrito()
        # session['carrito'] = {}
        
        # PASO 8: Retornar respuesta exitosa
        return jsonify({
            "ok": True,
            "pedido_id": pedido_id,
            "total": total,
            "mensaje": "Compra realizada exitosamente"
        }), 200
        
    except Exception as e:
        # Manejo de errores
        return jsonify({"ok": False, "error": str(e)}), 500
```

**Lo que hace PedidoService.crear_pedido():**
```python
def crear_pedido(self, usuario_id, email, total, items):
    cursor = None
    try:
        cursor = self.conexion.cursor()
        
        # PASO 1: Insertar pedido principal
        query_pedido = """
            INSERT INTO pedidos (usuario_id, email, total, estado)
            VALUES (%s, %s, %s, 'completado')
        """
        cursor.execute(query_pedido, (usuario_id, email, total))
        # INSERT INTO pedidos (usuario_id, email, total, estado)
        # VALUES (14, 'juan@example.com', 1178357.00, 'completado')
        
        self.conexion.commit()
        
        # PASO 2: Obtener ID del pedido recién creado
        pedido_id = cursor.lastrowid
        # Ejemplo: 42
        
        # PASO 3: Insertar cada item del pedido
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
            # INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio, subtotal)
            # VALUES (42, 18, 2, 524699.00, 1049398.00)
            # 
            # INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio, subtotal)
            # VALUES (42, 19, 1, 128959.00, 128959.00)
        
        self.conexion.commit()
        cursor.close()
        
        return {"ok": True, "pedido_id": pedido_id}
        
    except Exception as e:
        if cursor:
            cursor.close()
        return {"ok": False, "error": str(e)}
```

---

## Casos de Uso Reales

### Caso 1: María Compra una Laptop

**CONTEXTO**: María necesita una laptop para trabajar desde casa.

**FLUJO DETALLADO:**

```
1. María abre el sitio: http://127.0.0.1:5000
   └─ Ejecuta: mostrar_catalogo(pagina=1)
   └─ SQL: SELECT * FROM producto LIMIT 0, 9
   └─ Muestra primeros 9 productos

2. María busca "laptop"
   └─ URL: /buscar?q=laptop
   └─ Ejecuta: buscar_productos("laptop")
   └─ SQL: SELECT * FROM producto 
           WHERE nombre LIKE '%laptop%' 
              OR descripcion LIKE '%laptop%' 
              OR categoria LIKE '%laptop%'
   └─ Encuentra: 0 resultados (no hay laptops en el catálogo actual)

3. María busca "notebook" en su lugar
   └─ Encuentra: Notebook Lenovo IdeaPad 3 (ID: 47)
   └─ Precio: $599,999
   └─ Stock: 10 unidades

4. María ve el detalle
   └─ URL: /producto/47
   └─ SQL: SELECT * FROM producto WHERE id = 47
   └─ Muestra especificaciones completas

5. María decide comprar, agrega al carrito
   └─ Click en "Agregar al carrito"
   └─ JavaScript: fetch('/agregar_carrito/47', {method: 'POST', body: {cantidad: 1}})
   └─ Ejecuta: agregar_carrito(47)
   └─ session['carrito'] = {'47': 1}
   └─ Alert: "Producto agregado"

6. María ve su carrito
   └─ URL: /carrito
   └─ obtener_items_detalle() busca detalles del producto 47
   └─ Muestra:
       Notebook Lenovo IdeaPad 3
       Cantidad: 1
       Precio: $599,999
       Total: $599,999

7. María quiere comprar pero no tiene cuenta
   └─ Click en "Confirmar compra"
   └─ Sistema detecta que no está logueada
   └─ Redirige a: /acceso

8. María se registra
   └─ Click en "Crear cuenta"
   └─ URL: /nuevo_usuario
   └─ Completa formulario:
       Nombre: María
       Apellido: García
       Email: maria.garcia@gmail.com
       Contraseña: MiPassword2024!
   └─ POST /cargar_usuario
   └─ UsuarioService.crear_usuario()
   └─ bcrypt cifra: MiPassword2024! → $2b$12$...
   └─ SQL: INSERT INTO usuario (nombre, apellido, email, contraseña)
           VALUES ('María', 'García', 'maria.garcia@gmail.com', '$2b$12$...')
   └─ Respuesta: "Cuenta creada"

9. María se loguea
   └─ POST /cuenta
   └─ Email: maria.garcia@gmail.com
   └─ Contraseña: MiPassword2024!
   └─ UsuarioService.login()
   └─ bcrypt.checkpw() → True
   └─ session['usuario_id'] = 21
   └─ session['usuario_email'] = 'maria.garcia@gmail.com'
   └─ session['usuario_nombre'] = 'María'

10. María confirma la compra
    └─ POST /procesar_compra
    └─ PedidoService.crear_pedido()
    └─ SQL: INSERT INTO pedidos (usuario_id=21, email='maria.garcia@...', total=599999)
    └─ pedido_id = 51
    └─ SQL: INSERT INTO pedido_items (pedido_id=51, producto_id=47, cantidad=1, precio=599999, subtotal=599999)
    └─ ProductoService.restar_stock(47, 1)
    └─ SQL: UPDATE producto SET cantidad = cantidad - 1 WHERE id = 47
    └─ Stock: 10 → 9
    └─ CarritoService.vaciar_carrito()
    └─ session['carrito'] = {}
    └─ Respuesta: {
          "ok": true,
          "pedido_id": 51,
          "total": 599999,
          "mensaje": "Compra realizada exitosamente"
        }

RESULTADO:
✅ María tiene su cuenta registrada
✅ Pedido #51 creado
✅ Stock actualizado (Notebook: 9 unidades disponibles)
✅ María recibe confirmación de compra
```

### Caso 2: Administrador Agrega Nuevo Producto

**CONTEXTO**: El administrador recibe un nuevo producto y debe agregarlo al catálogo.

```
1. Admin se loguea
   └─ Email: admin@fullgaming.com
   └─ Contraseña: Admin123!
   └─ session['es_admin'] = 1

2. Admin accede a panel de gestión
   └─ URL: /gestion_productos
   └─ @admin_manager.requerir_admin verifica sesión
   └─ Lista todos los productos con opciones Editar/Eliminar

3. Admin click en "Agregar Producto"
   └─ URL: /formulario
   └─ Muestra formulario de carga

4. Admin completa formulario
   Datos del nuevo producto:
   ├─ Nombre: Teclado Mecánico Redragon K552
   ├─ Descripción: Teclado mecánico RGB, switches Outemu Blue, 87 teclas
   ├─ Categoría: Tecnología
   ├─ Precio: 45999
   ├─ Cantidad: 25
   └─ Foto: teclado-redragon.jpg (archivo)

5. Admin envía formulario
   └─ POST /cargar_producto
   └─ secure_filename('teclado-redragon.jpg')
   └─ Valida que el nombre sea seguro (sin ../ ni caracteres especiales)
   └─ Guarda en: static/uploads/teclado-redragon.jpg

6. Sistema inserta en BD
   └─ ProductoService.agregar_producto()
   └─ SQL: INSERT INTO producto 
           (nombre, descripcion, categoria, precio, cantidad, foto)
           VALUES 
           ('Teclado Mecánico Redragon K552', 
            'Teclado mecánico RGB...', 
            'Tecnología', 
            45999, 
            25, 
            'static/uploads/teclado-redragon.jpg')
   └─ Producto ID: 48

7. Sistema responde
   └─ {"mensaje": "Producto cargado correctamente"}
   └─ Admin ve confirmación en pantalla

8. Producto visible en catálogo
   └─ Cualquier usuario puede ahora:
       - Ver el teclado en la página principal
       - Buscarlo por "teclado" o "redragon"
       - Agregarlo al carrito
       - Comprarlo

RESULTADO:
✅ Nuevo producto en catálogo (ID: 48)
✅ Imagen guardada en servidor
✅ Disponible para compra inmediatamente
```

### Caso 3: Usuario Actualiza Cantidad en Carrito

**CONTEXTO**: Juan agregó 1 TV pero quiere comprar 2.

```
1. Estado inicial del carrito de Juan
   └─ session['carrito'] = {'28': 1}  # Smart TV Samsung

2. Juan ve su carrito
   └─ URL: /carrito
   └─ Muestra: Smart TV 65" - Cantidad: 1 - Total: $1,099,999

3. Juan cambia cantidad a 2
   └─ Input type="number" value cambia de 1 a 2
   └─ JavaScript detecta cambio (onChange)
   └─ fetch('/actualizar_carrito/28', {
        method: 'POST',
        body: JSON.stringify({cantidad: 2})
      })

4. Servidor valida stock
   └─ ProductoService.obtener_por_id(28)
   └─ SQL: SELECT * FROM producto WHERE id = 28
   └─ producto = (..., cantidad=2, ...)  # Hay 2 en stock
   └─ Validación: cantidad solicitada (2) <= stock (2) ✓

5. Servidor actualiza carrito
   └─ CarritoService.actualizar_cantidad(28, 2)
   └─ session['carrito']['28'] = 2
   └─ session.modified = True

6. Respuesta al cliente
   └─ {"ok": true}
   └─ JavaScript actualiza la página
   └─ Nuevo total: $2,199,998 (1,099,999 × 2)

RESULTADO:
✅ Carrito actualizado
✅ Total recalculado
✅ Validación de stock OK
```

---

## Debugging y Troubleshooting

### Caso 1: "Error al agregar producto - Stock insuficiente"

**SÍNTOMA**: Usuario intenta agregar 5 unidades pero solo hay 2.

**DEBUG PASO A PASO:**

```python
# En agregar_carrito()
producto = service.obtener_por_id(18)
stock = producto[5]  # 2

cantidad_solicitada = 5

if stock <= 0:  # 2 <= 0? No
    # No entra aquí
    
# Continúa...
carrito_service.agregar_item(18, 5)
# session['carrito']['18'] = 5

# Al intentar comprar:
# actualizar_carrito valida:
if cantidad > producto[5]:  # 5 > 2? Sí
    return jsonify({"ok": False, "error": "Stock insuficiente"}), 400
```

**SOLUCIÓN**: El usuario debe reducir la cantidad o esperar a que haya más stock.

### Caso 2: "Contraseña incorrecta" cuando debería ser correcta

**SÍNTOMA**: Usuario jura que la contraseña es correcta pero no puede entrar.

**DEBUG:**

```python
# En UsuarioService.login()
print(f"Email ingresado: {email}")
# Email ingresado: juan@example.com

usuario = self.buscar_usuario(email)
print(f"Usuario encontrado: {usuario is not None}")
# Usuario encontrado: True

hash_guardado = usuario["contraseña"]
print(f"Tipo de hash: {type(hash_guardado)}")
# Tipo de hash: <class 'str'>  ← PROBLEMA: Debería ser bytes

print(f"Hash: {hash_guardado}")
# Hash: $2b$12$VBLLKIlD4P4aLZn3Po18n...

# Convertir a bytes
if isinstance(hash_guardado, str):
    hash_guardado = hash_guardado.encode('utf-8')

print(f"Contraseña ingresada: {contraseña}")
# Contraseña ingresada: miPassword123

resultado = bcrypt.checkpw(contraseña.encode('utf-8'), hash_guardado)
print(f"Resultado: {resultado}")
# Resultado: False ← Contraseña incorrecta

# CAUSA POSIBLE:
# - Contraseña tiene espacios al inicio/final
# - Usuario escribió con Caps Lock
# - Hash corrupto en base de datos
```

**SOLUCIÓN**: 
- Verificar que no hay espacios: `contraseña.strip()`
- Usar "Olvidé mi contraseña" para resetear
- Verificar hash en BD directamente

### Caso 3: Carrito se vacía inesperadamente

**SÍNTOMA**: Usuario agrega productos al carrito pero al volver, está vacío.

**DEBUG:**

```python
# Verificar configuración de sesiones
print(f"Secret key configurada: {bool(app.secret_key)}")
# True

print(f"SESSION_PERMANENT: {session.permanent}")
# False ← PROBLEMA: Sesión no es permanente

print(f"SESSION_COOKIE_SECURE: {app.config['SESSION_COOKIE_SECURE']}")
# True ← PROBLEMA en desarrollo: Requiere HTTPS

# Verificar datos en sesión
print(f"Carrito en sesión: {session.get('carrito')}")
# {} ← Vacío después de cerrar navegador
```

**SOLUCIÓN:**
```python
# En app.py, asegurar que:
@app.before_request
def make_session_permanent():
    session.permanent = True  # ← Sesión persiste
    
app.config['SESSION_COOKIE_SECURE'] = False  # En desarrollo
```

---

## Consultas SQL Generadas

### Todas las consultas que genera el sistema

#### 1. PRODUCTOS

```sql
-- Obtener todos los productos
SELECT * FROM catalogo.producto;

-- Obtener productos paginados (página 2, 9 por página)
SELECT * FROM catalogo.producto LIMIT 9, 9;

-- Buscar productos
SELECT * FROM catalogo.producto 
WHERE nombre LIKE '%samsung%' 
   OR descripcion LIKE '%samsung%' 
   OR categoria LIKE '%samsung%';

-- Filtrar por categoría
SELECT * FROM catalogo.producto 
WHERE categoria = 'Electrodomésticos';

-- Obtener producto por ID
SELECT * FROM catalogo.producto WHERE id = 18;

-- Agregar producto
INSERT INTO catalogo.producto (nombre, descripcion, categoria, precio, cantidad, foto)
VALUES ('TV Philips', 'Descripción...', 'TV_Video', 524699, 10, 'static/uploads/tv.jpg');

-- Editar producto
UPDATE catalogo.producto
SET nombre='TV Philips 4K', descripcion='Nueva desc...', categoria='TV_Video', 
    precio=499999, cantidad=15, foto='static/uploads/tv-new.jpg'
WHERE id=18;

-- Eliminar producto
DELETE FROM catalogo.producto WHERE id = 18;

-- Restar stock (al comprar)
UPDATE catalogo.producto
SET cantidad = cantidad - 2
WHERE id = 18 AND cantidad >= 2;
```

#### 2. USUARIOS

```sql
-- Crear usuario
INSERT INTO usuario (nombre, apellido, email, contraseña)
VALUES ('Juan', 'Pérez', 'juan@example.com', '$2b$12$VBLLKIlD4P4aLZn3Po18n...');

-- Buscar usuario por email
SELECT * FROM usuario WHERE email = 'juan@example.com';

-- Actualizar admin flag
UPDATE usuario SET is_admin = 1 WHERE email = 'admin@example.com';
```

#### 3. PEDIDOS

```sql
-- Crear pedido
INSERT INTO pedidos (usuario_id, email, total, estado)
VALUES (14, 'juan@example.com', 1178357.00, 'completado');

-- Crear items del pedido
INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio, subtotal)
VALUES (42, 18, 2, 524699.00, 1049398.00);

INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio, subtotal)
VALUES (42, 19, 1, 128959.00, 128959.00);

-- Obtener pedidos de un usuario
SELECT * FROM pedidos WHERE usuario_id = 14 ORDER BY fecha DESC;

-- Obtener detalle de un pedido
SELECT pi.*, p.nombre, p.foto
FROM pedido_items pi
JOIN producto p ON pi.producto_id = p.id
WHERE pi.pedido_id = 42;
```

---

## Interacción Frontend-Backend

### Ejemplo: Agregar al Carrito con AJAX

**HTML (producto_detalle.html):**
```html
<div class="producto">
    <h2>TV Philips 50" 4K</h2>
    <p>Precio: $524,699</p>
    <input type="number" id="cantidad" value="1" min="1" max="10">
    <button onclick="agregarAlCarrito(18)">Agregar al Carrito</button>
</div>
```

**JavaScript:**
```javascript
async function agregarAlCarrito(productoId) {
    // PASO 1: Obtener cantidad del input
    const cantidad = document.getElementById('cantidad').value;
    
    // PASO 2: Preparar datos
    const datos = {
        cantidad: parseInt(cantidad)
    };
    
    try {
        // PASO 3: Enviar request al backend
        const response = await fetch(`/agregar_carrito/${productoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });
        
        // PASO 4: Parsear respuesta
        const resultado = await response.json();
        
        // PASO 5: Mostrar resultado al usuario
        if (response.ok) {
            // Éxito (HTTP 200)
            alert(resultado.mensaje);  // "Producto agregado"
            
            // Opcional: Actualizar contador del carrito en navbar
            actualizarContadorCarrito();
        } else {
            // Error (HTTP 400, 404, etc.)
            alert('Error: ' + resultado.error);
        }
        
    } catch (error) {
        // Error de red o servidor no responde
        console.error('Error:', error);
        alert('Error al conectar con el servidor');
    }
}

function actualizarContadorCarrito() {
    // Obtener cantidad de items en carrito via AJAX
    fetch('/api/carrito/count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('carrito-badge').textContent = data.count;
        });
}
```

**Backend (app.py):**
```python
@app.route('/agregar_carrito/<int:id_producto>', methods=['POST'])
def agregar_carrito(id_producto):
    # PASO 1: Recibir datos del request
    datos = request.get_json()  # {'cantidad': 2}
    cantidad = int(datos.get('cantidad', 1))
    
    # PASO 2: Validar producto
    service = ProductoService()
    producto = service.obtener_por_id(id_producto)
    
    if not producto:
        # HTTP 404
        return jsonify({"ok": False, "error": "Producto no existe"}), 404
    
    stock = producto[5]
    if stock <= 0:
        # HTTP 400
        return jsonify({"ok": False, "error": "Producto agotado"}), 400
    
    # PASO 3: Agregar al carrito
    carrito_service.agregar_item(id_producto, cantidad)
    
    # PASO 4: Responder con JSON
    # HTTP 200
    return jsonify({
        "ok": True, 
        "mensaje": "Producto agregado"
    }), 200
```

**Flujo completo:**
```
Usuario click → JavaScript → fetch() → Flask → Service → Sesión
                                                   ↓
Usuario ← alert() ← Promise ← JSON Response ← Flask
```

---

## Tabla de Códigos HTTP Usados

| Código | Significado | Usado en |
|--------|-------------|----------|
| 200 | OK | Operación exitosa |
| 400 | Bad Request | Datos inválidos (stock insuficiente, cantidad negativa) |
| 401 | Unauthorized | Credenciales incorrectas (login fallido) |
| 403 | Forbidden | No tiene permisos (usuario normal intenta acceder a admin) |
| 404 | Not Found | Recurso no existe (producto no encontrado) |
| 500 | Internal Server Error | Error en el servidor (error de BD, excepción) |

---

Esta documentación cubre todos los aspectos prácticos del sistema. ¡Úsala para entender cada flujo en detalle! 🚀
