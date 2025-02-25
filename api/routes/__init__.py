import importlib
from fastapi import FastAPI

# **List of route modules**
ROUTE_MODULES = [
    "api.routes.health",
    "api.routes.docs",
    "api.routes.feedback",
    "api.routes.auth"
]

def register_routes(app: FastAPI):
    """Dynamically register all routes from the ROUTE_MODULES list."""
    for module_name in ROUTE_MODULES:
        module = importlib.import_module(module_name)
        if hasattr(module, "router"):
            app.include_router(module.router, prefix="/api/v1")  # Prefixing all routes
