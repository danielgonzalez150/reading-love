"""
Módulo principal

Aquí se manejará toda la API que conecta el Frontend con la base de datos.
"""
# Obtener el objeto FastAPI, Request para enviar, y Form para recibir datos
from fastapi import FastAPI, Request, Form, Response, Cookie, Depends, status

# Importar los templates de Jinja para mostrar el HTML
from fastapi.templating import Jinja2Templates

# Importar el objeto de respuesta HTML para mostrar el HTML
from fastapi.responses import HTMLResponse, RedirectResponse

# Importar el montaje de archivos estáticos jdmc
from fastapi.staticfiles import StaticFiles

# Importar el CRUD del usuario (Registro y logeo)
from database.auth_repository import register_new_user, login_user

# Importar el CRUD de los libros
from database.book_repository import get_featured_books

# Creamos el objeto de FastAPI y el objeto de plantilas
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Montar la carpeta de archivos estáticos (CSS, JS, imágenes) jdmc
app.mount("/static", StaticFiles(directory="static"), name="static")

async def verificar_sesion(session_token: str = Cookie(None)):
    """
    Si no hay token en las cookies, redirige al login.
    """
    if not session_token:
        # Aquí puedes lanzar un error o redirigir
        return RedirectResponse(url="/login", status_code=303)
    
    # Opcional: Podrías validar el token con supabase.auth.get_user(session_token)
    return session_token

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session_token: str = Cookie(None)):
    """
    Método GET para obtener el índice
    """
    # El "Freno": Si no hay cookie, mandamos la redirección de una vez
    if not session_token:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # Si hay cookie, el código sigue normal
    lista_libros = get_featured_books(10)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "libros": lista_libros
    })

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    """
    Método GET para renderizar la plantilla de registro
    """
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/auth/register")
async def post_register(
    request: Request, 
    email: str = Form(...), 
    password: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: str = Form(...)
):
    """
    Función que registra un usuario mediante los datos del Front y muestra una
    plantilla de éxito o de fracaso.

    Entrada:
        - email del usuario
        - contraseña del usuario
    
    Retorna:
        - La plantilla de registro con el mensaje de error o éxito.
    """

    # Llamar la función
    resultado = register_new_user(email, password, nombre, apellido, telefono)
    
    # Checar que no sea nulo
    if resultado is not None:
        mensaje = "¡Registro exitoso! Ya puedes iniciar sesión."
    else:
        mensaje = "Hubo un error al intentar registrarte."
        
    # Retornar la plantilla con el mensaje
    return templates.TemplateResponse("register.html", {
        "request": request, 
        "mensaje": mensaje
    })

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    """
    Función para renderizar la página de login.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/auth/login")
async def post_login(request: Request, email: str = Form(...), password: str = Form(...)):
    """
    Método POST para realizar el login del usuario.

    Entrada:
        - emaiL: Correo del usuario del formulario.
        - password: Contraseña del usuario del usuario

    Retorna:
        - Renderiza el template del index sí se logea exitosamente, sino
        renderiza nuevamente el login.

    """
    # LLamar a la función CRUD para el logeo
    resultado = login_user(email, password)
    
    if resultado and resultado.session:
        # 1. Creamos la respuesta de redirección al índice ("/")
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
        # 2. Le pegamos la cookie a esa misma respuesta
        response.set_cookie(
            key="session_token", 
            value=resultado.session.access_token, 
            httponly=True,
            max_age=3600 # La sesión dura 1 hora
        )
        return response
    
    # Si falla, lo mandamos de vuelta al login con un mensaje
    return templates.TemplateResponse("login.html", {
        "request": request, # Necesario para Jinja2
        "mensaje": "Correo o contraseña incorrectos"
    })