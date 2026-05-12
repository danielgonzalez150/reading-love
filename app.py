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
# JDMC 20260511: funciones para detalles del libro y procesamiento de compras
from database.book_repository import get_featured_books, get_book_details, create_purchase, get_purchase_history

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

# ===== ENDPOINTS PARA MODAL DE DETALLES Y COMPRA - JDMC 20260511 =====
# GET /api/libro/{book_id}: retorna detalles completos del libro en JSON
# POST /api/compra: procesa la transacción de compra y actualiza stock

@app.get("/api/libro/{book_id}")
async def get_libro_detalle(book_id: int, session_token: str = Cookie(None)):
    """
    Endpoint que obtiene los detalles completos de un libro (JSON).
    
    Entrada:
        - book_id: ID del libro
    
    Retorna:
        - JSON con los detalles del libro o error 404
    """
    if not session_token:
        return {"error": "No autenticado"}
    
    libro = get_book_details(book_id)
    
    if not libro:
        return {"error": "Libro no encontrado"}
    
    return libro

@app.post("/api/compra")
async def realizar_compra(
    book_id: int = Form(...),
    cantidad: int = Form(...),
    session_token: str = Cookie(None)
):
    """
    Endpoint para procesar una compra.
    
    Entrada:
        - book_id: ID del libro a comprar
        - cantidad: Cantidad de libros a comprar
    
    Retorna:
        - JSON con el resultado de la transacción
    """
    if not session_token:
        return {"error": "No autenticado", "success": False, "details": "No hay token de sesión"}
    
    from database.client import supabase
    
    try:
        # Obtener el usuario actual desde el token
        user = supabase.auth.get_user(session_token)
        user_id = user.user.id if user and user.user else None
        
        if not user_id:
            return {"error": "Usuario no válido", "success": False, "details": "No se pudo obtener el ID del usuario del token"}
        
        print(f"[COMPRA] User ID: {user_id}, Book ID: {book_id}, Cantidad: {cantidad}")
        
        # Procesar la compra
        resultado = create_purchase(user_id, book_id, cantidad)
        
        if resultado:
            print(f"[COMPRA EXITOSA] Transacción ID: {resultado.get('id_transaccion')}, Total: {resultado.get('total')}")
            return {
                "success": True,
                "mensaje": "¡Compra realizada exitosamente!",
                "transaccion_id": resultado.get("id_transaccion"),
                "total": resultado.get("total")
            }
        else:
            print(f"[ERROR COMPRA] create_purchase retornó None")
            return {"error": "No se pudo procesar la compra", "success": False, "details": "La función create_purchase no retornó datos válidos"}
    
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR ENDPOINT COMPRA] {error_msg}")
        import traceback
        traceback.print_exc()
        return {
            "error": "Error al procesar la compra",
            "success": False,
            "details": error_msg
        }


@app.get("/api/historial-compras")
async def historial_compras(session_token: str = Cookie(None)):
    """
    Endpoint para obtener el historial de compras del usuario autenticado.
    """
    if not session_token:
        return {"success": False, "error": "No autenticado", "details": "No hay token de sesión"}

    from database.client import supabase

    try:
        user = supabase.auth.get_user(session_token)
        user_id = user.user.id if user and user.user else None

        if not user_id:
            return {
                "success": False,
                "error": "Usuario no válido",
                "details": "No se pudo obtener el ID del usuario del token"
            }

        historial = get_purchase_history(user_id)
        return {"success": True, "historial": historial}

    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR HISTORIAL] {error_msg}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": "Error al obtener historial",
            "details": error_msg
        }