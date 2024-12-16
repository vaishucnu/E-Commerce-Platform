from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import ProductCreate, ProductResponse
from app.db import get_db
from typing import List


router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
  products = db.query(Product).all()
  return products

@router.post("/", response_model=ProductResponse, status_code=201)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
  if db.query(Product).filter(Product.name == product.name).first():
      raise HTTPException(status_code=400, detail="Product with this name already exists.")
  new_product = Product(**product.dict())
  db.add(new_product)
  db.commit()
  db.refresh(new_product)
  return new_product
