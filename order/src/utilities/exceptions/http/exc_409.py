"""
The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
"""

import fastapi

async def http_409_exc_conflict_not_available_product() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_409_CONFLICT,
        detail="Not enough products available to complete the order",
    )
