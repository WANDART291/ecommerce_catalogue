# 🛒 Ecommerce Catalogue API

A **production-grade, transactional E-commerce backend** built for **reliability and scale**.

---

## 🚀 Project Overview

**Ecommerce Catalogue** is a **headless backend API** designed to power modern online marketplaces.  
It goes beyond simple CRUD operations to handle complex, real-world commerce logic, including:

- Recursive product categorization  
- Inventory concurrency handling  
- Asynchronous notifications  

### 🎯 Key Problem Solved

**Preventing overselling during high-traffic events** (e.g., Black Friday) by using **atomic database transactions** to lock inventory at the exact moment of purchase.

---

## ⚡ System Architecture

### Order Processing Workflow

This diagram illustrates how the system safely handles checkout requests using **Atomic Transactions** and **Async Workers**.

```mermaid
sequenceDiagram
    participant User
    participant API as Django API
    participant DB as PostgreSQL
    participant Celery as Celery Worker

    User->>API: POST /orders/ (Checkout)
    
    rect rgb(240, 248, 255)
    note right of API: Atomic Transaction Start
    API->>DB: Check Cart & Stock
    alt Stock Available
        API->>DB: Create Order
        API->>DB: Deduct Inventory (Lock Row)
        API->>DB: Delete Cart
        DB-->>API: Success
    else Stock Empty
        DB-->>API: Rollback Transaction
        API-->>User: 400 Bad Request
    end
    end

    API->>Celery: Trigger Email Task (.delay)
    API-->>User: 201 Created (Order Receipt)
    
    Celery->>User: Send Confirmation Email (Async)

🛠️ Technology Stack
Component	Technology	Description
Core Framework	Django & DRF	The brain of the application
Database	PostgreSQL 15	Relational storage for products, orders, and users
Concurrency	Atomic Transactions	Ensures order creation and inventory deduction happen simultaneously
Async Tasks	Celery & Redis	Background jobs (emails, maintenance tasks)
API Docs	Swagger / OpenAPI	Interactive API docs via drf-spectacular
Authentication	JWT (Djoser)	Secure, stateless auth with social login support
📂 Project Structure
ecommerce_catalogue/
├── config/             # Project settings and main URL routing
├── catalogue/          # Product, Brand, and Category management
├── cart/               # Shopping cart logic
├── orders/             # Transactional logic & Celery tasks
│   ├── tasks.py        # Email & background jobs
│   └── views.py        # Atomic inventory deduction logic
├── docker-compose.yml  # Container orchestration
└── requirements.txt    # Python dependencies

🔌 API Reference
Feature	Method	Endpoint	Description
Docs	GET	/api/docs/	Interactive Swagger UI (Start here!)
Auth	POST	/auth/jwt/create/	Obtain access & refresh tokens
Catalog	GET	/api/v1/catalogue/products/	List products with filtering & search
Cart	POST	/api/v1/cart/	Add items to the shopping cart
Orders	POST	/api/v1/orders/	Checkout: converts Cart to Order & locks stock
🏁 Getting Started
1️⃣ Clone & Build
git clone https://github.com/yourusername/ecommerce_catalogue.git
cd ecommerce_catalogue
docker compose up --build

2️⃣ Environment Configuration

Create a .env file in the root directory (optional — defaults are provided in Docker):

POSTGRES_DB=ecommerce_nexus
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin123
DB_HOST=db
REDIS_HOST=redis
SECRET_KEY=your-secret-key-here

3️⃣ Setup Database
# Apply migrations
docker compose exec web python manage.py migrate

# Create a superuser for the Admin Panel
docker compose exec web python manage.py createsuperuser

4️⃣ Access the App

API Root: http://localhost:8000/api/v1/

Swagger Docs: http://localhost:8000/api/docs/

Admin Panel: http://localhost:8000/admin/

🧪 Testing

The project includes a comprehensive test suite covering:

Model integrity

API responses

Concurrency & transactional safety

docker compose exec web python manage.py test catalogue

👨‍💻 Author

Developed by [Wandile Khanyile].
Ready for production deployment 🚀