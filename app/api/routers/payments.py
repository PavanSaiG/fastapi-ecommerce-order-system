from fastapi import APIRouter, Depends, BackgroundTasks, Response
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import os

from app.database.session import get_db
from app.models.order import Order
from app.core.exceptions import OrderAlreadyPaidException
from app.services.order_service import trigger_invoice_generation
from app.websocket.order_updates import manager

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/{order_id}/pay")
async def process_payment(order_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    WHY: Simulate payment processing.
    HOW: Validates order state, raises custom exception if already paid, updates status, and broadcasts via WebSocket.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"error": "Order not found"}
    
    if order.status != "PENDING":
        raise OrderAlreadyPaidException(order_id=order_id)
    
    # Process payment (mock)
    order.status = "PAID"
    db.commit()
    
    # Trigger invoice generation background task
    background_tasks.add_task(trigger_invoice_generation, order_id)
    
    # Broadcast real-time status update
    await manager.broadcast_status(order_id, "PAID")
    
    return {"message": f"Payment successful for order {order_id}"}

@router.get("/{order_id}/invoice")
async def download_invoice(order_id: int):
    """
    WHY: Allow downloading of generated invoices.
    HOW: Returns FileResponse for downloading a file. Will generate a dummy text file if it doesn't exist.
    """
    file_path = f"invoice_{order_id}.pdf"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(f"Invoice for Order {order_id}")
    return FileResponse(path=file_path, filename=f"invoice_{order_id}.pdf", media_type='application/pdf')
