from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderUpdate(BaseModel):
    status: str

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str

    class Config:
        from_attributes = True
