# 📖 Reading Love - Plataforma de Gestión Literaria

Reading Love es una aplicación web diseñada para conectar a lectores con sus obras favoritas. El proyecto se enfoca en ofrecer una experiencia fluida de exploración de catálogos, gestión de inventarios y seguridad de usuarios, integrando tecnologías modernas de desarrollo backend.

## 🚀 Objetivo del Proyecto

Desarrollar un sistema integral de librería que permita:

- **Autenticación Segura:** Registro e inicio de sesión de usuarios mediante Supabase Auth.

- **Catálogo Dinámico:** Visualización de libros reales con detalles técnicos (ISBN, Autor, Precio, Stock).

- **Gestión de Datos:** Arquitectura relacional para manejar autores, géneros y editoriales.

- **Experiencia de Usuario (UX):** Interfaz limpia y responsiva utilizando FastAPI y Jinja2.

## 🛠️ Stack Tecnológico

- **Backend:** FastAPI (Python 3.10+)

- **Base de Datos & Auth:** Supabase (PostgreSQL)

- **Frontend:** HTML5, Jinja2 Templates y Pico.css (para un diseño minimalista).

- **Control de Versiones:** Git & GitHub.

## 📂 Estructura del Repositorio

```
ReadingLove/
├── database/           # Lógica de conexión y repositorios (CRUD)
│   ├── client.py       # Conexión con Supabase
│   ├── auth_repository.py # Lógica de Registro/Login
│   └── book_repository.py # Consultas de libros
├── static/             # Archivos estáticos (CSS, JS, Imágenes)
├── templates/          # Plantillas HTML (Jinja2)
├── app.py              # Punto de entrada de la aplicación (FastAPI)
└── requirements.txt    # Dependencias del proyecto
```

## 🔑 Funcionalidades Implementadas

- **Seguridad por Cookies:** Protección de rutas mediante session_token. Si un usuario no está logueado, es redirigido automáticamente al login.

- **Relaciones Muchos a Muchos:** Implementación de tablas intermedias para vincular libros con múltiples géneros.

- **Inyección de Datos Reales:** Base de datos poblada con autores y títulos clásicos para una demostración realista.

- **Manejo de Estáticos:** Carpeta configurada para servir estilos personalizados y portadas.

## 🛠️ Instalación y Uso

**1- Clonar el repositorio:**

```
git clone https://github.com/danielgonzalez150/reading-love.git
```

**2- Instalar dependencias:**

```
pip install -r requirements.txt
```

**3- Configurar variables de entorno:**

Crea un archivo .env con tus credenciales de Supabase (SUPABASE_URL y SUPABASE_KEY).

**4- Correr el servidor:**

```
uvicorn app:app --reload
```

## 📷 Imagenes

**1- Base de datos:**

<img width="1256" height="782" alt="image" src="https://github.com/user-attachments/assets/78662a13-6712-4ba4-a43a-4339704676a1" />

## 👥 Colaboradores

Daniel Mitchell González Henao 

Paul Bryan Orrego Calderón

Jose David Montero Cardona
