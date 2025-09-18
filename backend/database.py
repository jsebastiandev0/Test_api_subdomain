import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")
MONGODB_URL = os.getenv("MONGODB_URL")

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