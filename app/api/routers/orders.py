from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Form
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse
from app.core.dependencies import get_current_user
from app.services.order_service import send_order_confirmation_email

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    WHY: Handles user order placement.
    HOW: Async endpoint. Demonstrates BackgroundTasks for sending emails, preventing users from waiting for the email to send.
    """
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Calculate price
    total_price = product.price * order.quantity
    
    # Create order
    new_order = Order(
        user_id=current_user.id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status="PENDING"
    )
    db.add(new_order)
    
    # Update stock
    product.stock -= order.quantity
    
    db.commit()
    db.refresh(new_order)
    
    # Add background task
    background_tasks.add_task(send_order_confirmation_email, current_user.email, new_order.id)
    
    return new_order

@router.post("/checkout-form")
async def submit_checkout_form(
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    WHY: Accept order from standard HTML form.
    HOW: Uses Form variables. Parses standard application/x-www-form-urlencoded data.
    """
    return {"product_id": product_id, "quantity": quantity, "message": "Checkout form received"}

@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    WHY: Retrieve user's orders.
    HOW: Sync endpoint filtering by current authenticated user.
    """
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders
