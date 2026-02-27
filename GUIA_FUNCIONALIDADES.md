# 🎮 Full Gaming — Guía de Funcionalidades

> **¿Para quién es este documento?**
> Está pensado para alguien que quiere entender cómo funciona el sistema, ya sea para presentarlo, explicarlo o simplemente entender qué hace cada parte. Mezcla explicaciones simples con algunos detalles técnicos.

---

## 📋 Índice

1. [¿Qué es Full Gaming?](#1-qué-es-full-gaming)
2. [Tecnologías usadas](#2-tecnologías-usadas)
3. [¿Cómo se comunica el usuario con el sistema?](#3-cómo-se-comunica-el-usuario-con-el-sistema)
4. [Registro e Inicio de Sesión](#4-registro-e-inicio-de-sesión)
5. [El Carrito de Compras](#5-el-carrito-de-compras)
6. [Los Pedidos](#6-los-pedidos)
7. [Gestión de Productos](#7-gestión-de-productos)
8. [Gestión de Stock](#8-gestión-de-stock)
9. [Gestión de Usuarios](#9-gestión-de-usuarios)
10. [Estadísticas del Negocio](#10-estadísticas-del-negocio)
11. [El Perfil del Usuario](#11-el-perfil-del-usuario)
12. [Sistema de Emails](#12-sistema-de-emails)
13. [Seguridad del Sistema](#13-seguridad-del-sistema)
14. [Vista Mobile (Responsive)](#14-vista-mobile-responsive)
15. [Resumen Visual del Flujo](#15-resumen-visual-del-flujo)

---

## 1. ¿Qué es Full Gaming?

**Full Gaming** es una tienda online (e-commerce) para venta de hardware y periféricos gamer.

Hay dos tipos de usuarios:

| Tipo | ¿Qué puede hacer? |
|------|-------------------|
| **Cliente** | Ver productos, buscarlos, agregarlos al carrito, comprar, gestionar su perfil y direcciones |
| **Administrador** | Todo lo anterior + cargar/editar/eliminar productos, gestionar usuarios, agregar stock y ver estadísticas del negocio |

---

## 2. Tecnologías usadas

| Tecnología | Para qué sirve | ¿Qué es en términos simples? |
|------------|---------------|------------------------------|
| **Python** | Lenguaje principal del backend | El "cerebro" del sistema, procesa toda la lógica |
| **Flask** | Framework web | El sistema que recibe peticiones y devuelve páginas |
| **MySQL** | Base de datos | Donde se guarda toda la información (productos, usuarios, pedidos) |
| **HTML + CSS** | Frontend / Interfaz visual | Lo que ve el usuario en pantalla |
| **JavaScript** | Interactividad | Los botones, modales, actualizaciones sin recargar la página |
| **Bootstrap** | Diseño responsive | Permite que la página se adapte a celular y PC automáticamente |
| **bcrypt** | Seguridad de contraseñas | Cifra las contraseñas para que nadie pueda leerlas, ni siquiera el admin |
| **SMTP / Gmail** | Envío de emails | Para enviar códigos de verificación y bienvenidas |

---

## 3. ¿Cómo se comunica el usuario con el sistema?

Cada vez que el usuario hace algo (clic en un botón, llenar un formulario, navegar a una página), el navegador hace una **petición HTTP** al servidor.

```
Usuario hace clic
      ↓
Navegador envía petición a Flask (ej: POST /cuenta)
      ↓
Flask ejecuta la función correspondiente
      ↓
La función consulta/modifica MySQL si es necesario
      ↓
Flask devuelve una respuesta (página HTML o dato JSON)
      ↓
El navegador muestra el resultado
```

**¿Qué es JSON?** Es un formato de texto que usan el servidor y el navegador para pasarse datos entre sí sin recargar la página. Por ejemplo, cuando hacés clic en "Agregar al carrito", el navegador le manda al servidor `{"producto_id": 5, "cantidad": 1}` y el servidor responde `{"ok": true}`.

---

## 4. Registro e Inicio de Sesión

### Registro

Cuando un usuario se registra (`/nuevo_usuario`):

1. Ingresa nombre, apellido, email y contraseña
2. El sistema valida que el email no esté ya registrado
3. La contraseña se **cifra con bcrypt** antes de guardarla (nunca se guarda en texto plano)
4. Se crea el registro en la tabla `usuario`
5. El sistema loguea al usuario automáticamente (crea una sesión)
6. Se envía un **email de bienvenida** con un link para eliminar la cuenta si no fue el usuario quien se registró (medida de seguridad)

### Inicio de Sesión

Cuando un usuario inicia sesión (`/cuenta`):

1. Ingresa email y contraseña
2. El sistema busca el usuario por email en la base de datos
3. Usa `bcrypt.checkpw()` para comparar la contraseña ingresada con el hash guardado
4. Si coincide, crea una **sesión del servidor** con el ID, nombre, email y rol del usuario
5. Esa sesión dura hasta que el usuario cierre sesión o limpie las cookies

```python
# Simplificado: así funciona la validación de contraseña
if bcrypt.checkpw(contraseña_ingresada.encode(), hash_guardado_en_bd):
    # Contraseña correcta → iniciar sesión
```

### Sesión

La **sesión** es como una "memoria temporal" en el servidor que recuerda quién está logueado. Guarda:

- `usuario_id` → el ID de la persona
- `usuario_nombre` → su nombre
- `usuario_email` → su email
- `es_admin` → si es administrador (1) o no (0)

---

## 5. El Carrito de Compras

### ¿Cómo funciona?

El carrito **no se guarda en la base de datos**. Se guarda en la **sesión del navegador** (en memoria del servidor). Esto lo hace más rápido porque no necesita consultar la base de datos cada vez que se agrega un producto.

Internamente es un simple diccionario:

```python
# Así luce el carrito internamente
session['carrito'] = {
    "3": 2,   # producto con ID 3, cantidad 2
    "7": 1,   # producto con ID 7, cantidad 1
    "12": 3   # producto con ID 12, cantidad 3
}
```

### Operaciones del carrito

| Acción | ¿Qué hace el sistema? |
|--------|----------------------|
| **Agregar producto** | Si el producto ya está, suma la cantidad. Si no, lo agrega con cantidad 1 |
| **Cambiar cantidad** | Actualiza el número directamente en la sesión |
| **Eliminar producto** | Borra la clave del diccionario |
| **Ver total** | Recorre cada producto, busca su precio en la BD y suma |
| **Vaciar carrito** | Reemplaza el diccionario por uno vacío |

### Al hacer una compra

Cuando el usuario confirma la compra:

1. Se llama al `PedidoService` para crear el pedido en la base de datos
2. Se descuenta el stock de cada producto vendido
3. Se vacía el carrito de la sesión
4. El usuario recibe confirmación

---

## 6. Los Pedidos

### ¿Qué pasa cuando alguien compra?

El `PedidoService` maneja todo el proceso de compra:

```
Confirmación del carrito
         ↓
Se crea registro en tabla "pedidos"
(usuario, total, fecha, dirección de envío, estado: "completado")
         ↓
Se crean registros en tabla "pedido_items"
(uno por cada producto: qué producto, cantidad, precio en ese momento, ganancia calculada)
         ↓
Se descuenta el stock de cada producto en tabla "producto"
         ↓
Se vacía el carrito
```

### Datos que guarda un pedido

- **Quién compró**: ID y email del usuario
- **Cuánto pagó**: total en pesos
- **Qué compró**: lista de productos con cantidades y precios exactos al momento de la compra
- **Dónde enviar**: dirección, provincia, código postal
- **Datos de contacto**: teléfono, DNI
- **Cuándo**: fecha y hora automática

> 💡 Los precios se guardan **al momento de la compra**. Si el admin cambia el precio de un producto después, los pedidos anteriores no se modifican.

### Cálculo de ganancia por pedido

Cuando se registra el pedido, el sistema también calcula cuánto ganó el negocio en cada ítem:

```
Ganancia por ítem = (precio de venta - costo del producto) × cantidad
```

Estos datos se usan luego en las estadísticas.

---

## 7. Gestión de Productos

### ¿Qué puede hacer el admin?

Desde `/gestion_productos`, el administrador puede:

- **Ver todos los productos** con filtros por estado de stock (normal, bajo, agotado) y por marca
- **Buscar productos** en tiempo real sin recargar la página
- **Agregar producto**: nombre, descripción, categoría, precio, costo, stock, imagen y marca
- **Editar producto**: modificar cualquier dato
- **Eliminar producto**: borra el producto y sus registros relacionados de stock

### ¿Cómo se suben las imágenes?

Las imágenes pueden ser:

1. **URL externa**: Se copia el link de una imagen de internet (ej: imagen de MercadoLibre)
2. **Archivo local**: Se sube desde la computadora y se guarda en `/static/uploads/`

El sistema muestra la imagen en el catálogo usando el CSS `object-fit: contain` para que siempre se vea bien sin importar las proporciones originales de la imagen.

### Estados de stock

| Estado | Condición | Color en pantalla |
|--------|-----------|-------------------|
| **Normal** | Stock > umbral | Verde |
| **Bajo stock** | Stock ≤ umbral | Amarillo |
| **Agotado** | Stock = 0 | Rojo |

---

## 8. Gestión de Stock

El `StockService` maneja la **mercadería que el negocio COMPRA** para revender (no las ventas a clientes).

### ¿Para qué sirve?

El admin puede registrar cada vez que compra mercadería:

- ¿Qué producto compró?
- ¿Cuántas unidades compró?
- ¿Cuánto invirtió en total?
- ¿Cuál fue el costo unitario?
- ¿A qué precio sugiere venderlo?
- ¿Qué porcentaje de ganancia espera?

Estos datos permiten al sistema calcular:

- El **costo real** de los productos vendidos
- La **ganancia bruta** del negocio
- Comparar **precio de venta vs costo de compra**

### Flujo de stock

```
Admin compra mercadería del proveedor
         ↓
Registra la compra en el sistema (stock_compras)
         ↓
El stock del producto aumenta en la tabla producto
         ↓
Cuando alguien compra, el stock baja automáticamente
         ↓
Las estadísticas usan todos estos datos para calcular ganancias
```

---

## 9. Gestión de Usuarios

Desde `/usuarios`, el administrador puede:

### Ver usuarios

- Lista de todos los usuarios registrados
- Filters por estado, rol y búsqueda por nombre o email
- Ver la fecha del último acceso de cada usuario
- Ver cuántos pedidos hizo cada usuario

### Acciones disponibles

| Acción | Descripción |
|--------|-------------|
| **Ver detalle** | Modal con todos los datos del usuario + historial de pedidos |
| **Dar/quitar admin** | Cambiar si el usuario es administrador o cliente normal |
| **Eliminar cuenta** | Elimina el usuario y todos sus datos relacionados |

### ¿Cómo funciona el "dar admin"?

Solo se modifica el campo `is_admin` en la tabla `usuario`:
- `is_admin = 0` → cliente normal
- `is_admin = 1` → administrador

El sistema verifica esto en cada ruta protegida con un decorador `@requerir_admin`.

---

## 10. Estadísticas del Negocio

El panel de estadísticas (`/estadisticas`) es solo visible para administradores. Muestra una foto completa del estado del negocio.

### ¿Qué calcula?

**Ventas**
- Total vendido en pesos (suma de todos los pedidos)
- Cantidad de ventas realizadas
- Ticket promedio (total ÷ cantidad de ventas)

**Ganancia**
- Ganancia total (precio de venta − costo × cantidad por cada ítem vendido)
- Margen de ganancia promedio en porcentaje

**Usuarios**
- Total de usuarios registrados
- Usuarios activos (que compraron alguna vez)
- Nuevos usuarios en el último mes

**Productos**
- Productos más vendidos (ranking por cantidad vendida)
- Categorías más vendidas
- Productos con bajo stock o agotados

**Ventas por período**
- Gráfico de ventas por mes
- Comparación entre períodos

### ¿Cómo se calculan?

El `EstadisticasService` hace consultas directas a MySQL combinando varias tablas:

```sql
-- Ejemplo simplificado: ganancia total
SELECT SUM((p.precio - prod.costo) * p.cantidad)
FROM pedido_items p
JOIN producto prod ON p.producto_id = prod.id
```

---

## 11. El Perfil del Usuario

Desde `/perfil`, cada usuario puede gestionar su cuenta. Está dividido en 3 secciones:

### Sección "Resumen"

Muestra un resumen de la cuenta:
- Datos personales (nombre, email, teléfono, DNI)
- Dirección principal configurada
- Últimos pedidos realizados

### Sección "Direcciones"

El usuario puede gestionar múltiples direcciones de envío:
- Agregar nueva dirección (calle, número, ciudad, provincia, código postal)
- Editar dirección existente
- Eliminar dirección
- Marcar una como **dirección principal** (se usa automáticamente al comprar)

Cada dirección se guarda en la tabla `direcciones` con referencia al `usuario_id`.

### Sección "Editar Cuenta"

- Modificar nombre, apellido, email, teléfono y DNI
- **Cambiar contraseña** (requiere verificación por email):
  1. El sistema envía un código de 6 dígitos al email del usuario
  2. El usuario ingresa el código en un modal
  3. Si el código es correcto, puede ingresar la nueva contraseña
- **Eliminar cuenta** (zona peligrosa):
  1. Se muestra una advertencia detallada de todo lo que se perderá
  2. El usuario debe ingresar su contraseña para confirmar
  3. Se eliminan todos sus datos (pedidos, direcciones, cuenta)
  4. La sesión se cierra automáticamente

---

## 12. Sistema de Emails

El sistema usa **Gmail** como servidor de correos. Envía emails automáticos en 3 situaciones:

### Email de Bienvenida

Se envía cuando alguien se registra. Incluye:
- Mensaje de bienvenida personalizado
- Botón para ir a la tienda
- Sección de seguridad: "¿No te registraste? → Eliminá tu cuenta" con un link único y de un solo uso

### Email de Recuperación de Contraseña

Cuando el usuario olvida su contraseña:
1. Ingresa su email en el formulario de recuperación
2. El sistema genera un código de 6 dígitos con expiración de 10 minutos
3. Envía el código al email
4. El usuario ingresa el código y puede crear una nueva contraseña

### Email de Cambio de Contraseña (doble verificación)

Cuando el usuario quiere cambiar su contraseña desde el perfil:
1. El sistema envía un código de verificación a su email actual
2. Confirma que es realmente el dueño de la cuenta
3. Recién entonces puede cambiar la contraseña

### Modo DEV (sin SMTP configurado)

Si el sistema no tiene credenciales de email, en vez de enviar el email, muestra el código directamente en la pantalla. Esto permite probar el sistema aunque no haya configuración de email.

---

## 13. Seguridad del Sistema

### Contraseñas cifradas (bcrypt)

Las contraseñas **nunca** se guardan en texto plano. Se guarda un "hash" que es una versión cifrada irreversible:

```
contraseña original: "12345"
hash guardado en BD: "$2b$12$eImiTXuWVxfM37uY3Jaln..."
```

No hay forma de "descifrar" el hash. Para validar, se vuelve a cifrar la contraseña ingresada y se compara con el hash guardado.

### Rutas protegidas

Hay dos tipos de protección:

| Protección | ¿Cómo funciona? | Ejemplo |
|------------|-----------------|---------|
| **@requerir_login** | Verifica que haya sesión activa | `/perfil`, `/carrito` |
| **@requerir_admin** | Verifica que `es_admin == 1` | `/gestion_productos`, `/estadisticas` |

Si alguien intenta acceder a una ruta de admin sin serlo, es redirigido o recibe un error 403.

### Tokens de un solo uso

Para ciertas operaciones sensibles (recuperar contraseña, eliminar cuenta por email), el sistema genera tokens únicos de 32 caracteres. Una vez usados, se invalidan.

### Validación en el servidor

Todas las validaciones importantes se hacen en el servidor (Python/Flask), no solo en el navegador. Aunque alguien desactive el JavaScript, los datos siguen siendo validados.

---

## 14. Vista Mobile (Responsive)

El sistema usa **diseño responsive**, lo que significa que se adapta automáticamente a cualquier tamaño de pantalla.

### ¿Cómo funciona técnicamente?

Se usa una técnica de CSS llamada **media query**:

```css
/* Este estilo solo aplica en pantallas de 768px o menos (celulares) */
@media (max-width: 768px) {
  .navbar {
    padding: 10px;  /* menos espacio en mobile */
  }
}
```

El navegador detecta el ancho de la pantalla y aplica los estilos correspondientes. La PC y el celular usan el mismo HTML, pero diferentes estilos CSS.

### Adaptaciones en mobile

- **Navbar**: más compacto, buscador debajo, íconos sin texto
- **Carrusel**: más chico, sin bordes
- **Categorías**: grilla 2×2 en vez de 5 en fila
- **Productos**: imágenes fijas en contenedor, no se deforman
- **Tablas de gestión**: scroll horizontal para ver todas las columnas
- **Formularios**: inputs más grandes para evitar el zoom automático de iOS
- **Modales**: botones en columna, ocupan todo el ancho

---

## 15. Resumen Visual del Flujo

### Flujo del cliente

```
Entra al sitio (/)
      ↓
Ve catálogo con productos y carrusel
      ↓
Busca productos o navega por categorías
      ↓
Hace clic en un producto → ve detalle
      ↓
Agrega al carrito (sin necesitar cuenta)
      ↓
Va al carrito → hace clic en "Comprar"
      ↓
Si no está logueado → redirige a /acceso
      ↓
Completa datos de envío
      ↓
Confirma compra → se crea el pedido en BD
      ↓
Stock baja, carrito se vacía
      ↓
Ve confirmación del pedido
```

### Flujo del administrador

```
Login con cuenta admin
      ↓
Navbar muestra barra de administración
      ↓
      ├── Estadísticas → dashboard con métricas del negocio
      ├── Productos → cargar, editar, eliminar, ver stock
      └── Usuarios → ver, dar admin, eliminar cuentas
```

### ¿Cómo saber si el usuario es admin?

```python
# En cada ruta protegida, Flask verifica la sesión
if session.get('es_admin') != 1:
    return redirect('/acceso')  # No es admin, fuera
```

---

## 📂 Archivos clave del sistema

| Archivo | Función |
|---------|---------|
| `app.py` | Punto de entrada. Define todas las rutas (URLs) del sistema |
| `database.py` | Función de conexión a MySQL |
| `migrations.py` | Crea/actualiza columnas en la BD automáticamente al iniciar |
| `services/carrito_service.py` | Lógica completa del carrito (sesión) |
| `services/pedido_service.py` | Creación de pedidos y descuento de stock |
| `services/producto_service.py` | CRUD de productos |
| `services/usuario_service.py` | Registro, login, perfil, recuperación de contraseña |
| `services/estadisticas_service.py` | Cálculo de métricas y ganancias |
| `services/stock_service.py` | Registro de compras de mercadería |
| `services/email_service.py` | Envío de emails (bienvenida, recuperación, cambio de contraseña) |
| `services/admin_manager.py` | Decoradores de seguridad para rutas admin |
| `static/css/index.css` | Archivo maestro que importa todos los CSS |
| `static/css/11-mobile.css` | Todos los estilos responsive para mobile |
| `templates/` | Todas las páginas HTML del sistema |

---

*Documentación generada para el proyecto Full Gaming — Febrero 2026*
