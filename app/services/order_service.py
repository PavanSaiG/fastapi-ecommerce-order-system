import time

def send_order_confirmation_email(email: str, order_id: int):
    """
    Simulates sending an email in the background.
    """
    time.sleep(2)  # Simulate network delay
    print(f"Email sent to {email} confirming order {order_id}")

def trigger_invoice_generation(order_id: int):
    """
    Simulates generating an invoice pdf in the background.
    """
    time.sleep(3)
    print(f"Invoice generated for order {order_id}")
