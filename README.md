# Full Gaming

**Full Gaming** es un e-commerce con el objetivo de la venta de hardware y software de computación.

## Tecnologías

- Python
- MySQL
- Flask
- Bootstrap

## Dependencias

Todas las dependencias necesarias para ejecutar el proyecto están listadas en el archivo `requirements.txt`.  
Para instalarlas, ejecuta:

# Activar tu entorno virtual si aún no lo hiciste

python -m venv .venv
.venv\Scripts\Activate.ps1

# Instalar dependencias

pip install -r requirements.txt

## Configuración de la base de datos

En el archivo `database.py` cada usuario debe modificar:

- `database` → el nombre de su base de datos local
- `password` → su contraseña local de MySQL

No se suben credenciales al repositorio por seguridad.

## Ejecutar el proyecto

El script principal para correr la aplicación es:

python app.py

## Clonar el proyecto

Para trabajar con el proyecto, tus compañeros pueden clonar el repositorio:

git clone https://github.com/gonzasp06/Full_Gaming.git
cd Full_Gaming

Luego deben crear su entorno virtual, instalar dependencias y configurar `database.py` como se indica arriba.

## 📚 Documentación del Sistema

Se ha creado documentación completa del sistema para facilitar su comprensión y estudio:

### Documentos Disponibles

1. **[RESUMEN_PARA_EXAMEN.md](RESUMEN_PARA_EXAMEN.md)** - ⭐ **EMPIEZA AQUÍ**
   - Resumen ejecutivo en 5 minutos
   - Los conceptos más importantes
   - Preguntas típicas de examen con respuestas
   - Checklist de preparación
   - Puntos para destacar al profesor

2. **[DOCUMENTACION_SISTEMA.md](DOCUMENTACION_SISTEMA.md)** - Documentación completa y detallada
   - Arquitectura general del proyecto
   - Estructura de base de datos
   - Explicación de todos los servicios y clases
   - Flujos de usuario y administrador
   - Sistema de autenticación y seguridad
   - Sistema de carrito de compras
   - Conceptos clave y preguntas frecuentes

3. **[GUIA_RAPIDA_EXAMEN.md](GUIA_RAPIDA_EXAMEN.md)** - Guía rápida de referencia
   - Respuestas a preguntas comunes
   - Explicaciones concisas de cada funcionalidad
   - Diagramas de flujo simplificados
   - Comandos útiles
   - Solución de errores comunes

4. **[EJEMPLOS_PRACTICOS.md](EJEMPLOS_PRACTICOS.md)** - Ejemplos prácticos con código
   - Código comentado línea por línea
   - Casos de uso reales completos
   - Debugging y troubleshooting
   - Consultas SQL generadas por el sistema
   - Interacción frontend-backend

5. **[DIAGRAMAS_VISUALES.md](DIAGRAMAS_VISUALES.md)** - Diagramas y visualizaciones
   - Arquitectura del sistema en diagramas ASCII
   - Flujo de datos completo
   - Estructura de base de datos visual
   - Flujos de autenticación y compra
   - Organización de archivos

### ¿Para qué sirve esta documentación?

- **Estudiar para exámenes**: Explicaciones detalladas de cómo funciona cada componente
- **Incorporar nuevos desarrolladores**: Entender rápidamente la arquitectura
- **Resolver problemas**: Ejemplos de debugging y soluciones
- **Referencia técnica**: Consultar cómo se implementan funcionalidades específicas

## Colaboración

- Hacer commits claros al trabajar en nuevas funciones o arreglos.
- Hacer `push` a la rama principal o crear ramas nuevas si trabajan en features específicas.
