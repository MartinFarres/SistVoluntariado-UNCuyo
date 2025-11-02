# Sistema de Gestión de Voluntariado - UNCuyo

Este repositorio contiene el código fuente del Sistema de Gestión de Voluntariado de la UNCuyo, una aplicación full-stack diseñada para conectar, administrar y coordinar a voluntarios, organizaciones y programas de voluntariado.

El sistema se divide en dos componentes principales:
* `voluntariados-backend`: Una API RESTful construida con Django y Django REST Framework.
* `voluntariados-frontend`: Una Aplicación de Página Única (SPA) construida con Vue.js 3 y Vite.

---

## ✨ Características Principales

Este sistema provee una plataforma integral para los tres roles de usuario principales:

* **Para Voluntarios:**
    * Creación de perfiles y gestión de datos personales.
    * Exploración de programas de voluntariado disponibles.
    * Postulación a convocatorias de voluntariado.
    * Inscripción a turnos (horarios) específicos una vez aceptados.
    * Seguimiento de horas y asistencias.
    * Descarga de certificados de participación.

* **Para Gestionadores (Delegados de Organizaciones):**
    * Gestión del perfil de la organización.
    * Creación y administración de programas de voluntariado.
    * Definición de etapas (convocatoria, cursado) y cupos.
    * Revisión, aceptación o rechazo de postulaciones de voluntarios.
    * Creación y gestión de turnos.
    * Registro de asistencia de los voluntarios a los turnos.

* **Para Administradores del Sitio:**
    * Dashboard general con estadísticas.
    * Gestión completa de usuarios, roles y permisos.
    * Administración de todas las organizaciones y programas de voluntariado.
    * Gestión de datos maestros (facultades, carreras, ubicaciones, etc.).

## 🛠️ Stack Tecnológico

* **Backend:**
    * [Python](https://www.python.org/)
    * [Django](https://www.djangoproject.com/)
    * [Django REST Framework](https://www.django-rest-framework.org/)
    * [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) (para autenticación)
    * [PostgreSQL](https://www.postgresql.org/) (Recomendado para producción)
    * [Docker](https://www.docker.com/) (Soportado para despliegue)

* **Frontend:**
    * [Vue.js 3](https://vuejs.org/)
    * [Vite](https://vitejs.dev/)
    * [TypeScript](https://www.typescriptlang.org/)
    * [Vue Router](https://router.vuejs.org/) (para enrutamiento)
    * (Probablemente Pinia o Vuex para manejo de estado)
    * (Probablemente Tailwind CSS o similar para estilos)

---

## 🚀 Puesta en Marcha (Entorno de Desarrollo)

Para ejecutar el proyecto localmente, necesitarás levantar el backend y el frontend por separado en dos terminales distintas.

### 1. Backend (Django API)

1.  Navega al directorio del backend:
    ```bash
    cd voluntariados-backend
    ```

2.  (Recomendado) Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    # En macOS/Linux
    source venv/bin/activate
    # En Windows
    # venv\Scripts\activate
    ```

3.  Instala las dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```

4.  Copia el archivo de variables de entorno de ejemplo:
    ```bash
    cp .env.example .env
    ```

5.  Edita el archivo `.env` y configura tus variables, especialmente la base de datos (`DATABASE_URL`). Por defecto, usará SQLite si se deja en blanco.

6.  Ejecuta las migraciones para crear la estructura de la base de datos:
    ```bash
    python manage.py migrate
    ```

7.  (Opcional) Carga datos iniciales o crea un superusuario:
    ```bash
    python manage.py createsuperuser
    ```

8.  Inicia el servidor de desarrollo del backend:
    ```bash
    python manage.py runserver
    ```
    La API estará disponible en `http://127.0.0.1:8000`.

### 2. Frontend (Vue.js App)

1.  Abre una **nueva terminal** y navega al directorio del frontend:
    ```bash
    cd voluntariados-frontend
    ```

2.  Instala las dependencias de Node.js:
    ```bash
    npm install
    ```

3.  Copia el archivo de variables de entorno de ejemplo:
    ```bash
    cp .env.example .env
    ```

4.  Edita el archivo `.env` y asegúrate de que `VITE_API_URL` apunte a tu servidor backend:
    ```
    VITE_API_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
    ```

5.  Inicia el servidor de desarrollo de Vite:
    ```bash
    npm run dev
    ```
    La aplicación web estará disponible en `http://localhost:5173` (o el puerto que indique Vite).

---

## 🐳 Despliegue con Docker

El directorio `voluntariados-backend` incluye un `docker-compose.yml` y `dockerfile` para facilitar el despliegue. Consulta el `README.md` dentro de ese directorio para instrucciones específicas de Docker.

## 📄 Licencia

Este proyecto está distribuido bajo la Licencia MIT.
