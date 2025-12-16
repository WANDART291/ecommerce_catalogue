# 🛒 Ecommerce Catalogue API

A **production-grade, transactional E-commerce backend** built for **reliability and scale**.

**Tech Stack:** Django · Django REST Framework · Docker · PostgreSQL · Celery · Redis

---

## 🚀 Project Overview

**Ecommerce Catalogue API** is a **headless backend** designed to power modern online marketplaces.

It goes beyond basic CRUD functionality to handle **real-world commerce challenges**, including:

- Recursive product categorization  
- Safe inventory management under high traffic  
- Transactional order processing  
- Asynchronous background tasks  

This project is built with **production reliability** in mind.

---

## 🎯 Key Problem Solved

### Preventing Overselling

During high-traffic events (e.g., Black Friday), multiple users may attempt to buy the same product at the same time.

This API prevents **overselling** by:

- Using **atomic database transactions**
- Locking inventory rows during checkout
- Ensuring order creation and stock deduction happen **together or not at all**

If stock is insufficient, the transaction is rolled back automatically.

---

## ⚙️ Order Processing Flow (Conceptual)

1. User submits a checkout request  
2. Server starts a database transaction  
3. Cart items and inventory levels are verified  
4. If stock is available:
   - Order is created
   - Inventory is deducted
   - Cart is cleared
5. If stock is unavailable:
   - Transaction is rolled back
   - User receives an error response
6. Confirmation email is sent asynchronously via Celery  

This guarantees **data consistency and reliability** under concurrency.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|--------|------------|--------|
| Backend Framework | Django & DRF | Core API and business logic |
| Database | PostgreSQL 15 | Reliable relational data storage |
| Transactions | Atomic DB Transactions | Prevent race conditions |
| Async Tasks | Celery & Redis | Email sending & background jobs |
| Authentication | JWT (Djoser) | Secure, stateless authentication |
| API Docs | Swagger / OpenAPI | Interactive API documentation |

---

## 📂 Project Structure

```bash
ecommerce_catalogue/
├── config/             # Project settings and URL routing
├── catalogue/          # Products, brands, and categories
├── cart/               # Shopping cart logic
├── orders/             # Order processing & transactions
│   ├── tasks.py        # Celery background jobs
│   └── views.py        # Atomic checkout logic
├── docker-compose.yml  # Container orchestration
└── requirements.txt    # Python dependencies

🔌 API Endpoints
Feature	Method	Endpoint	Description
API Docs	GET	/api/docs/	Swagger UI
Auth	POST	/auth/jwt/create/	Obtain JWT tokens
Products	GET	/api/v1/catalogue/products/	List products
Cart	POST	/api/v1/cart/	Add items to cart
Orders	POST	/api/v1/orders/	Checkout & lock inventory

🏁 Getting Started
1️⃣ Clone & Run with Docker
git clone https://github.com/WANDART291/ecommerce_catalogue.git
cd ecommerce_catalogue
docker compose up --build

2️⃣ Environment Variables (Optional)

Create a .env file in the project root:

POSTGRES_DB=ecommerce_nexus
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin123
DB_HOST=db
REDIS_HOST=redis

SECRET_KEY=your-secret-key-here
3️⃣ Database Setup
bash
Copy code
# Run migrations
docker compose exec web python manage.py migrate

# Create admin user
docker compose exec web python manage.py createsuperuser
🌐 Access Points
API Root: http://localhost:8000/api/v1/

Swagger Docs: http://localhost:8000/api/docs/

Admin Panel: http://localhost:8000/admin/

🧪 Testing
The project includes tests covering:

Model integrity

API behavior

Transaction safety

Run tests with:

docker compose exec web python manage.py test catalogue


docker compose exec web python manage.py test catalogue
👨‍💻 Author
Wandile Khanyile
Built with production-readiness in mind 🚀
