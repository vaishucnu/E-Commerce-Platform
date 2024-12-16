from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Product, Order
from app.schemas import OrderCreate, OrderResponse
from app.db import get_db

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=201)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
  total_price = 0
  product_quantities = order.products

  for item in product_quantities:
    product = db.query(Product).filter(Product.id == item.id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {item.id} not found.")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}.")

    total_price += product.price * item.quantity

  for item in product_quantities:
    product = db.query(Product).filter(Product.id == item.id).first()
    product.stock -= item.quantity
    db.add(product)

  new_order = Order(products=[item.dict() for item in product_quantities], total_price=total_price, status="completed")
  db.add(new_order)
  db.commit()
  db.refresh(new_order)
  return new_order
