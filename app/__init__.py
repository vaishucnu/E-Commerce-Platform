from fastapi import FastAPI
from app.db import init_db
from app.routes.products import router as products_router
from app.routes.orders import router as orders_router
from app.middleware import APIKeyMiddleware

def create_app():
  app = FastAPI(title="E-Commerce API", version="1.0.0")
  init_db()
  
  # Add API Key validation middleware globally
  app.add_middleware(APIKeyMiddleware)

  # Include routers for products and orders
  app.include_router(products_router, prefix="/products", tags=["Products"])
  app.include_router(orders_router, prefix="/orders", tags=["Orders"])
  
  return app

app = create_app()
