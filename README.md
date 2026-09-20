#  Sistema de Gestión "Inventario Colegio"

Proyecto final Full-Stack (EPE 3) desarrollado para optimizar y automatizar el control de insumos de un establecimiento educacional. El sistema reemplaza los registros manuales por una plataforma web centralizada con validaciones de reglas de negocio en tiempo real.

## Tecnologías Utilizadas
* **Back-End:** Python, Django (ORM, Vistas, Validaciones transaccionales).
* **Base de Datos:** SQLite (Base de datos poblada masivamente mediante script automatizado).
* **Front-End:** HTML5, CSS3, Vanilla JavaScript (DOM Manipulation).
* **Integración:** Arquitectura asíncrona mediante Fetch API y formato JSON.

##  Funcionalidades Principales
1. **Control Transaccional:** Registro de 'Entradas' y 'Salidas' con actualización de stock automatizada.
2. **Validación de Integridad:** El Back-End impide retiros que superen el stock actual (Error 400).
3. **Buscador Asíncrono:** Motor de filtrado en tiempo real en el Front-End (sin recargar la página).
4. **Base de Datos en Producción:** El sistema incluye un inventario pre-cargado con múltiples categorías (Mobiliario, Tecnología, Laboratorio, etc.) listo para su evaluación.

##  Instrucciones de Ejecución para el Evaluador
Para probar este proyecto localmente, no es necesario realizar migraciones ni crear datos, ya que la base de datos `db.sqlite3` viene configurada y poblada.

1. Clonar este repositorio.
2. Abrir la terminal en la carpeta del proyecto.
3. Ejecutar el servidor de desarrollo de Django:
   `python manage.py runserver`
4. Abrir un navegador web e ingresar a `http://127.0.0.1:8000/`

**Autor:** Juan Daniel Segura Huerta
