🛒 Ecommerce Nexus API

A production-grade, headless E-commerce backend built for reliability, concurrency safety, and seamless payments.








🚀 Project Overview

Ecommerce Nexus is a RESTful API designed to power modern online marketplaces.

Unlike basic tutorials, this system handles the complexities of real-world commerce:

high-concurrency inventory locking

payment gateway integration

asynchronous task processing

It is built as a Headless API, meaning it can serve any frontend (React, Next.js, Vue, Flutter, etc).

🌟 Key Features

📦 Product Catalogue
Recursive categories, brand management, and product variants (size, color)

🛒 Smart Cart
Persistent carts with stock validation + merging logic

💳 Chapa Payments
Payment initiation + verification + webhook callbacks

⚡ Celery + Redis
For async background tasks (email receipts, payment checks)

🛡️ Concurrency Safety
Atomic DB transactions to prevent overselling during high-traffic events

🎯 Distributed Architecture
1. Solving the “Overselling” Problem

Scenario:
Two users try to order the last pair of sneakers at the exact same time.

Solution implemented:

Pessimistic row-level locking using PostgreSQL + transaction.atomic

prevents race conditions on inventory rows

concurrent requests wait or fail gracefully

2. Payment Flow (Chapa)

User submits checkout

API calculates totals and requests payment session from Chapa

User completes payment on Chapa

Chapa redirects to API callback

API verifies reference

Order status updated → async receipt email sent

🛠 Tech Stack
Component	Technology	Purpose
Framework	Django + DRF	API Logic
Auth	JWT (SimpleJWT)	Stateless authentication
Database	PostgreSQL 15	Relational storage
Cache/Broker	Redis	Caching + message queue
Workers	Celery	Async tasks/receipts
Payments	Chapa API	Payment provider
Infrastructure	Docker + Compose	Container orchestration
📂 Project Structure
ecommerce_catalogue/
├── config/                 # Settings, URLs, WSGI
├── catalogue/              # Product + category + variants
├── cart/                   # Cart + cart items
├── orders/                 # Order + payment logic
│   ├── tasks.py            # Celery tasks for receipt emails
│   └── views.py            # Payment verification + transactions
├── docker-compose.yml      # Redis + DB + Celery + Web
└── requirements.txt        # Python dependencies

🏁 Getting Started
🔧 Prerequisites

Docker Desktop installed

Git installed

1️⃣ Clone the Repo
git clone https://github.com/YOUR_GITHUB_USERNAME/ecommerce_catalogue.git
cd ecommerce_catalogue

2️⃣ Run With Docker

This spins up Django + PostgreSQL + Redis + Celery automatically.

docker compose up --build

3️⃣ Create Superuser
docker compose exec web python manage.py createsuperuser

🔌 API Endpoints (Quick Reference)
Method	Endpoint	Description
GET	/api/docs/	Swagger + ReDocs
GET	/api/v1/catalogue/products/	List products
POST	/api/v1/cart/	Create shopping cart
POST	/api/v1/orders/	Place order + inventory lock
POST	/api/v1/payment/initiate/{id}/	Initiate Chapa payment
GET	/api/v1/payment/verify/{ref}/	Verify payment + send receipt
🧪 Testing

Run automated test suite inside Docker container:

docker compose exec web python manage.py test

👨‍💻 Author

Wandile Khanyile – Backend Developer

Built with Django, Docker, and coffee ☕