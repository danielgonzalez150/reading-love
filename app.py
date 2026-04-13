"""
Módulo principal

Aquí se manejará toda la API que conecta el Frontend con la base de datos.
"""
# Obtener el objeto FastAPI, Request para enviar, y Form para recibir datos
from fastapi import FastAPI, Request, Form

# Importar los templates de Jinja para mostrar el HTML
from fastapi.templating import Jinja2Templates

# Importar el objeto de respuesta HTML para mostrar el HTML
from fastapi.responses import HTMLResponse

# Importar el CRUD del usuario (Registro y logeo)
from database.auth_repository import register_new_user, login_user

# Creamos el objeto de FastAPI y el objeto de plantilas
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    """
    Función para renderizar la plantilla de registro
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
    
    # Checar que haya resultado y que sea un usuario válido
    if resultado is not None and resultado.user is not None:
        # Aquí luego guardaremos la sesión, por ahora solo confirmamos
        return {"status": "success", "message": f"Bienvenido {resultado.user.email}"}
    else:
        # Mostrar nuevamente el login en caso de error
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "mensaje": "Credenciales incorrectas o correo no confirmado."
        })