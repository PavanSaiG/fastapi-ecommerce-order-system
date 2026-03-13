# 🏗️ FastAPI Event-Driven E-Commerce: Step-by-Step Development Guide

This document outlines the step-by-step logic, architectural decisions, and package mappings used to build this production-style Event-Driven E-Commerce API system. 

It serves as a reference for your future development and helps you look back at exactly what packages were installed, why they were chosen, and where they are used.

---

## 📦 Required Packages and Where They Are Used

Here is the breakdown of the dependencies mapped inside `requirements.txt` and their specific use cases in the codebase:

| Package | Purpose | Where It Is Used |
|---|---|---|
| **`fastapi`** | The core web framework running the entire application. | Used everywhere (`app/main.py`, `app/api/routers/*.py`). |
| **`uvicorn[standard]`** | The ASGI server that runs the FastAPI application and handles concurrent network processing safely. | Executed in the terminal (`uvicorn app.main:app`). |
| **`sqlalchemy`** | The Object-Relational Mapper (ORM) mapped to our backend SQLite Database representing state. | `app/database/db.py`, `app/models/*.py` |
| **`pydantic` & `pydantic[email]`** | Strictly validates request-bodies via type annotation. Fails gracefully with JSON errors on bad payloads natively. | `app/schemas/*.py` |
| **`pydantic-settings`** | Helps securely import strings from `.env` environment files directly into typed python variables. | `app/config.py` |
| **`passlib[bcrypt]` & `bcrypt==3.2.2`** | Performs cryptography! Used to securely hash strings before committing user passwords into databases. | `app/core/security.py` |
| **`python-jose[cryptography]`** | Used exclusively for generating & decoding JSON Web Tokens (JWT) strings exchanged during logging in. | `app/core/dependencies.py`, `app/core/security.py` |
| **`python-multipart`** | Specifically parses multipart HTTP streams, required for File Uploads and standard Form Data (e.g. `OAuth2PasswordRequestForm`). | `app/api/routers/users.py`, `app/api/routers/products.py` |
| **`pytest` & `httpx`** | Test runners capable of launching isolated instances of FastAPI to mock endpoints automatically. | `tests/*.py` |

---

## 🛠️ Step-by-Step Development Process

### Step 1: Core Configuration and Database Connectivity
Before generating routes, we lay the data foundation.
1. **`app/config.py`**: A centralized location grabbing environment variables securely.
2. **`app/database/db.py` & `app/database/session.py`**: Initializes the `create_engine` (connecting to standard `sqlite`) and generates reusable sessions.

### Step 2: Defining the Entities (SQLAlchemy ORM)
We mapped our SQLite relationships natively via Python Objects.
1. **`app/models/user.py`** - Represents our customers/admins natively storing hashed passwords.
2. **`app/models/product.py`** - Handles inventory schemas.
3. **`app/models/order.py`** - Holds relationship keys bridging products with users representing sales data state.

### Step 3: Pydantic Data Validations
Before we inject data into our ORM, it must be validated perfectly. 
We created **`app/schemas/...`**.
- They ensure string payloads like `email` fit proper standard `<>@<>.com` regex constructs (this is why `pydantic[email]` was added to requirements).
- `Config: from_attributes = True` was placed on all Response models. This signals FastAPI to automatically convert raw Database DB-Models directly into JSON on return.

### Step 4: Security and Dependency Injections
How do we ensure that endpoints are perfectly gated without repeating `if user.token is valid:` conditionally in every route explicitly? 
- **`app/core/security.py`**: Implements strictly algorithmic hashing (using `passlib`) & JWT Generation (using `jose`). Note: We bound strings natively to `[:72]` character limits strictly averting internal crash payload states.
- **`app/core/dependencies.py`**: Defines standard `get_current_user` logic mapping FastAPI `Depends(...)`. If the token is natively invalid or expired, this dependency throws a `401 Unauthorized` exception intercepting execution strictly preventing endpoint breaches dynamically.

### Step 5: Route Implementation
Each domain of the system got its distinct router within **`app/api/routers/...`**
1. **Users (`users.py`)**: Authenticated forms parsing via `python-multipart` to return the aforementioned JWTs.
2. **Products (`products.py`)**: Showcases simple CRUD, path parameter limits, query skips, and binary File Uploading streams natively.
3. **Orders (`orders.py`)**: Showcases `BackgroundTasks`. Immediately after a customer submits an order natively, FastAPI closes the HTTP connection and releases them while queuing an email-function on an isolated worker automatically without utilizing external Celery/RabbitMQ mechanisms dynamically down stream.

### Step 6: Payment Real-Time Interactivity (WebSockets)
1. **`app/websocket/order_updates.py`**: A standard connection manager buffering native connected sockets continuously in a generic python dict list grouping.
2. **`app/api/routers/payments.py`**: Handles incoming payments updating DB state limits. When `order.status` evolves to `PAID`, python calls `manager.broadcast_status()` which maps cleanly over our WebSocket pipes seamlessly without polling.

### Step 7: Final Main Hookups
Everything converges upon **`app/main.py`**.
We define explicit cross-cutting handlers.
- **CORS Middleware**: Prevents browser security exceptions intercepting native Web requests cleanly if external React.js applications boot up natively calling the endpoints.
- **`LogProcessTimeMiddleware`**: An abstract hook appending precisely tracked seconds to response payloads. 
- **`app.include_router(...)`**: Bootstraps all routing components together natively registering the system.

### Step 8: Quality Control
We wrote isolated scenarios verifying our logic.
- **`tests/test_users.py`** natively runs the `TestClient` mimicking the application cleanly over a temporary mock dataset without needing to boot specific web-server hooks.
