# 🎯 GUÍA RÁPIDA PARA EL EXAMEN

## Respuestas Rápidas a Preguntas Comunes

### 1. ¿Qué hace este sistema?
Full Gaming es un **e-commerce** (tienda online) para vender hardware y software de computación. Permite:
- **Usuarios**: Navegar productos, buscar, agregar al carrito, comprar
- **Administradores**: Gestionar productos (crear, editar, eliminar)

### 2. ¿Qué tecnologías usa?
- **Python + Flask**: Backend (servidor web)
- **MySQL**: Base de datos
- **HTML + Bootstrap**: Frontend (interfaz)
- **bcrypt**: Encriptación de contraseñas
- **JavaScript**: Interactividad

### 3. ¿Cómo está organizado el código?

```
app.py              → Controlador (rutas HTTP)
services/           → Lógica de negocio
  ├── producto_service.py    → Maneja productos
  ├── usuario_service.py     → Maneja usuarios y login
  ├── carrito_service.py     → Maneja carrito
  ├── pedido_service.py      → Maneja compras
  └── admin_manager.py       → Controla permisos
templates/          → Vistas HTML
static/             → Imágenes, CSS, JS
```

### 4. ¿Cómo funciona el login?

```
1. Usuario ingresa email + contraseña
2. UsuarioService busca el usuario en MySQL
3. bcrypt compara la contraseña ingresada con el hash guardado
4. Si coincide: crea sesión con los datos del usuario
5. Si no coincide: error "Credenciales incorrectas"
```

**Código simplificado:**
```python
def login(self, email, contraseña):
    usuario = self.buscar_usuario(email)
    if bcrypt.checkpw(contraseña, usuario['contraseña']):
        return usuario  # Login exitoso
    return None  # Login fallido
```

### 5. ¿Cómo se protegen las contraseñas?

Con **bcrypt**:
1. Al registrarse: `bcrypt.hashpw(contraseña, salt)` → Genera hash único
2. Se guarda el hash, NUNCA la contraseña real
3. Al login: `bcrypt.checkpw(contraseña, hash)` → Verifica sin desencriptar

**Ejemplo:**
```
Contraseña ingresada: "miPassword123"
Hash guardado: "$2b$12$VBLLKIlD4P4aLZn3Po18n.3zq.rYAF6qoh3ZGC/6gT2MMIYruGTdG"
```

### 6. ¿Qué es una sesión?

Una **sesión** guarda datos temporales del usuario en una cookie cifrada:

```python
session = {
    'usuario_id': 14,
    'usuario_email': 'juan@example.com',
    'es_admin': 0,
    'carrito': {'18': 2, '19': 1}
}
```

**Características:**
- Persiste durante 7 días
- Se borra al hacer logout
- Está cifrada (no se puede leer desde el navegador)

### 7. ¿Cómo funciona el carrito?

El carrito se guarda en la **sesión** (no en base de datos):

```python
# Estructura del carrito
session['carrito'] = {
    '18': 2,  # producto_id: cantidad
    '19': 1
}

# Agregar producto
def agregar_item(self, producto_id, cantidad):
    if producto_id in carrito:
        carrito[producto_id] += cantidad  # Suma a existente
    else:
        carrito[producto_id] = cantidad   # Nuevo item
```

**Ventajas:**
- Rápido (no requiere base de datos)
- Funciona sin login
- Temporal (para un estado transitorio)

### 8. ¿Cómo se procesa una compra?

**5 pasos:**

```
1. Obtener carrito de sesión
2. Crear registro en tabla "pedidos"
3. Crear registros en tabla "pedido_items" (detalle)
4. Restar stock de cada producto
5. Vaciar carrito
```

**Ejemplo con datos reales:**
```
Carrito: {'18': 2, '19': 1}

→ INSERT INTO pedidos (usuario_id=14, total=1178357)
→ INSERT INTO pedido_items (pedido_id=42, producto_id=18, cantidad=2, ...)
→ INSERT INTO pedido_items (pedido_id=42, producto_id=19, cantidad=1, ...)
→ UPDATE producto SET cantidad=cantidad-2 WHERE id=18
→ UPDATE producto SET cantidad=cantidad-1 WHERE id=19
→ session['carrito'] = {}
```

### 9. ¿Cómo funcionan los servicios?

Los **servicios** separan la lógica de negocio de las rutas:

```python
# ❌ SIN servicios (todo en app.py)
@app.route('/productos')
def listar_productos():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    cursor.close()
    return render_template('productos.html', productos=productos)

# ✅ CON servicios (mejor organización)
@app.route('/productos')
def listar_productos():
    service = ProductoService()
    productos = service.obtener_todos()  # Lógica en el servicio
    return render_template('productos.html', productos=productos)
```

**Beneficios:**
- Código más limpio
- Reutilizable
- Fácil de testear
- Fácil de mantener

### 10. ¿Cómo se protegen las rutas de admin?

Con un **decorador** que verifica permisos:

```python
@app.route('/eliminar_producto/<int:id>')
@admin_manager.requerir_admin  # ← Verifica si es admin
def eliminar_producto(id):
    # Solo ejecuta si session['es_admin'] == 1
    service = ProductoService()
    service.eliminar_producto(id)
    return redirect('/gestion_productos')
```

**¿Qué pasa si no eres admin?**
→ HTTP 403 Forbidden (acceso denegado)

### 11. ¿Qué es MVC?

**MVC** = Modelo-Vista-Controlador (patrón de diseño)

```
┌──────────────────────────────────────────┐
│ MODELO (Datos)                           │
│ - services/*.py                          │
│ - MySQL database                         │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│ CONTROLADOR (Lógica)                     │
│ - app.py (rutas)                         │
│ - Procesa requests                       │
│ - Llama servicios                        │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│ VISTA (Presentación)                     │
│ - templates/*.html                       │
│ - Muestra datos al usuario               │
└──────────────────────────────────────────┘
```

**En Full Gaming:**
- **Modelo**: ProductoService + MySQL
- **Vista**: index.html, carrito.html, etc.
- **Controlador**: app.py (rutas Flask)

### 12. ¿Qué hace cada servicio?

| Servicio | Responsabilidad | Ejemplo |
|----------|-----------------|---------|
| **ProductoService** | CRUD de productos | Buscar, crear, editar productos |
| **UsuarioService** | Usuarios y login | Registro, autenticación |
| **CarritoService** | Carrito de compras | Agregar, eliminar items |
| **PedidoService** | Procesar compras | Guardar pedidos en BD |
| **AdminManager** | Permisos | Proteger rutas de admin |

### 13. ¿Cómo se evita SQL Injection?

Con **consultas parametrizadas**:

```python
# ❌ INSEGURO (vulnerable a SQL injection)
cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}'")

# ✅ SEGURO (parametrizado)
cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
```

**¿Por qué?**
Si un usuario ingresa: `admin@example.com' OR '1'='1`
- Inseguro: ejecuta `SELECT * FROM usuario WHERE email = 'admin@example.com' OR '1'='1'` → Devuelve todos los usuarios
- Seguro: busca literalmente el email `admin@example.com' OR '1'='1` → No encuentra nada

### 14. ¿Qué tablas hay en la base de datos?

```
producto          → Catálogo de productos
  ├── id
  ├── nombre
  ├── descripcion
  ├── categoria
  ├── precio
  ├── cantidad (stock)
  └── foto

usuario           → Usuarios registrados
  ├── idusuario
  ├── nombre
  ├── apellido
  ├── email
  ├── contraseña (hash)
  └── is_admin

pedidos           → Compras realizadas
  ├── id
  ├── usuario_id → FK a usuario
  ├── email
  ├── total
  ├── estado
  └── fecha

pedido_items      → Detalle de cada pedido
  ├── id
  ├── pedido_id → FK a pedidos
  ├── producto_id → FK a producto
  ├── cantidad
  ├── precio
  └── subtotal
```

### 15. ¿Cómo funciona la paginación?

Divide el catálogo en páginas de 9 productos:

```python
def obtener_paginados(self, pagina, por_pagina):
    inicio = (pagina - 1) * por_pagina
    # Página 1: inicio = 0   → productos 0-8
    # Página 2: inicio = 9   → productos 9-17
    # Página 3: inicio = 18  → productos 18-26
    cursor.execute('SELECT * FROM producto LIMIT %s, %s', (inicio, por_pagina))
```

**Ejemplo:**
- Total productos: 46
- Productos por página: 9
- Total páginas: ceil(46 / 9) = 6 páginas

---

## Flujos Completos con Ejemplos Reales

### FLUJO 1: Usuario Compra un Producto

```
PASO 1: Usuario ve catálogo
├─ GET http://127.0.0.1:5000/
├─ ProductoService.obtener_paginados(1, 9)
├─ SELECT * FROM producto LIMIT 0, 9
└─ Renderiza index.html con 9 productos

PASO 2: Usuario busca "Samsung"
├─ GET http://127.0.0.1:5000/buscar?q=Samsung
├─ ProductoService.buscar_productos("Samsung")
├─ SELECT * FROM producto WHERE nombre LIKE '%Samsung%'
└─ Muestra 3 resultados (TV, Aspiradora, Barra de Sonido)

PASO 3: Usuario ve detalle del Smart TV (id=28)
├─ GET http://127.0.0.1:5000/producto/28
├─ ProductoService.obtener_por_id(28)
├─ SELECT * FROM producto WHERE id = 28
└─ Muestra: "Smart TV 65 Pulgadas - $1,099,999"

PASO 4: Usuario agrega al carrito
├─ POST http://127.0.0.1:5000/agregar_carrito/28
├─ CarritoService.agregar_item(28, 1)
├─ session['carrito'] = {'28': 1}
└─ Respuesta: {"ok": true, "mensaje": "Producto agregado"}

PASO 5: Usuario ve su carrito
├─ GET http://127.0.0.1:5000/carrito
├─ CarritoService.obtener_items_detalle()
├─ Para cada item en carrito: buscar producto en BD
└─ Muestra: 1 producto, Total: $1,099,999

PASO 6: Usuario confirma compra (debe estar logueado)
├─ Si NO está logueado → Redirige a /acceso
└─ Si está logueado → continúa...

PASO 7: Usuario se loguea
├─ POST http://127.0.0.1:5000/cuenta
├─ email: juan@example.com, contraseña: pass123
├─ UsuarioService.login()
├─ bcrypt.checkpw() verifica contraseña
├─ session['usuario_id'] = 14
└─ Respuesta: {"mensaje": "Login exitoso"}

PASO 8: Usuario procesa compra
├─ POST http://127.0.0.1:5000/procesar_compra
├─ PedidoService.crear_pedido()
│   ├─ INSERT INTO pedidos (usuario_id=14, total=1099999)
│   └─ INSERT INTO pedido_items (pedido_id=50, producto_id=28, cantidad=1)
├─ ProductoService.restar_stock(28, 1)
│   └─ UPDATE producto SET cantidad = cantidad - 1 WHERE id = 28
├─ CarritoService.vaciar_carrito()
│   └─ session['carrito'] = {}
└─ Respuesta: {"ok": true, "pedido_id": 50}

RESULTADO:
✅ Pedido creado (ID: 50)
✅ Stock actualizado (Smart TV: de 2 a 1 unidad)
✅ Carrito vaciado
✅ Usuario puede ver su historial de compras
```

### FLUJO 2: Admin Crea un Producto

```
PASO 1: Admin se loguea
├─ POST http://127.0.0.1:5000/cuenta
├─ email: admin@example.com, contraseña: admin123
├─ UsuarioService.login()
├─ session['es_admin'] = 1
└─ Acceso a rutas administrativas habilitado

PASO 2: Admin accede a formulario
├─ GET http://127.0.0.1:5000/formulario
├─ @admin_manager.requerir_admin verifica session['es_admin']
└─ Renderiza formulario_carga_producto.html

PASO 3: Admin completa y envía formulario
├─ Datos:
│   ├─ Nombre: "Notebook Lenovo IdeaPad 3"
│   ├─ Descripción: "Procesador Intel Core i5..."
│   ├─ Categoría: "Tecnología"
│   ├─ Precio: 599999
│   ├─ Cantidad: 10
│   └─ Foto: notebook-lenovo.jpg (archivo)
└─ POST http://127.0.0.1:5000/cargar_producto

PASO 4: Servidor procesa el archivo
├─ secure_filename('notebook-lenovo.jpg')
├─ Guarda en: static/uploads/notebook-lenovo.jpg
└─ Retorna ruta: 'static/uploads/notebook-lenovo.jpg'

PASO 5: Servidor guarda en base de datos
├─ ProductoService.agregar_producto()
├─ INSERT INTO producto (nombre, descripcion, categoria, precio, cantidad, foto)
│   VALUES ('Notebook Lenovo IdeaPad 3', '...', 'Tecnología', 599999, 10, 'static/uploads/notebook-lenovo.jpg')
└─ Respuesta: {"mensaje": "Producto cargado correctamente"}

RESULTADO:
✅ Producto creado con ID 47
✅ Imagen guardada en servidor
✅ Visible en catálogo para todos los usuarios
```

---

## Comandos Útiles

### Ejecutar el sistema
```bash
# 1. Activar entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar database.py con tus credenciales locales

# 4. Ejecutar aplicación
python app.py

# Acceder desde navegador:
# http://127.0.0.1:5000
```

### Crear un usuario administrador
```bash
python crear_admin.py
```

### Verificar conexión a base de datos
```
http://127.0.0.1:5000/verificar_conexion
```

---

## Errores Comunes y Soluciones

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solución**: `pip install -r requirements.txt`

### Error: "Can't connect to MySQL server"
**Solución**: 
1. Verificar que MySQL esté corriendo
2. Configurar `database.py` con credenciales correctas

### Error: 403 Forbidden al acceder a /formulario
**Solución**: Debes estar logueado como administrador (is_admin = 1)

### El carrito se vacía al cerrar el navegador
**Solución**: Es comportamiento normal. La sesión expira. Para persistir: guardar carrito en BD.

---

## Puntos Clave para Recordar

1. **Flask** es el framework web (maneja HTTP requests/responses)
2. **Services** separan lógica de negocio de rutas
3. **bcrypt** protege contraseñas (hash irreversible)
4. **Sesiones** guardan estado temporal del usuario
5. **Decoradores** protegen rutas (@admin_manager.requerir_admin)
6. **Consultas parametrizadas** previenen SQL injection
7. **MVC** organiza el código (Modelo-Vista-Controlador)
8. **Carrito en sesión** es rápido pero temporal
9. **Pedidos en BD** son permanentes y auditables
10. **Stock se actualiza** al confirmar compra

---

## Vocabulario Técnico

- **CRUD**: Create, Read, Update, Delete (operaciones básicas)
- **Hash**: Función que convierte datos en cadena irreversible
- **Salt**: Dato aleatorio agregado antes de hashear
- **Sesión**: Datos temporales asociados a un usuario
- **Cookie**: Archivo pequeño guardado en el navegador
- **Decorador**: Función que modifica el comportamiento de otra función
- **ORM**: Object-Relational Mapping (no se usa en este proyecto)
- **API REST**: Interfaz de comunicación (parcialmente implementada)
- **JSON**: Formato de intercambio de datos
- **AJAX**: Peticiones asíncronas (fetch en JavaScript)

---

## Diagrama de Flujo Simplificado

```
          ┌──────────────┐
          │   USUARIO    │
          └──────┬───────┘
                 │
                 │ 1. HTTP Request
                 ▼
          ┌──────────────┐
          │  FLASK       │
          │  (app.py)    │ ← Rutas: @app.route('/')
          └──────┬───────┘
                 │
                 │ 2. Llama servicio
                 ▼
          ┌──────────────┐
          │  SERVICE     │
          │  (lógica)    │ ← ProductoService, UsuarioService, etc.
          └──────┬───────┘
                 │
                 │ 3. Consulta SQL
                 ▼
          ┌──────────────┐
          │   MYSQL      │
          │  (datos)     │ ← Tablas: producto, usuario, pedidos
          └──────┬───────┘
                 │
                 │ 4. Resultados
                 ▼
          ┌──────────────┐
          │  SERVICE     │ ← Procesa datos
          └──────┬───────┘
                 │
                 │ 5. Retorna datos
                 ▼
          ┌──────────────┐
          │  FLASK       │ ← Renderiza template
          └──────┬───────┘
                 │
                 │ 6. HTTP Response
                 ▼
          ┌──────────────┐
          │  USUARIO     │ ← Ve HTML en navegador
          └──────────────┘
```

---

¡Esta guía te da todo lo necesario para explicar el sistema con confianza! 🎓
