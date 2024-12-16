from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import status
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")  # Retrieve API key from environment variable

class APIKeyMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    api_key = request.headers.get("Authorization")

    # Validate the API key
    if not api_key or api_key != f"Bearer {API_KEY}":
      error_detail = {
        "error": "Unauthorized",
        "message": "Invalid or missing API key",
        "status_code": status.HTTP_401_UNAUTHORIZED
      }
      # Return custom error response with a JSON body
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=error_detail
      )

    # If valid, continue with the request processing
    response = await call_next(request)
    return response
