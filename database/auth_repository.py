# Importamos el objeto de supabase Client
from database.client import supabase

def register_new_user(email, password, nombre, apellido, telefono):
    """
    Función que usa las funciones del objeto supabase para registrar un usuario.

    Entrada
        - email: Correo único del usuario
        - password: La contraseña hasheada del usuario.

    Retorna
        - Una respuesta propia de supabase (201 si se creó el usuario,
        código de error si no se pudo crear)
    """
    try:
        # Intentamos logear en la tabla privada
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        # Si sale bien, insertamos los datos en la tabla de clientes
        if auth_response.user:
            user_id = auth_response.user.id # El UUID que generó Supabase
            
            # Insertamos en tu tabla pública 'clientes'
            supabase.table("clientes").insert({
                "id_cliente": user_id, # Usamos el mismo ID de Auth para vincularlos
                "nombre": nombre,
                "apellido": apellido,
                "telefono": telefono
            }).execute()

        return auth_response
    
    # Si hay algún error
    except Exception as e:
        # Imprimimos el error
        print(f"Error en el registro: {e}")

        # Retornamos none para que se sepa que no funcionó
        return None