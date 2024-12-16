# E-Commerce API
This is a production-grade RESTful API for an e-commerce platform. The API allows users to view available products, add new products, place orders, and includes security features like API key validation.

## Features:
  - GET /products: Retrieve all products.
  - POST /products: Create a new product (requires authentication).
  - POST /orders: Place an order with stock validation (requires authentication).

## Directory Structure
```
e-commerce/
├── app/                        # Application code
│   ├── __init__.py             # FastAPI application setup
│   ├── middleware.py           # API authorisation validation
│   ├── db.py                   # Database connection and initialization
│   ├── models/                 # Database models (Product, Order)
│   ├── routes/                 # API endpoints (products, orders)
|        ├── orders             # Routes for /orders
|        ├── products           # Routes for /products
│   └── schemas/                # Request/Response schemas
├── tests/                      # Test cases
│   ├── products/               # Product-related tests
│   └── orders/                 # Order-related tests
├── Dockerfile                  # Docker configuration for deployment
|── API contract                # contains API contract
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```
## Setup
  1. Clone the Repository
     ```bash
      git clone https://github.com/vaishucnu/E-Commerce-Platform.git
      cd e-commerce
     ```
  2. Create and Activate a Virtual Environment
      ```bash
       python3 -m venv venv
       source venv/bin/activate
      ```
  3. Install Dependencies
      ```bash
      pip install -r requirements.txt
      ```
  7. Set up environment variables
     Create a .env file in the root of the project and add the following:
        ```bash
        API_KEY=<your-api-key>
        ```

## Run the Application
## Option 1: Run locally
Run the FastAPI app locally using Uvicorn:
```bash
uvicorn app.main:app --reload
```
This will start the server at http://127.0.0.1:8000. You can access the docs at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc UI: http://127.0.0.1:8000/redoc

## Option 2: Dockerize and run
Build the Docker image:
```bash
docker build -t e-commerce-api
```
Run the Docker container:
```bash
docker run -d -p 8000:8000 e-commerce-api
```
Now the app will be accessible at http://localhost:8000.

## API Endpoints 
The API contract is defined in the [API contract](https://github.com/vaishucnu/E-Commerce-Platform/blob/main/API%20contract.pdf) file.

## 1. GET /products
- Retrieve all available products.
```bash
curl -X 'GET' \
  'http://localhost:8000/products' \
  -H 'Authorization: Bearer <API_KEY>'
```

## 2.POST /products
- Create a new product.
```bash
curl -X 'POST' \
  'http://localhost:8000/products' \
  -H 'Authorization: Bearer <API_KEY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Product Name",
  "description": "Product Description",
  "price": 49.99,
  "stock": 100
}'
```
## 3. POST /orders
- Create an order for selected products, ensuring stock availability.
```bash
curl -X 'POST' \
  'http://localhost:8000/orders' \
  -H 'Authorization: Bearer <API_KEY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "products": [{"id": 1, "quantity": 2}],
  "total_price": 99.98
}'
```
## Security (API Key Validation)
- All routes are protected by API key validation.
- To access any of the routes, you must include the Authorization header in your request with the format:
```bash
curl -X 'GET' \
  'http://localhost:8000/products' \
  -H 'Authorization: Bearer <API_KEY>'
```
Replace <API_KEY> with the correct API key.

## Testing
The project includes unit tests for the following functionality:

- Product Management (creating and retrieving products)
- Order Management (creating orders with stock validation)
To run the tests:
```bash
pytest tests/
```
This will automatically run all test cases in the tests/ directory.

## Test Coverage
The tests cover:
- Valid and invalid requests for product retrieval and creation.
- Valid and invalid orders, including scenarios with insufficient stock or invalid product IDs.
- API Key Validation - The API requires an API key for authentication. Include it in the Authorization header as a Bearer token.

## Resultant Output 
You can view the resulting output in the attached PDF, which includes the screenshot of the request and response:
[View Output PDF](https://github.com/vaishucnu/E-Commerce-Platform/blob/main/output.pdf)

