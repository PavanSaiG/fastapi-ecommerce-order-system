# ⚡ Event-Driven E-Commerce Order Processing System (FastAPI)

![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Architecture](https://img.shields.io/badge/Architecture-Event%20Driven-orange)
![Status](https://img.shields.io/badge/Project-Production%20Style-success)

A **production-grade backend system built with FastAPI** that simulates a modern **event-driven e-commerce platform**.
The system manages **Users, Products, Orders, Payments, and Notifications** while demonstrating best practices in **API design, authentication, async processing, background tasks, and WebSocket communication**.

This repository demonstrates how **real-world scalable backend services** are structured using FastAPI.

-----

# 🚀 Key Features

✔ RESTful API design using **FastAPI**
✔ **OAuth2 + JWT authentication**
✔ **SQLAlchemy ORM** database models
✔ **Pydantic validation schemas**
✔ **Layered architecture (DDD-inspired)**
✔ **Background tasks for async processing**
✔ **WebSocket support for real-time updates**
✔ **Centralized dependency injection**
✔ **Structured exception handling**
✔ **Pytest test suite**

---

# 🏗 System Architecture

The application follows a **layered architecture inspired by Domain Driven Design (DDD)**.

```
Client
   │
   ▼
FastAPI Routers
   │
   ▼
Service Layer (Business Logic)
   │
   ▼
ORM Models (SQLAlchemy)
   │
   ▼
Database
```

### Architecture Layers

| Layer          | Responsibility                                |
| -------------- | --------------------------------------------- |
| **Routers**    | API endpoints and request handling            |
| **Schemas**    | Request validation and response serialization |
| **Services**   | Business logic and orchestration              |
| **Models**     | Database ORM entities                         |
| **Core**       | Security, dependencies, middleware            |
| **WebSockets** | Real-time communication                       |

---

# 📂 Project Structure

```text
fastapi-order-system
│
├── app
│   ├── api
│   │   └── routers
│   │       ├── notifications.py
│   │       ├── orders.py
│   │       ├── payments.py
│   │       ├── products.py
│   │       └── users.py
│   │
│   ├── core
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   └── security.py
│   │
│   ├── database
│   │   ├── db.py
│   │   └── session.py
│   │
│   ├── models
│   │   ├── order.py
│   │   ├── product.py
│   │   └── user.py
│   │
│   ├── schemas
│   │   ├── order_schema.py
│   │   ├── product_schema.py
│   │   └── user_schema.py
│   │
│   ├── services
│   │   ├── order_service.py
│   │   └── payment_service.py
│   │
│   ├── websocket
│   │   └── order_updates.py
│   │
│   ├── config.py
│   └── main.py
│
├── tests
│   ├── test_orders.py
│   └── test_users.py
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/fastapi-order-system.git
cd fastapi-order-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Linux / Mac**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start the FastAPI server using **Uvicorn**:

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically generates API documentation.

| Documentation | URL                         |
| ------------- | --------------------------- |
| Swagger UI    | http://127.0.0.1:8000/docs  |
| ReDoc         | http://127.0.0.1:8000/redoc |

Swagger allows **testing APIs directly from the browser**.

---

# 🔐 Authentication Flow

This project uses **OAuth2 Password Flow with JWT Tokens**.

### Step 1 — Register User

```
POST /users/register
```

Example body:

```json
{
  "email": "user@email.com",
  "password": "password123"
}
```

---

### Step 2 — Login

```
POST /users/login
```

Form Data:

```
username=user@email.com
password=password123
```

Returns:

```
access_token
```

---

### Step 3 — Use Token

Add header in protected API calls:

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

# 📡 API Examples

### Create Product

```bash
curl -X POST http://127.0.0.1:8000/products/ \
-H "Content-Type: application/json" \
-d '{"name":"Laptop","description":"Gaming Laptop","price":1200,"stock":10}'
```

---

### Get Product

```bash
curl -X GET http://127.0.0.1:8000/products/1
```

---

### Place Order

```bash
curl -X POST http://127.0.0.1:8000/orders/ \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"product_id":1,"quantity":1}'
```

---

### Pay for Order

```bash
curl -X POST http://127.0.0.1:8000/payments/1/pay
```

---

# ⚡ Real-Time Order Updates (WebSocket)

The system pushes **live order status updates** using WebSockets.

Example client:

```javascript
let ws = new WebSocket("ws://localhost:8000/ws/orders/1");

ws.onmessage = function(event) {
    console.log("Order Update:", event.data);
};
```

When payment is triggered, the server broadcasts updates to the socket.

---

# 🧪 Running Tests

The project includes **Pytest-based unit tests**.

Run tests with:

```bash
pytest
```

---

# 📌 Technologies Used

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| FastAPI    | High-performance Python API framework |
| SQLAlchemy | ORM for database models               |
| Pydantic   | Data validation                       |
| Uvicorn    | ASGI server                           |
| JWT        | Authentication tokens                 |
| WebSockets | Real-time updates                     |
| Pytest     | Testing framework                     |

---

# 📈 Future Improvements

* Docker containerization
* CI/CD pipeline (GitHub Actions)
* Kafka / EventBridge integration
* Redis caching
* Async database support

---

# 👨‍💻 Author

**Pavan Sai Gajula**

Python / AWS Developer
Backend & Cloud Enthusiast

---

⭐ If you found this project useful, consider **starring the repository**.
