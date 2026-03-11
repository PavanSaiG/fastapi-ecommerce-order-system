from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id

class OrderAlreadyPaidException(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id

# Custom handlers for standard exceptions
async def product_not_found_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Product with ID {exc.product_id} not found."}
    )

async def order_already_paid_handler(request: Request, exc: OrderAlreadyPaidException):
    return JSONResponse(
        status_code=400,
        content={"message": f"Order with ID {exc.order_id} has already been paid."}
    )
