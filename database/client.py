"""
Este módulo contiene el objeto Client de Supabase, para permitir
la conexión desde el backend a la base de datos.
"""
# os Para buscar los códigos de la base de datos en el sistema operativo
import os

# load_dotenv para obtener las variables de entorno
from dotenv import load_dotenv

# La función para crear un cliente de supabase, y el objeto Client para typing
from supabase import create_client, Client

# Cargar las variables del .env
load_dotenv()

# Las guardamos en variables (url y key)
url: str | None= os.getenv("SUPABASE_URL")
key: str | None= os.getenv("SUPABASE_KEY")

# Validamos que las variables existan para evitar errores crípticos
if not url or not key:
    raise ValueError("Faltan las credenciales de Supabase en el archivo .env")

# Instancia única del cliente para todo el proyecto
supabase: Client = create_client(url, key)