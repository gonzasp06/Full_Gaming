# 📝 RESUMEN EJECUTIVO PARA EL EXAMEN

## 🎯 Lo Más Importante en 5 Minutos

### ¿Qué es Full Gaming?
Un **e-commerce** (tienda online) para vender hardware y software de computación, desarrollado con **Flask + MySQL**.

### Características Principales
1. ✅ Catálogo de productos con búsqueda y filtrado
2. ✅ Carrito de compras en sesión
3. ✅ Sistema de usuarios con autenticación segura (bcrypt)
4. ✅ Panel administrativo para gestionar productos
5. ✅ Procesamiento de pedidos con control de stock

---

## 🏗️ Arquitectura en 3 Capas

```
1. PRESENTACIÓN (Vista)
   └─ templates/*.html → Lo que ve el usuario

2. LÓGICA (Controlador + Servicios)
   ├─ app.py → Rutas HTTP
   └─ services/*.py → Lógica de negocio

3. DATOS (Modelo)
   └─ MySQL → Base de datos
```

---

## 🔐 Seguridad Implementada

### 1. Contraseñas Encriptadas (bcrypt)
```python
# Al registrar:
hash = bcrypt.hashpw("miPass123", salt)
# Guarda: "$2b$12$VBLLKIlD4P4a..."

# Al hacer login:
bcrypt.checkpw("miPass123", hash)  # → True/False
```

**¿Por qué es seguro?**
- No se puede desencriptar (hash irreversible)
- Cada contraseña tiene un "salt" único
- Costoso computacionalmente (dificulta fuerza bruta)

### 2. Sesiones Cifradas
```python
session['usuario_id'] = 14
# Cookie firmada con secret_key
# No se puede modificar desde el navegador
```

### 3. Protección de Rutas Admin
```python
@admin_manager.requerir_admin  # Decorador
def eliminar_producto(id):
    # Solo si session['es_admin'] == 1
```

### 4. SQL Injection Prevención
```python
# ✅ Seguro (parametrizado)
cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))

# ❌ Inseguro (vulnerable)
cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}'")
```

---

## 💾 Base de Datos: 4 Tablas Clave

```
1. producto      → Catálogo (id, nombre, precio, stock, foto)
2. usuario       → Usuarios (id, email, contraseña_hash, is_admin)
3. pedidos       → Compras (id, usuario_id, total, fecha)
4. pedido_items  → Detalle de pedidos (pedido_id, producto_id, cantidad)
```

**Relaciones:**
- 1 usuario → N pedidos
- 1 pedido → N items
- 1 producto → N items

---

## 🛒 Carrito de Compras

### ¿Dónde se guarda?
En la **sesión** (cookie cifrada), NO en base de datos.

```python
session['carrito'] = {
    '18': 2,  # producto_id: cantidad
    '19': 1
}
```

### ¿Por qué en sesión?
- ✅ Rápido (sin consultas a BD)
- ✅ Funciona sin login
- ✅ Temporal (se limpia al comprar)

### Flujo Completo
```
1. Agregar producto → session['carrito']['18'] = 2
2. Ver carrito → Busca detalles en BD
3. Confirmar compra → Crear pedido en BD
4. Restar stock → UPDATE producto
5. Vaciar carrito → session['carrito'] = {}
```

---

## 📦 Servicios: Separación de Responsabilidades

### ¿Qué es un Servicio?
Clase que encapsula la lógica de negocio de una entidad.

### 5 Servicios Principales

#### 1. ProductoService
```python
• obtener_todos()      → Lista productos
• obtener_por_id(id)   → Detalle de producto
• buscar_productos()   → Búsqueda
• agregar_producto()   → Crear (admin)
• editar_producto()    → Actualizar (admin)
• eliminar_producto()  → Eliminar (admin)
```

#### 2. UsuarioService
```python
• crear_usuario()  → Registro (con bcrypt)
• login()          → Autenticación
• buscar_usuario() → Por email
```

#### 3. CarritoService
```python
• agregar_item()      → Agregar al carrito
• obtener_carrito()   → Ver carrito
• actualizar_cantidad() → Cambiar cantidad
• vaciar_carrito()    → Limpiar
```

#### 4. PedidoService
```python
• crear_pedido()  → Guardar compra en BD
```

#### 5. AdminManager
```python
• requerir_admin() → Decorador para proteger rutas
• es_admin()       → Verificar permisos
```

---

## 🔄 Flujos Importantes

### Flujo 1: Registro + Login

```
REGISTRO:
Usuario → form → POST /cargar_usuario
         → UsuarioService.crear_usuario()
         → bcrypt.hashpw(contraseña)
         → INSERT INTO usuario
         → {"mensaje": "Cuenta creada"}

LOGIN:
Usuario → form → POST /cuenta
         → UsuarioService.login(email, pass)
         → bcrypt.checkpw(pass, hash)
         → session['usuario_id'] = 14
         → {"mensaje": "Login exitoso"}
```

### Flujo 2: Compra Completa

```
1. Agregar al carrito
   └─ session['carrito']['18'] = 2

2. Ver carrito
   └─ Busca detalles en producto tabla

3. Confirmar compra
   ├─ INSERT INTO pedidos (total=1178357)
   ├─ INSERT INTO pedido_items (producto_id=18, cantidad=2)
   ├─ UPDATE producto SET cantidad = cantidad - 2
   └─ session['carrito'] = {}

4. Resultado
   └─ Pedido #42 creado, stock actualizado
```

### Flujo 3: Admin Gestiona Producto

```
1. Login como admin
   └─ session['es_admin'] = 1

2. Crear producto
   ├─ GET /formulario (protegido)
   ├─ POST /cargar_producto
   ├─ secure_filename(foto)
   ├─ Guardar en static/uploads/
   └─ INSERT INTO producto

3. Editar producto
   ├─ GET /editar_producto/18
   ├─ POST /actualizar_producto/18
   └─ UPDATE producto WHERE id=18

4. Eliminar producto
   ├─ GET /eliminar_producto/18
   └─ DELETE FROM producto WHERE id=18
```

---

## 🎓 Preguntas Típicas de Examen

### 1. ¿Qué es MVC y cómo se aplica aquí?

**MVC** = Modelo-Vista-Controlador

- **Modelo**: `services/*.py` + MySQL (datos y lógica)
- **Vista**: `templates/*.html` (presentación)
- **Controlador**: `app.py` (rutas Flask)

**Ejemplo:**
```python
# CONTROLADOR (app.py)
@app.route('/productos')
def listar_productos():
    service = ProductoService()  # Modelo
    productos = service.obtener_todos()
    return render_template('productos.html', productos)  # Vista
```

### 2. ¿Por qué usar bcrypt para contraseñas?

✅ **Hash irreversible** → No se puede desencriptar
✅ **Salt único** → Misma contraseña, hash diferente
✅ **Costoso** → Dificulta ataques de fuerza bruta
✅ **Estándar de la industria** → Probado y confiable

**Alternativas inseguras:**
❌ Texto plano → Cualquiera puede leer
❌ MD5/SHA1 → Muy rápidos, fáciles de romper
❌ Base64 → No es encriptación, solo codificación

### 3. ¿Cómo funciona la sesión en Flask?

```python
# Flask guarda session en una cookie FIRMADA
session['usuario_id'] = 14

# Cookie en navegador:
# session=eyJ1c3VhcmlvX2lkIjoxNH0.ZwT8xg.signature

# Estructura:
# [datos_base64].[timestamp].[firma_HMAC]
```

**Características:**
- Cifrada con `secret_key`
- No modificable sin la clave
- Expira en 7 días (configurable)
- Se borra con `session.clear()`

### 4. ¿Qué pasa si dos usuarios compran el último producto?

**Escenario:**
- Stock: 1 unidad
- Usuario A y B agregan al carrito simultáneamente

**Solución actual:**
```python
# Al procesar compra:
UPDATE producto
SET cantidad = cantidad - 1
WHERE id = 18 AND cantidad >= 1  # ← Validación atómica
```

Si stock < cantidad:
→ Primera compra: OK (stock 1 → 0)
→ Segunda compra: FALLA (stock 0, no cumple >= 1)

**Mejora sugerida:**
- Validar stock al agregar al carrito
- Reservar stock temporalmente
- Timeout de reserva (ej: 10 minutos)

### 5. ¿Cómo se comunica el frontend con el backend?

**Tecnología:** AJAX (fetch API)

```javascript
// FRONTEND (JavaScript)
fetch('/agregar_carrito/18', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({cantidad: 2})
})
.then(response => response.json())
.then(data => alert(data.mensaje))
```

```python
# BACKEND (Flask)
@app.route('/agregar_carrito/<int:id>', methods=['POST'])
def agregar_carrito(id):
    datos = request.get_json()  # {'cantidad': 2}
    # ... lógica ...
    return jsonify({"ok": True, "mensaje": "Agregado"}), 200
```

**Ventajas:**
- ✅ Sin recargar la página
- ✅ Respuesta rápida
- ✅ Mejor experiencia de usuario

### 6. ¿Qué es un decorador y para qué se usa?

**Definición:** Función que modifica el comportamiento de otra función.

**Ejemplo en el proyecto:**
```python
@admin_manager.requerir_admin
def eliminar_producto(id):
    # Solo se ejecuta si es admin
    pass

# Sin decorador, sería:
def eliminar_producto(id):
    if not es_admin():
        return abort(403)
    # ... código ...
```

**Otros decoradores en Flask:**
- `@app.route('/ruta')` → Define una ruta HTTP
- `@app.before_request` → Ejecuta antes de cada request

---

## 📊 Datos de Ejemplo del Sistema

### Productos Reales en el Catálogo

```
ID: 18 | TV Philips 50" 4K        | $524,699  | Stock: 9
ID: 19 | Parlante Bluetooth       | $128,959  | Stock: 18
ID: 28 | Smart TV Samsung 65"     | $1,099,999| Stock: 2
ID: 41 | Tablet Lenovo 11"        | $729,999  | Stock: 4
ID: 44 | Xbox Series S            | $786,599  | Stock: 5
```

### Usuarios de Ejemplo

```
ID: 14 | Juan Pérez    | juan@example.com    | is_admin: 0
ID: 17 | María García  | maria@example.com   | is_admin: 0
```

### Categorías Disponibles

```
• Electrodomésticos (23 productos)
• TV_Video (3 productos)
• Tecnología (15 productos)
• Climatización (5 productos)
```

---

## 💡 Conceptos Clave para Recordar

### 1. Separación de Responsabilidades
Cada componente tiene un propósito único:
- `app.py` → Solo rutas
- `services/` → Solo lógica
- `templates/` → Solo presentación

### 2. DRY (Don't Repeat Yourself)
Los servicios evitan duplicar código:
```python
# En lugar de copiar consultas SQL en cada ruta,
# se usa ProductoService.obtener_por_id() en múltiples lugares
```

### 3. Seguridad por Capas
- Contraseñas: bcrypt
- Sesiones: Cookies firmadas
- SQL: Consultas parametrizadas
- Admin: Decoradores de autorización
- Uploads: secure_filename()

### 4. Estado vs Persistencia
- **Estado temporal** → Sesión (carrito)
- **Persistencia** → Base de datos (pedidos)

### 5. RESTful Aproximado
```
GET  /producto/18     → Ver
POST /cargar_producto → Crear
POST /actualizar_producto/18 → Editar
GET  /eliminar_producto/18   → Eliminar
```

---

## 🚀 Comandos Rápidos

```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\Activate.ps1

# Activar (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py

# Acceder desde navegador
http://127.0.0.1:5000
```

---

## 📚 Documentación Completa

Para más detalles, consulta:

1. **[DOCUMENTACION_SISTEMA.md](DOCUMENTACION_SISTEMA.md)**
   → Explicación detallada de todo el sistema

2. **[GUIA_RAPIDA_EXAMEN.md](GUIA_RAPIDA_EXAMEN.md)**
   → Respuestas rápidas a preguntas comunes

3. **[EJEMPLOS_PRACTICOS.md](EJEMPLOS_PRACTICOS.md)**
   → Código comentado y casos de uso

4. **[DIAGRAMAS_VISUALES.md](DIAGRAMAS_VISUALES.md)**
   → Diagramas ASCII de arquitectura y flujos

---

## ✅ Checklist para el Examen

Asegúrate de poder explicar:

- [ ] Arquitectura MVC del sistema
- [ ] Cómo funciona bcrypt (hash + salt)
- [ ] Diferencia entre sesión y base de datos
- [ ] Flujo completo de una compra
- [ ] Cómo se protegen las rutas de admin
- [ ] Qué hace cada servicio
- [ ] Estructura de la base de datos
- [ ] Cómo prevenir SQL injection
- [ ] Por qué el carrito está en sesión
- [ ] Flujo de autenticación completo

---

## 🎯 Puntos Importantes para Destacar al Profesor

1. **Arquitectura Limpia**
   - Separación de responsabilidades con servicios
   - Código organizado y mantenible

2. **Seguridad Implementada**
   - bcrypt para contraseñas
   - Sesiones cifradas
   - Protección contra SQL injection
   - Control de acceso por roles

3. **Funcionalidad Completa**
   - CRUD de productos
   - Sistema de usuarios
   - Carrito de compras
   - Procesamiento de pedidos
   - Panel administrativo

4. **Buenas Prácticas**
   - Consultas parametrizadas
   - Validación de datos
   - Manejo de errores
   - Código reutilizable

5. **Escalabilidad**
   - Fácil agregar nuevas funcionalidades
   - Servicios independientes
   - Base de datos normalizada

---

¡Mucha suerte en tu examen! 🍀

Con esta documentación completa, tenés todo lo necesario para explicar el sistema en detalle y responder cualquier pregunta que te hagan.

**Tip final:** Practicá explicar cada flujo con tus propias palabras. Entender es más importante que memorizar. 🧠
