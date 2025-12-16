# 🛒 Ecommerce Catalogue API

A **production-grade, transactional E-commerce backend** built for **reliability, scalability, and data consistency**.

**Tech Stack:** Django · Django REST Framework · PostgreSQL · Docker · Celery · Redis

---

## 🚀 Project Overview

**Ecommerce Catalogue API** is a **headless backend system** designed to power modern online marketplaces.

It goes beyond basic CRUD operations to handle **real-world commerce requirements**, including:

- Recursive product categorization  
- Flexible product variant modeling  
- Safe inventory management under concurrency  
- Transactional checkout processing  
- Asynchronous background tasks  

The system is designed with **production reliability** as a first-class concern.

---

## 🎯 Key Problem Solved

### Preventing Overselling Under High Traffic

During peak traffic events (e.g. flash sales or Black Friday), multiple customers may attempt to purchase the same product simultaneously.

This backend prevents **overselling** by:

- Using **atomic database transactions**
- Locking inventory rows during checkout
- Ensuring order creation and stock deduction occur **as a single operation**

If inventory is insufficient, the transaction is automatically rolled back.

---

## ⚙️ Order Processing Flow (Conceptual)

1. User submits a checkout request  
2. Server opens a database transaction  
3. Cart items and inventory levels are validated  
4. If stock is available:
   - Order is created
   - Inventory is deducted
   - Cart is cleared
5. If stock is unavailable:
   - Transaction is rolled back
   - User receives an error response
6. Order confirmation email is sent asynchronously via Celery  

This approach guarantees **data integrity and consistency** under concurrency.

---

## 🗂️ ERD (Entity Relationship Diagram)

BRAND 1 ─────── ∞ PRODUCT

PRODUCT 1 ───── ∞ PRODUCT_IMAGE

PRODUCT 1 ───── ∞ PRODUCT_VARIANT

PRODUCT ∞ ───── ∞ CATEGORY
(via PRODUCT_CATEGORY)

CATEGORY 1 ───── ∞ CATEGORY
(parent → child, recursive)

PRODUCT_VARIANT ∞ ───── ∞ ATTRIBUTE_VALUE
(via VARIANT_ATTRIBUTE_VALUE)

ATTRIBUTE 1 ───── ∞ ATTRIBUTE_VALUE


### ERD Notes

- A **Brand** can have many **Products**
- **Products** can belong to multiple **Categories**
- **Categories** support recursive parent–child relationships
- Each **Product** can have multiple **Variants**
- Variants are defined by **attribute combinations** (e.g. Size, Color)
- Inventory is tracked at the **variant level**
- Products support multiple images with ordering

This schema supports **scalable catalog modeling** and **safe transactional operations**.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|---------|------------|---------|
| Backend Framework | Django & DRF | Core API and business logic |
| Database | PostgreSQL 15 | Relational data storage |
| Transactions | Atomic DB Transactions | Prevent race conditions |
| Async Tasks | Celery & Redis | Background jobs & email delivery |
| Authentication | JWT (Djoser) | Secure, stateless authentication |
| API Docs | Swagger / OpenAPI | Interactive API documentation |

---

## 📂 Project Structure

```bash
ecommerce_catalogue/
├── config/             # Project settings and URL routing
├── catalogue/          # Products, brands, categories, attributes
├── cart/               # Shopping cart logic
├── orders/             # Order processing & transactional logic
│   ├── tasks.py        # Celery background jobs
│   └── views.py        # Atomic checkout implementation
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
# Apply migrations
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

👨‍💻 Author

Wandile Khanyile
Built with production-ready backend principles 🚀
