"""
Modulo del CRUD para los libros.
"""

# Importamos el objeto cliente de supabase
from database.client import supabase
from datetime import datetime

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

# ===== FUNCIONES PARA MODAL DE DETALLES Y COMPRA - JDMC 20260511 =====
# get_book_details: obtiene info completa del libro (autor, editorial, descripción)
# create_purchase: procesa compra, valida stock y genera transacción

def get_book_details(book_id: int):
    """
    Obtiene los detalles completos de un libro con información del autor y editorial.

    Entrada:
        - book_id: El ID del libro.

    Retorna:
        - Un diccionario con los detalles del libro (título, descripción, precio, stock, autor, editorial, etc.)
    """
    try:
        # Obtener datos del libro con join a autores y editoriales
        response = (
            supabase.table("libros")
            .select(
                "id_libro, titulo, descripcion_libro, precio, ano_publicacion, stock, "
                "id_autor, id_editorial, "
                "autores(nombre), "
                "editoriales(nombre)"
            )
            .eq("id_libro", book_id)
            .eq("activo", True)
            .single()
            .execute()
        )

        return response.data
    
    except Exception as e:
        print(f"Error al obtener detalles del libro {book_id}: {e}")
        return None

def get_book_by_name(book_name: str):
    """
    Busca libros en la base de datos de Supabase que coincidan 
    o contengan el nombre proporcionado (Case-Insensitive).
    
    Parámetros:
    - supabase_client: El objeto cliente de Supabase ya inicializado.
    - book_name: El string con el nombre o parte del nombre del libro.
    
    Retorna:
    - Una lista con los libros encontrados o una lista vacía si no hay coincidencias.
    """
    try:
        # Usamos '%' antes y después para que busque coincidencias parciales (ej. "amor" encuentra "El amor en los tiempos del cólera")
        search_pattern = f"%{book_name}%"
        
        response = (
            supabase.table("libros")
            .select("id_libro, titulo, precio, ano_publicacion, stock")
            .ilike("titulo", search_pattern)
            .eq("activo", True)  # Asegúrate de que tu columna se llame 'nombre' o 'titulo'
            .execute()
        )
        
        # .execute() devuelve un objeto que contiene el atributo 'data' con la lista de registros
        return response.data

    except Exception as e:
        print(f"Error al buscar el libro: {e}")
        return []
    
def create_purchase(user_id: str, book_id: int, cantidad: int):
    """
    Crea transacción con detalles. Inserta en transacciones y detalle_transaccion.
    """
    try:
        print(f"[CP] INICIO: User={user_id}, Book={book_id}, Qty={cantidad}")
        
        # Step 1: Get book details
        print(f"[CP] Step 1: Fetching book data...")
        libro_response = supabase.table("libros").select("precio, stock").eq("id_libro", book_id).single().execute()
        print(f"[CP] Libro response: {libro_response}")
        
        if not libro_response.data:
            print(f"[CP] ERROR Step 1: No book data found")
            return None

        libro = libro_response.data
        precio = libro.get("precio", 0)
        stock = libro.get("stock", 0)
        print(f"[CP] Step 1 OK: precio={precio}, stock={stock}")
        
        # Step 2: Validate stock
        if stock < cantidad:
            print(f"[CP] ERROR Step 2: Stock insuficiente ({stock} < {cantidad})")
            return None
        print(f"[CP] Step 2 OK: Stock validado")

        # Step 3: Calculate total
        total = precio * cantidad
        print(f"[CP] Step 3 OK: total={total}")
        
        # Step 4: Insert transaction
        print(f"[CP] Step 4: Inserting transacción...")
        tx_response = supabase.table("transacciones").insert({
            "id_cliente": user_id, 
            "fecha": datetime.now().isoformat(), 
            "total": total
        }).execute()
        print(f"[CP] TX response: {tx_response}")
        
        if not tx_response.data or len(tx_response.data) == 0:
            print(f"[CP] ERROR Step 4: No transaction data")
            return None

        tx = tx_response.data[0]
        id_tx = tx.get("id_transaccion")
        print(f"[CP] Step 4 OK: id_transaccion={id_tx}")
        
        # Step 5: Insert detail
        print(f"[CP] Step 5: Inserting detalle_transaccion...")
        detail_response = supabase.table("detalle_transaccion").insert({
            "id_transaccion": id_tx, 
            "id_libro": book_id, 
            "cantidad": cantidad, 
            "precio_unitario": precio
        }).execute()
        print(f"[CP] Detail response: {detail_response}")
        
        if not detail_response.data or len(detail_response.data) == 0:
            print(f"[CP] ERROR Step 5: No detail data")
            return None
        print(f"[CP] Step 5 OK: detalle created")

        # Step 6: Update stock
        print(f"[CP] Step 6: Updating stock...")
        update_response = supabase.table("libros").update({"stock": stock - cantidad}).eq("id_libro", book_id).execute()
        print(f"[CP] Update response: {update_response}")
        print(f"[CP] Step 6 OK: stock updated to {stock - cantidad}")
        
        print(f"[CP] ✅ SUCCESS: TX={id_tx}")
        return tx

    except Exception as e:
        print(f"[CP] ❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_purchase_history(user_id: str):
    """
    Obtiene el historial de compras de un usuario específico.

    Retorna una lista con transacciones y sus ítems:
    [
        {
            "id_transaccion": int,
            "fecha": str,
            "total": number,
            "items": [
                {
                    "id_libro": int,
                    "titulo": str,
                    "cantidad": int,
                    "precio_unitario": number,
                    "subtotal": number
                }
            ]
        }
    ]
    """
    try:
        print(f"[HISTORIAL] Consultando compras para user_id={user_id}")

        transacciones_response = (
            supabase.table("transacciones")
            .select("id_transaccion, fecha, total")
            .eq("id_cliente", user_id)
            .order("fecha", desc=True)
            .execute()
        )

        transacciones = transacciones_response.data or []

        if not transacciones:
            print("[HISTORIAL] Sin transacciones para el usuario")
            return []

        ids_transaccion = [t.get("id_transaccion") for t in transacciones if t.get("id_transaccion") is not None]

        detalles_response = (
            supabase.table("detalle_transaccion")
            .select("id_transaccion, id_libro, cantidad, precio_unitario, subtotal, libros(titulo)")
            .in_("id_transaccion", ids_transaccion)
            .execute()
        )

        detalles = detalles_response.data or []

        detalles_por_transaccion = {}
        for d in detalles:
            tx_id = d.get("id_transaccion")
            if tx_id not in detalles_por_transaccion:
                detalles_por_transaccion[tx_id] = []

            detalles_por_transaccion[tx_id].append({
                "id_libro": d.get("id_libro"),
                "titulo": (d.get("libros") or {}).get("titulo", "Libro"),
                "cantidad": d.get("cantidad", 0),
                "precio_unitario": d.get("precio_unitario", 0),
                "subtotal": d.get("subtotal", 0)
            })

        historial = []
        for tx in transacciones:
            tx_id = tx.get("id_transaccion")
            historial.append({
                "id_transaccion": tx_id,
                "fecha": tx.get("fecha"),
                "total": tx.get("total", 0),
                "items": detalles_por_transaccion.get(tx_id, [])
            })

        print(f"[HISTORIAL] Transacciones encontradas: {len(historial)}")
        return historial

    except Exception as e:
        print(f"[HISTORIAL] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return []