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

# Importar la función de registrar usuario
from database.auth_repository import register_new_user

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