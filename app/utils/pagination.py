from fastapi import Query
from typing import Tuple

def get_pagination(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
) -> Tuple[int, int]:
    """
    Returns offset and limit for SQLAlchemy queries
    """
    offset = (page - 1) * limit
    return offset, limit
