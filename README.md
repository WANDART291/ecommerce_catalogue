# 🛒 Ecommerce Nexus API

A **production-grade, headless E-commerce backend** built for **reliability, concurrency safety, and seamless payments**.

![Status](https://img.shields.io/badge/Status-Active_Development-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)

---

## 🚀 Project Overview

**Ecommerce Nexus** is a RESTful API designed to power modern online marketplaces. Unlike basic tutorials, this system handles the **complexities of real-world commerce**: high-concurrency inventory locking, payment gateway integration, and asynchronous communication.

It is built as a **Headless API**, meaning it can serve any frontend (React, Vue, Mobile Apps) indiscriminately.

### 🌟 Key Features
- **📦 Product Catalogue:** Recursive categories, brand management, and flexible product variants (Size/Color).
- **🛒 Smart Cart:** Persistent cart logic with stock validation.
- **💳 Payments (Chapa):** Integrated Chapa Payment Gateway with verification callbacks and webhook handling.
- **⚡ Async Tasks:** Uses **Celery & Redis** to handle non-blocking tasks (e.g., sending email receipts) without slowing down the server.
- **🛡️ Concurrency Safety:** Uses database transactions (`transaction.atomic`) to prevent "overselling" during high-traffic events.

---

## 🎯 The Architecture

### 1. The "Overselling" Problem & Solution
**Scenario:** Two users try to buy the last pair of sneakers at the exact same millisecond.
**Solution:** This API implements **Pessimistic Locking**. When a checkout begins, the specific inventory rows are locked in the PostgreSQL database. The second request is forced to wait or fail gracefully, ensuring inventory never drops below zero.

### 2. Payment Flow (Chapa Integration)
1. **Initiate:** User requests checkout; Server calculates total and contacts Chapa API.
2. **Redirect:** User is redirected to Chapa's secure payment page.
3. **Verify:** Upon success, Chapa redirects user back to our API.
4. **Finalize:** The API verifies the transaction reference (`tx_ref`), updates the Order status to `Completed`, and triggers an email receipt.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
|:---|:---|:---|
| **Core Framework** | Django & DRF | API Logic & ORM |
| **Database** | PostgreSQL 15 | Relational Data Storage |
| **Caching/Broker** | Redis | Caching & Task Message Broker |
| **Async Workers** | Celery | Background Task Processing (Emails) |
| **Payments** | Chapa API | Payment Gateway Integration |
| **Containerization** | Docker & Compose | Orchestration & Environment Consistency |
| **Auth** | JWT (SimpleJWT) | Stateless Authentication |

---

## 📂 Project Structure

```bash
ecommerce_catalogue/
├── config/             # Settings, URLs, and WSGI config
├── catalogue/          # Product management (Models: Product, Category, Variant)
├── cart/               # Cart logic (Models: Cart, CartItem)
├── orders/             # Transactional logic (Models: Order, Payment)
│   ├── tasks.py        # Celery tasks for async emails
│   └── views.py        # Payment verification & atomic transactions
├── docker-compose.yml  # Docker services (Web, DB, Redis, Celery)
└── requirements.txt    # Dependencies

🏁 Getting StartedPrerequisitesDocker Desktop installedGit1️⃣ Clone the RepoBashgit clone [https://github.com/YOUR_GITHUB_USERNAME/ecommerce_catalogue.git](https://github.com/YOUR_GITHUB_USERNAME/ecommerce_catalogue.git)
cd ecommerce_catalogue
2️⃣ Run with DockerThis command spins up the Django Server, PostgreSQL, Redis, and Celery Worker automatically.Bashdocker compose up --build
3️⃣ Create SuperuserOnce the containers are running, create an admin account to manage the catalogue.Bashdocker compose exec web python manage.py createsuperuser
🔌 API Endpoints (Quick Reference)MethodEndpointDescriptionGET/api/docs/Swagger UI (Full Documentation)GET/api/v1/catalogue/products/List all productsPOST/api/v1/cart/Create a shopping cartPOST/api/v1/orders/Place an order (Locks inventory)POST/api/v1/payment/initiate/{id}/Get Chapa Payment LinkGET/api/v1/payment/verify/{ref}/Verify Payment & Send Receipt🧪 TestingTo run the automated test suite inside the container:Bashdocker compose exec web python manage.py test
👨‍💻 AuthorWandile Khanyile - Backend DeveloperBuilt with Django, Docker, and Coffee ☕

