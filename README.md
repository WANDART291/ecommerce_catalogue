🛒 Ecommerce Nexus API

A production-grade, headless e-commerce backend built for reliability, concurrency safety, and seamless payments.








🚀 Project Overview

Ecommerce Nexus is a RESTful backend powering modern online marketplaces. It handles real-world commerce complexities such as:

high-concurrency inventory locking

asynchronous background task execution

secure payment workflows

Built as a Headless API, enabling frontend freedom (React, Angular, Vue, Flutter, etc).

🌟 Key Features

📦 Catalogue System — recursive product categories + variants

🛒 Smart Cart — persistent carts w/ merge + validation

💳 Payments — integrated Chapa payment gateway

⚡ Async Tasks — Celery workers with Redis broker

🛡️ Concurrency Safety — PostgreSQL row-level locks + transaction.atomic()

🎯 Core Architecture Concepts
🔐 Solving the Overselling Problem

When two customers attempt to buy the last product simultaneously:

inventory rows are locked using pessimistic locking

concurrent transactions wait or gracefully fail

ensures product stock never becomes negative

💳 Payment Flow (Chapa)

Checkout request received

Total calculated + session initiated with Chapa

Customer redirected to complete payment

Chapa redirects back with transaction reference

API verifies payment

Order marked completed + Celery sends receipt email asynchronously

🛠 Tech Stack
Component	Technology
Framework	Django + Django REST Framework
Database	PostgreSQL 15
Cache / Broker	Redis
Async Workers	Celery
Authentication	JWT (SimpleJWT)
Containerization	Docker + Docker Compose
Payment Provider	Chapa API
📂 Project Structure
ecommerce_catalogue/
├── config/                # Core settings, URLs, WSGI
├── catalogue/             # Product + category + variant models/API
├── cart/                  # Cart + cart item management
├── orders/                # Orders + payments
│   ├── tasks.py           # Celery async tasks
│   └── views.py           # Payment verification + transactions
├── docker-compose.yml     # DB + Redis + Celery + Django services
└── requirements.txt       # Python dependencies

🏁 Getting Started
🔧 Prerequisites

Docker Desktop installed

Git installed

1️⃣ Clone Repository
git clone https://github.com/YOUR_GITHUB_USERNAME/ecommerce_catalogue.git
cd ecommerce_catalogue

2️⃣ Build & Start Containers
docker compose up --build

3️⃣ Create Django Admin User
docker compose exec web python manage.py createsuperuser

🔌 API Endpoints Overview
Method	Endpoint	Description
GET	/api/docs/	Swagger + Redoc auto-docs
GET	/api/v1/catalogue/products/	List products
POST	/api/v1/cart/	Create cart
POST	/api/v1/orders/	Checkout + lock inventory
POST	/api/v1/payment/initiate/{id}/	Create Chapa payment session
GET	/api/v1/payment/verify/{ref}/	Verify Chapa payment
🧪 Run Tests
docker compose exec web python manage.py test

👨‍💻 Author

Wandile Khanyile — Backend Developer

Built with Django, DRF, Docker and ☕