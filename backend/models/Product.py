from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    """Modelo simple para productos"""
    name: str
    price: float
    description: Optional[str] = None
    stock: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
