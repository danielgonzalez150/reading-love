"""
Modulo del CRUD para los libros.
"""

# Importamos el objeto cliente de supabase
from database.client import supabase

def get_featured_books(limit_count: int = 6):
    """
    Trae libros activos para la página principal.

    Entrada:
        - limit_count: La cantidad de libros (6 por defecto).

    Retorna:
        - Una lista de diccionarios con los datos de los libros
    """
    try:
        # Intenta obtener el id, titulo, precio, año y stock del libro SOLO si están activos
        response = (
            supabase.table("libros")
            .select("id_libro, titulo, precio, ano_publicacion, stock") # Solo lo necesario
            .eq("activo", True) # Filtro de seguridad
            .limit(limit_count)
            .execute()
        )

        # Retorna los datos
        return response.data
    
    # Si algo sale mal, retornar una lista vacía
    except Exception as e:
        print(f"Error al obtener libros: {e}")
        return []