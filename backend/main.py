from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from models import Product
from crud import product_crud
from database import connect_to_mongo, close_mongo_connection
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI(
    title="Products CRUD API",
    description="API para gestionar productos con MongoDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicio y cierre
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "Products CRUD API", "version": "1.0.0"}

# Crear producto
@app.post("/products/", response_model=dict, status_code=201)
async def create_product(product: Product):
    """Crear un nuevo producto"""
    try:
        created_product = await product_crud.create_product(product)
        return {
            "message": "Producto creado exitosamente",
            "product": created_product
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {str(e)}")

# Obtener todos los productos
@app.get("/products/", response_model=dict)
async def get_products(
    skip: int = Query(0, ge=0, description="Número de productos a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Número de productos a obtener")
):
    """Obtener todos los productos con paginación"""
    try:
        products = await product_crud.get_all_products(skip=skip, limit=limit)
        return {
            "message": "Productos obtenidos exitosamente",
            "products": products,
            "total": len(products),
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")

# Obtener producto por ID
@app.get("/products/{product_id}", response_model=dict)
async def get_product(product_id: str):
    """Obtener un producto por ID"""
    try:
        product = await product_crud.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        return {
            "message": "Producto encontrado",
            "product": product
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener producto: {str(e)}")

# Actualizar producto
@app.put("/products/{product_id}", response_model=dict)
async def update_product(product_id: str, product_data: dict):
    """Actualizar un producto"""
    try:
        updated_product = await product_crud.update_product(product_id, product_data)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Producto no encontrado o no se pudo actualizar")
        
        return {
            "message": "Producto actualizado exitosamente",
            "product": updated_product
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")

# Eliminar producto
@app.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    """Eliminar un producto"""
    try:
        deleted = await product_crud.delete_product(product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        return {
            "message": "Producto eliminado exitosamente",
            "product_id": product_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")

# Buscar productos
@app.get("/products/search/{search_term}", response_model=dict)
async def search_products(search_term: str):
    """Buscar productos por nombre o descripción"""
    try:
        products = await product_crud.search_products(search_term)
        return {
            "message": f"Búsqueda completada para: {search_term}",
            "products": products,
            "total": len(products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

# Endpoint para verificar el estado de la API
@app.get("/health", response_model=dict)
async def health_check():
    """Verificar el estado de la API y conexión a la base de datos"""
    try:
        # Intentar hacer una operación simple en la DB
        await product_crud.get_all_products(limit=1)
        return {
            "status": "healthy",
            "database": "connected",
            "message": "API funcionando correctamente"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "message": f"Error: {str(e)}"
        }
    