from fastapi import APIRouter # Import the module docstring

router = APIRouter()

docs_content = """
API Gateway Documentation

## Overview
This API Gateway serves as a central entry point for various microservices, dynamically managing routes without modifying `main.py` directly.

## Available Services:
### 1. Health Check (`/api/v1/health`)
- **Description**: Provides a health status of the service.
- **Endpoints**:
  - `GET /health` → Returns service uptime and status.

### 2. Feedback Service (`/api/v1/feedback`)
- **Description**: Handles user feedback submissions.
- **Endpoints**:
  - `POST /feedback` → Submit new feedback.
  - `GET /feedback/{feedback_id}` → Retrieve feedback by ID.
  - `GET /feedback` → Get all feedback.

### 3. Authentication Service (`/api/v1/auth`)
- **Description**: Manages authentication and user sessions.
- **Endpoints**:
  - `POST /auth/login` → User login.
  - `POST /auth/register` → User registration.
  - `POST /auth/logout` → Logout current session.

---

## Dynamic Route Handling
New services can be added without modifying `main.py`. Simply follow these steps:

### Steps to Add a New Service:
1. **Create a New Route Module**  
   - Example: `routes/new_service.py`
   ```python
   from fastapi import APIRouter

   router = APIRouter()

   @router.get("/new-endpoint")
   def new_endpoint():
       return {"message": "This is a new service!"}
"""

@router.get("/docs", tags=["Documentation"])
def get_docs():
    
    return {"docs": docs_content}
