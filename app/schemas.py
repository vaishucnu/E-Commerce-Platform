from pydantic import BaseModel, Field
from typing import List, Optional

class ProductCreate(BaseModel):
  name: str = Field(..., min_length=1, max_length=100, description="The name of the product")
  description: Optional[str] = Field(None, max_length=255, description="A short description of the product")
  price: float = Field(..., gt=0, description="Price must be a positive number")
  stock: int = Field(..., ge=0, description="Stock must be a non-negative integer")

class ProductResponse(BaseModel):
  id: int
  name: str
  description: Optional[str]
  price: float
  stock: int

  class Config:
      orm_mode = True

class OrderProduct(BaseModel):
  id: int = Field(..., description="The ID of the product to order")
  quantity: int = Field(..., gt=0, description="Quantity must be a positive integer")

class OrderCreate(BaseModel):
  products: List[OrderProduct] = Field(..., description="List of products with their quantities")
  total_price: Optional[float]

class OrderResponse(BaseModel):
  id: int
  products: List[OrderProduct]
  total_price: float
  status: str

  class Config:
      orm_mode = True
