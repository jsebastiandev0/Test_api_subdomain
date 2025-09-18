import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Variables de configuración
MONGODB_BASE_URL = os.getenv("MONGODB_URL")
MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Verificar que las variables existen
if not MONGODB_BASE_URL:
    raise ValueError("MONGODB_URL no está configurada en el archivo .env")
if not MONGO_USERNAME:
    raise ValueError("MONGO_INITDB_ROOT_USERNAME no está configurada en el archivo .env")
if not MONGO_PASSWORD:
    raise ValueError("MONGO_INITDB_ROOT_PASSWORD no está configurada en el archivo .env")
if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME no está configurada en el archivo .env")

# Construir la URL completa con credenciales
MONGODB_URL = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGODB_BASE_URL.replace('mongodb://', '')}"

# Cliente de MongoDB
client: AsyncIOMotorClient = None
database = None


async def connect_to_mongo():
    """Conectar a MongoDB"""
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    print(f"Conectado a MongoDB: {DATABASE_NAME}")


async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    global client
    if client:
        client.close()
        print("Conexión a MongoDB cerrada")


def get_database():
    """Obtener la instancia de la base de datos"""
    return database


def get_collection(collection_name: str):
    """Obtener una colección específica"""
    return database[collection_name]


# Función helper para obtener la colección de productos
def get_products_collection():
    """Obtener la colección de productos"""
    return get_collection("products")