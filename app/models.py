from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
  __tablename__ = 'products'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  description = Column(String)
  price = Column(Float, nullable=False)
  stock = Column(Integer, nullable=False)

class Order(Base):
  __tablename__ = 'orders'

  id = Column(Integer, primary_key=True, index=True)
  products = Column(JSON, nullable=False)  # List of product IDs and quantities
  total_price = Column(Float, nullable=False)
  status = Column(String, default="pending")
