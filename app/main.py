from fastapi import FastAPI, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.db import engine, Base
from app.api.routers import users, products, orders, payments, notifications
from app.core.middleware import LogProcessTimeMiddleware
from app.core.exceptions import ProductNotFoundException, product_not_found_handler, OrderAlreadyPaidException, order_already_paid_handler
from app.websocket.order_updates import manager

# Startup & Shutdown Events using lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect DB, create tables
    print("Starting up... Connecting database")
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanups
    print("Shutting down... Closing connections")
    engine.dispose()

# OpenAPI Custom Metadata Generation
app = FastAPI(
    title="Event Driven E-Commerce Order Processing System",
    description="A complete production-style FastAPI project demonstrating core features.",
    version="1.0.0",
    contact={
        "name": "Arun E-Commerce API Team",
        "email": "support@example.com",
    },
    terms_of_service="http://example.com/terms/",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    lifespan=lifespan
)

# CORS Support Middleware
# WHY: Allows frontend apps running on different domains to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods: GET, POST, PUT, DELETE, PATCH
    allow_headers=["*"],
)

# Custom Middleware
app.add_middleware(LogProcessTimeMiddleware)

# Exception Handlers Registration
app.add_exception_handler(ProductNotFoundException, product_not_found_handler)
app.add_exception_handler(OrderAlreadyPaidException, order_already_paid_handler)

# APIRouter registration
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(notifications.router)

# WebSocket Endpoint for real-time tracking
@app.websocket("/ws/orders/{order_id}")
async def websocket_endpoint(websocket: WebSocket, order_id: int):
    """
    WHY: Allow clients to listen for order status updates in real-time.
    HOW: Uses WebSockets. Clients connect and wait for broadcasts.
    """
    await manager.connect(websocket, order_id)
    try:
        while True:
            # Keep connection alive, wait for client messages if any
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, order_id)

@app.get("/")
def read_root():
    return {"message": "Welcome to Event Driven E-Commerce Order Processing System"}
