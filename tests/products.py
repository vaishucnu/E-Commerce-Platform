import pytest
from fastapi.testclient import TestClient
from app.models import Product
from app.db import get_db
from unittest.mock import MagicMock

from tests.common.test_common import client  # Import the common test client

def test_get_products(mock_db):
  """Test: Retrieve all products"""
  mock_db.query.return_value.all.return_value = [
      Product(id=1, name="Product 1", description="Description 1", price=29.99, stock=100),
      Product(id=2, name="Product 2", description="Description 2", price=49.99, stock=150),
  ]
  response = client.get("/products/products", headers={"Authorization": "Bearer valid_api_key"})
  assert response.status_code == 200
  assert len(response.json()) == 2
  assert response.json()[0]["name"] == "Product 1"
  assert response.json()[1]["name"] == "Product 2"

def test_get_products_empty_db(mock_db):
  """Test: No products available (empty database)"""
  mock_db.query.return_value.all.return_value = []
  response = client.get("/products/products", headers={"Authorization": "Bearer valid_api_key"})
  assert response.status_code == 200
  assert response.json() == []

def test_create_product(mock_db):
  """Test: Create a new product"""
  product_data = {
      "name": "Product 3",
      "description": "Description 3",
      "price": 79.99,
      "stock": 200
  }
  mock_db.add.return_value = None
  mock_db.commit.return_value = None
  mock_db.refresh.return_value = None
  response = client.post("/products/products", json=product_data, headers={"Authorization": "Bearer valid_api_key"})
  assert response.status_code == 200
  assert response.json()["name"] == "Product 3"
  assert response.json()["price"] == 79.99

def test_create_product_missing_fields(mock_db):
  """Test: Missing required fields (e.g., stock)"""
  product_data = {"name": "Product 4", "price": 99.99}
  response = client.post("/products/products", json=product_data, headers={"Authorization": "Bearer valid_api_key"})
  assert response.status_code == 422
  assert "stock" in response.json()["detail"][0]["loc"]

def test_create_product_invalid_price(mock_db):
  """Test: Invalid price (negative value)"""
  product_data = {
      "name": "Product 5",
      "description": "Invalid price product",
      "price": -10.00,
      "stock": 50
  }
  response = client.post("/products/products", json=product_data, headers={"Authorization": "Bearer valid_api_key"})
  assert response.status_code == 422
  assert "price" in response.json()["detail"][0]["loc"]
