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

## Colaboración

- Hacer commits claros al trabajar en nuevas funciones o arreglos.
- Hacer `push` a la rama principal o crear ramas nuevas si trabajan en features específicas.
