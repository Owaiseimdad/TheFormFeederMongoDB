from fastapi import HTTPException, status
from typing import Any, Dict

class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str,
        meta: Dict[str, Any] = None
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers={"X-Error-Code": error_code}
        )
        self.meta = meta or {}

# Standard Errors
class NotFoundError(CustomHTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="not_found"
        )