from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order_unauthorized():
    # Attempting to create an order without auth should fail
    response = client.post(
        "/orders/",
        json={"product_id": 1, "quantity": 2}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
