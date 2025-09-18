from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from models import Product
from database import get_products_collection


class ProductCRUD:
    def __init__(self):
        self.collection = None
    
    def _get_collection(self):
        """Obtener la colección de forma lazy"""
        if self.collection is None:
            self.collection = get_products_collection()
        return self.collection

    async def create_product(self, product: Product) -> dict:
        """Crear un nuevo producto"""
        collection = self._get_collection()
        
        # Agregar timestamps
        product_dict = product.dict()
        product_dict["created_at"] = datetime.utcnow()
        product_dict["updated_at"] = datetime.utcnow()
        
        # Insertar en la base de datos
        result = await collection.insert_one(product_dict)
        
        # Obtener el producto creado
        created_product = await collection.find_one({"_id": result.inserted_id})
        
        # Convertir ObjectId a string para la respuesta
        created_product["id"] = str(created_product["_id"])
        del created_product["_id"]
        
        return created_product

    async def get_product(self, product_id: str) -> Optional[dict]:
        """Obtener un producto por ID"""
        collection = self._get_collection()
        
        try:
            # Buscar el producto
            product = await collection.find_one({"_id": ObjectId(product_id)})
            
            if product:
                # Convertir ObjectId a string
                product["id"] = str(product["_id"])
                del product["_id"]
                return product
            
            return None
        except Exception:
            return None

    async def get_all_products(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Obtener todos los productos con paginación"""
        collection = self._get_collection()
        
        cursor = collection.find().skip(skip).limit(limit)
        products = []
        
        async for product in cursor:
            # Convertir ObjectId a string
            product["id"] = str(product["_id"])
            del product["_id"]
            products.append(product)
        
        return products

    async def update_product(self, product_id: str, product_data: dict) -> Optional[dict]:
        """Actualizar un producto"""
        collection = self._get_collection()
        
        try:
            # Filtrar campos None y agregar timestamp de actualización
            update_data = {k: v for k, v in product_data.items() if v is not None}
            update_data["updated_at"] = datetime.utcnow()
            
            # Actualizar el producto
            result = await collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": update_data}
            )
            
            if result.modified_count == 1:
                # Obtener el producto actualizado
                updated_product = await collection.find_one({"_id": ObjectId(product_id)})
                
                if updated_product:
                    # Convertir ObjectId a string
                    updated_product["id"] = str(updated_product["_id"])
                    del updated_product["_id"]
                    return updated_product
            
            return None
        except Exception:
            return None

    async def delete_product(self, product_id: str) -> bool:
        """Eliminar un producto"""
        collection = self._get_collection()
        
        try:
            result = await collection.delete_one({"_id": ObjectId(product_id)})
            return result.deleted_count == 1
        except Exception:
            return False

    async def search_products(self, search_term: str) -> List[dict]:
        """Buscar productos por nombre o descripción"""
        collection = self._get_collection()
        
        # Búsqueda con expresión regular (case insensitive)
        query = {
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}}
            ]
        }
        
        cursor = collection.find(query)
        products = []
        
        async for product in cursor:
            # Convertir ObjectId a string
            product["id"] = str(product["_id"])
            del product["_id"]
            products.append(product)
        
        return products


# Instancia global del CRUD
product_crud = ProductCRUD()