import pytest
from fastapi.testclient import TestClient
from app.models import Product
from app.db import get_db
from unittest.mock import MagicMock

from tests.common.test_common import client

def test_create_order(mock_db):
  """Test: Place a new order with valid stock"""
  mock_db.query.return_value.filter_by.return_value.first.return_value = Product(id=1, name="Product 1", description="Description 1", price=29.99, stock=100)
  order_data = {
      "products": [
          {"id": 1, "quantity": 2}
      ],
      "total_price": 59.98
  }
  response = client.post("/orders/orders", json=order_data, headers={"Authorization": "Bearer valid_api_key"})
  assert response.status_code == 200
  assert response.json()["status"] == "completed"

def test_create_order_insufficient_stock(mock_db):
    """Test: Insufficient stock for an order"""
    mock_db.query.return_value.filter_by.return_value.first.return_value = Product(id=1, name="Product 1", description="Description 1", price=29.99, stock=10)
    order_data = {
        "products": [
            {"id": 1, "quantity": 15}  # Trying to order more than available stock
        ],
        "total_price": 449.85
    }
    response = client.post("/orders/orders", json=order_data, headers={"Authorization": "Bearer valid_api_key"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock available for product 1"

def test_create_order_invalid_product(mock_db):
  """Test: Invalid product ID in order"""
  mock_db.query.return_value.filter_by.return_value.first.return_value = None  # No product found
  order_data = {
      "products": [
          {"id": 999, "quantity": 2}  # Invalid product ID
      ],
      "total_price": 59.98
  }
  response = client.post("/orders/orders", json=order_data, headers={"Authorization": "Bearer valid_api_key"})
  assert response.status_code == 400
  assert response.json()["detail"] == "Product with ID 999 not found"

def test_create_order_missing_product_id(mock_db):
  """Test: Missing product ID in order"""
  order_data = {
      "products": [
          {"quantity": 2}  # Missing product ID
      ],
      "total_price": 59.98
  }
  response = client.post("/orders/orders", json=order_data, headers={"Authorization": "Bearer valid_api_key"})
  assert response.status_code == 422
  assert "id" in response.json()["detail"][0]["loc"]

def test_create_order_unauthorized():
  """Test: Unauthorized access while creating an order"""
  order_data = {
      "products": [
          {"id": 1, "quantity": 1}
      ],
      "total_price": 29.99
  }
  response = client.post("/orders/orders", json=order_data, headers={"Authorization": "Bearer invalid_api_key"})
  assert response.status_code == 401
  assert response.json() == {"detail": "Invalid or missing API key"}
