# Catálogo Web

Este es un proyecto de catálogo web desarrollado como parte de la materia de Práctica Profesionalizante 3 de la carrera de Tecnicatura Superior en Desarrollo de Software en la institución I.E.S 9012 "San Rafael Informática".

## Descripción

Este proyecto de catálogo web permite cargar productos con descripciones, cantidades, precios, categorías e imágenes. Los usuarios pueden filtrar los productos por categorías y navegar por las páginas, mostrando 10 productos por página.

## Características

- **Carga de Productos**: Permite agregar nuevos productos al catálogo con detalles como descripción, cantidad, precio, categorías e imagen.
- **Filtros por Categorías**: Los usuarios pueden filtrar los productos según diferentes categorías para encontrar fácilmente lo que están buscando.
- **Paginación**: Los productos se muestran en páginas, con 10 productos por página, para facilitar la navegación.

## Tecnologías Utilizadas

- **Python**: El lenguaje de programación principal utilizado para el backend y la lógica del negocio.
- **HTML**: Para la estructura de las páginas web.
- **CSS**: Para estilizar y diseñar las páginas.
- **Bootstrap**: Se utilizó para facilitar el diseño y hacer que el sitio web sea responsivo.
- **Flask**: Un framework de Python utilizado para desarrollar la aplicación web.
- **MySQL**: Una base de datos relacional utilizada para almacenar la información de los productos y categorías.

## Instalación

1. Clona este repositorio en tu máquina local utilizando Git:

   ```
   git clone https://github.com/tu_usuario/nombre_del_repositorio.git
   ```

2. Instala las dependencias del proyecto. Asegúrate de tener Python y pip instalados. Luego, ejecuta:

   ```
   pip install -r requirements.txt
   ```

3. Configura la base de datos MySQL. Asegúrate de tener un servidor MySQL instalado y configurado. Luego, crea una nueva base de datos y actualiza la configuración de la conexión en el archivo `config.py`.

4. Ejecuta la aplicación:

   ```
   python app.py
   ```

5. Abre tu navegador web y visita `http://localhost:5000` para ver la aplicación en acción.
