# Importamos el objeto de supabase Client
from database.client import supabase

def register_new_user(email, password):
    """
    Función que usa las funciones del objeto supabase para registrar un usuario.

    Entrada
        - email: Correo único del usuario
        - password: La contraseña hasheada del usuario.

    Retorna
        - Una respuesta propia de supabase (201 si se creó el usuario,
        código de error si no se pudo crear)
    """
    response = supabase.auth.sign_up({
        "email": email,
        "password": password,
    })
    return response