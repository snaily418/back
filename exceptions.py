from fastapi import HTTPException

AccessDeniedException = HTTPException(
    status_code=403,
    detail="Access denied",
)