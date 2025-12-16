# 🛒 Ecommerce Catalogue API

**A production-grade, transactional E-commerce backend built for reliability and scale.**

[![Django](https://img.shields.io/badge/Django-5.0-green)](https://www.djangoproject.com/) [![DRF](https://img.shields.io/badge/DRF-3.14-red)](https://www.django-rest-framework.org/) [![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-lightgrey)](https://www.postgresql.org/)

## 🚀 Project Overview

**Ecommerce Catalogue** is a headless backend API designed to power modern online marketplaces. It goes beyond simple CRUD operations to handle the complex business logic required for real-world commerce, including recursive categorization, inventory concurrency, and asynchronous notifications.

**Key Problem Solved:** Preventing "overselling" during high-traffic events (e.g., Black Friday) by utilizing atomic database transactions to lock inventory at the exact moment of purchase.

## ⚡ System Architecture

### Order Processing Workflow
This diagram illustrates how the system safely handles checkout requests using Atomic Transactions and Async Workers.

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

🛠️ Technology StackComponentTechnologyDescriptionCore FrameworkDjango & DRFThe brain of the application.DatabasePostgreSQL 15Relational storage for products, orders, and users.ConcurrencyAtomic TransactionsEnsures Order creation and Inventory deduction happen simultaneously.Async TasksCelery & RedisOffloads email sending and maintenance tasks.DocsSwagger / OpenAPIAutomated, interactive API documentation.AuthJWT (Djoser)Secure, stateless authentication.📂 Project StructureBashecommerce_catalogue/
├── config/             # Project settings and main URL routing
├── catalogue/          # Product, Brand, and Category management
├── cart/               # Shopping cart logic
├── orders/             # Transactional logic & Celery tasks
│   ├── tasks.py        # Email & background jobs
│   └── views.py        # Atomic inventory deduction logic
├── docker-compose.yml  # Container orchestration
└── requirements.txt    # Python dependencies
🔌 API ReferenceFeatureMethodEndpointDescriptionDocsGET/api/docs/Interactive Swagger UI (Start here!)AuthPOST/auth/jwt/create/Login and obtain access/refresh tokens.CatalogGET/api/v1/catalogue/products/List products with filtering and search.CartPOST/api/v1/cart/Add items to the shopping cart.OrdersPOST/api/v1/orders/Checkout. Converts Cart to Order & locks stock.🏁 Getting Started1. Clone & BuildBashgit clone https://github.com/WANDART291/ecommerce_catalogue.git
cd ecommerce_catalogue
docker compose up --build
2. Environment ConfigurationCreate a .env file in the root directory (optional, defaults provided in Docker):Code snippetPOSTGRES_DB=ecommerce_nexus
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin123
DB_HOST=db
REDIS_HOST=redis
SECRET_KEY=your-secret-key-here
3. Setup DatabaseBash# Apply migrations
docker compose exec web python manage.py migrate

# Create a superuser for the Admin Panel
docker compose exec web python manage.py createsuperuser
4. Access the AppAPI Root: http://localhost:8000/api/v1/Swagger Docs: http://localhost:8000/api/docs/Admin Panel: http://localhost:8000/admin/🧪 TestingThe project includes a comprehensive test suite covering model integrity, API responses, and concurrency checks.Bashdocker compose exec web python manage.py test catalogue
Developed by Wandile Khanyile. Ready for production deployment 🚀
