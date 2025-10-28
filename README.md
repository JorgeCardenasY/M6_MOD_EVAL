# Gestor de Tareas - Documentación del Proyecto

## Introducción

Este documento detalla el desarrollo de la aplicación web "Gestor de Tareas", un sistema diseñado para permitir a los usuarios gestionar sus tareas personales. La aplicación se ha construido utilizando el framework Django, siguiendo una serie de requerimientos específicos que abarcan desde la configuración inicial del proyecto hasta la implementación de funcionalidades clave como la autenticación de usuarios y la gestión de tareas.

A continuación, se presenta una explicación formal y en tercera persona del proceso de desarrollo, abordando cada uno de los requerimientos solicitados.

---

## Parte 1: Configuración Inicial

### Creación del Proyecto y la Aplicación

El desarrollo comenzó con la inicialización de un nuevo proyecto Django denominado `gestor_tareas`. Para ello, se utilizó el comando `django-admin startproject gestor_tareas`, que genera la estructura de directorios y ficheros base necesaria para cualquier proyecto Django.

Posteriormente, dentro del directorio del proyecto, se procedió a crear la aplicación principal, `tareas`, mediante el comando `python manage.py startapp tareas`. Esta aplicación encapsula toda la lógica de negocio relacionada con la gestión de tareas, incluyendo modelos, vistas, formularios y plantillas.

### Configuración del Proyecto

Para que el proyecto Django reconozca y pueda utilizar la aplicación `tareas`, fue necesario registrarla en el fichero de configuración `settings.py`. Se añadió `'tareas'` a la lista `INSTALLED_APPS`, asegurando así su correcta integración en el ecosistema del proyecto.

```python
# gestor_tareas/settings.py

INSTALLED_APPS = [
    # ...
    'tareas',
]
```

### Configuración de URLs

La gestión de las rutas de la aplicación se ha modularizado para mantener el código organizado y escalable. En el fichero `gestor_tareas/urls.py` (el `URLconf` raíz), se incluyó una referencia al fichero de URLs de la aplicación `tareas` utilizando la función `include()`:

```python
# gestor_tareas/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tareas.urls')),
]
```

Dentro de la aplicación `tareas`, se creó un fichero `urls.py` para definir las rutas específicas de la misma, asociando cada URL con su vista correspondiente.

---

## Parte 2: Vistas y Plantillas

### Gestión de Tareas en Memoria (Adaptación a Base de Datos)

Aunque el requerimiento inicial especificaba el manejo de tareas en memoria, se optó por una implementación más robusta y persistente utilizando la base de datos SQLite3, que viene configurada por defecto en Django. Esto se logró a través de la definición de un modelo `Tarea`, lo que permite una gestión de datos más fiable y escalable.

### Vistas para el CRUD de Tareas

Se implementaron las siguientes vistas basadas en funciones para manejar el ciclo de vida de las tareas (CRUD: Create, Read, Update, Delete):

-   **`lista_tareas(request)`**: Protegida con el decorador `@login_required`, esta vista recupera y muestra únicamente las tareas pertenecientes al usuario autenticado.
-   **`tarea_detail(request, tarea_id)`**: Permite visualizar los detalles de una tarea específica, asegurando que solo el usuario propietario pueda acceder a ella.
-   **`crear_tarea(request)`**: Gestiona la creación de nuevas tareas a través de un formulario de Django. Asocia automáticamente la nueva tarea con el usuario que ha iniciado sesión.
-   **`eliminar_tarea(request, tarea_id)`**: Permite a un usuario eliminar una de sus propias tareas.
-   **`completar_tarea(request, tarea_id)`**: Marca una tarea como completada.

### Formularios de Django

Para la creación de tareas, se utilizó la clase `forms.ModelForm` de Django, que facilita la creación de formularios a partir de un modelo existente. El formulario `TareaForm` se definió en el fichero `tareas/forms.py`, especificando los campos `titulo` y `descripcion`.

```python
# tareas/forms.py

from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion']
```

### Plantillas y Diseño con Bootstrap

La interfaz de usuario se ha diseñado utilizando **Bootstrap 5**, lo que garantiza una apariencia moderna y responsiva. Se ha seguido el principio DRY (Don't Repeat Yourself) mediante el uso de un sistema de plantillas de Django:

-   **`base.html`**: Plantilla principal que define la estructura común de la página, incluyendo la barra de navegación y el pie de página.
-   **`navbar.html` y `footer.html`**: Componentes reutilizables incluidos en `base.html`.
-   **`lista_tareas.html`**: Muestra la lista de tareas del usuario.
-   **`tarea_detail.html`**: Presenta los detalles de una tarea individual.
-   **`tareas.html`**: Contiene el formulario para agregar nuevas tareas.

---

## Parte 3: Autenticación y Seguridad

### Sistema de Autenticación de Django

Se ha implementado un sistema completo de autenticación de usuarios utilizando el módulo `django.contrib.auth`. Se crearon las siguientes vistas para gestionar el ciclo de vida del usuario:

-   **`registro_usuario(request)`**: Permite a los nuevos usuarios crear una cuenta. Utiliza el formulario `UserCreationForm` de Django.
-   **`iniciar_sesion(request)`**: Gestiona el inicio de sesión de los usuarios existentes mediante el `AuthenticationForm`.
-   **`cerrar_sesion(request)`**: Cierra la sesión del usuario actual.

### Protección de Vistas

La seguridad de la aplicación se ha reforzado para garantizar que solo los usuarios autenticados puedan acceder a las funcionalidades de gestión de tareas. Esto se ha logrado mediante:

-   **Decorador `@login_required`**: Se ha aplicado a todas las vistas de tareas para redirigir a los usuarios no autenticados a la página de inicio de sesión.
-   **Filtrado por Usuario**: En las vistas `lista_tareas`, `tarea_detail`, `eliminar_tarea` y `completar_tarea`, las consultas a la base de datos se filtran por el usuario autenticado (`request.user`). Esto previene que un usuario pueda ver o modificar las tareas de otro.

---

## Parte 4: Despliegue y Pruebas

### Pruebas de Funcionalidad

Se han realizado pruebas manuales exhaustivas para verificar el correcto funcionamiento de todas las características implementadas:

-   **Autenticación**: Se ha comprobado que el registro, inicio de sesión y cierre de sesión funcionan como se esperaba.
-   **Gestión de Tareas**: Se ha verificado que los usuarios pueden crear, ver, completar y eliminar sus propias tareas.
-   **Seguridad**: Se ha confirmado que un usuario no puede acceder a las tareas de otro a través de la manipulación de URLs.

### Configuración para Producción

Para un eventual despliegue en un entorno de producción, se han ajustado las siguientes configuraciones en `settings.py`:

-   **`DEBUG`**: Se ha establecido en `False` para desactivar los mensajes de depuración detallados.
-   **`ALLOWED_HOSTS`**: Se ha configurado para permitir únicamente las peticiones desde los dominios autorizados.
-   **`SECRET_KEY`**: Se ha generado una clave secreta única y se ha mantenido fuera del control de versiones en un entorno de producción real.

---

## Parte 5: Entrega

### Estructura del Proyecto

El proyecto se organiza de la siguiente manera:

-   **`gestor_tareas/`**: Directorio raíz del proyecto Django.
    -   **`gestor_tareas/`**: Contiene la configuración principal del proyecto (`settings.py`, `urls.py`).
    -   **`tareas/`**: Aplicación de Django que contiene la lógica de negocio.
        -   `models.py`: Define los modelos de la base de datos.
        -   `views.py`: Contiene las vistas que procesan las peticiones HTTP.
        -   `forms.py`: Define los formularios de Django.
        -   `urls.py`: Define las rutas de la aplicación.
        -   `templates/`: Contiene las plantillas HTML.
    -   `manage.py`: Script de utilidad para la gestión del proyecto.
    -   `db.sqlite3`: Base de datos SQLite.

### Cómo Ejecutar el Proyecto

Para ejecutar el proyecto en un entorno de desarrollo local, siga los siguientes pasos:

1.  **Clonar el Repositorio**:
    ```bash
    git clone <url-del-repositorio>
    cd gestor_tareas
    ```

2.  **Crear y Activar un Entorno Virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar las Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar las Migraciones**:
    ```bash
    python manage.py migrate
    ```

5.  **Crear un Superusuario** (opcional, para acceder al panel de administración):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Ejecutar el Servidor de Desarrollo**:
    ```bash
    python manage.py runserver
    ```

La aplicación estará disponible en `http://127.0.0.1:8000/`.
