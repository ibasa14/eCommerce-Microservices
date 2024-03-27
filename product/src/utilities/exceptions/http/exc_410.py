"""
The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
"""

import fastapi

async def http_410_product_gone() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_410_GONE,
        detail="The requested product is no longer available.",
    )
