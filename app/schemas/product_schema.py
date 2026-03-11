from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., title="The name of the item", max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    stock: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
