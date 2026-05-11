# Inventory Management API

A secure and role-based Inventory Management API built using **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **JWT Authentication**.

---

## Features

- JWT Authentication (Access & Refresh Tokens)
- Role-Based Authorization
- User Management
- Category Management
- Inventory Item Management
- Secure Password Hashing using bcrypt
- Cookie-Based Authentication
- CRUD Operations
- Low Stock Tracking
- Expiring Item Tracking
- Supplier-Based Filtering
- User-Based Item Tracking
- Category-Based Item Filtering
- Structured Error Handling
- Input Validation using Pydantic
- PostgreSQL Database Integration

---

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Passlib (bcrypt)
- Python-Jose (JWT)
- Alembic

---

## Project Structure

```bash
app/
│
├── controllers/
│   ├── auth_controllers.py
│   ├── category_controllers.py
│   ├── item_controllers.py
│   └── user_controllers.py
│
├── routes/
│   ├── auth_routes.py
│   ├── category_routes.py
│   ├── items_routes.py
│   └── user_routes.py
│
├── utils/
│   ├── dependencies.py
│   └── security.py
│
├── models/
├── constants.py
├── connections.py
└── main.py
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd <project-folder>
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Environment

#### Linux / Mac

```bash
source env/bin/activate
```

#### Windows

```bash
env\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory.

```env
db_user=postgres
db_pw=your_password
db_host=localhost
db_port=5432
db_name=inventory_db

secret_key=your_secret_key
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

### Swagger UI

```bash
http://127.0.0.1:8000/docs
```

### ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

## Authentication

The application uses:

- JWT Access Token
- JWT Refresh Token
- HTTPOnly Cookies
- Role-Based Authorization

---

## Roles

| Role | Permissions |
|------|-------------|
| Admin | Full Access |
| Manager | Manage Categories & Items |
| Staff | Limited Item Access |

---

## API Endpoints

### Auth Routes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register User |
| POST | `/login` | Login User |
| POST | `/logout` | Logout User |
| POST | `/refresh` | Refresh Access Token |

---

### User Routes

| Method | Endpoint |
|---|---|
| GET | `/users` |
| GET | `/users/{user_id}` |
| PUT | `/users/{user_id}` |
| PATCH | `/users/{user_id}` |
| DELETE | `/users/{user_id}` |

---

### Category Routes

| Method | Endpoint |
|---|---|
| POST | `/categories` |
| GET | `/categories` |
| GET | `/categories/{category_id}` |
| PUT | `/categories/{category_id}` |
| PATCH | `/categories/{category_id}` |
| DELETE | `/categories/{category_id}` |

---

### Item Routes

| Method | Endpoint |
|---|---|
| POST | `/items` |
| GET | `/items` |
| GET | `/items/{item_id}` |
| PUT | `/items/{item_id}` |
| PATCH | `/items/{item_id}` |
| DELETE | `/items/{item_id}` |

---

### Additional Item APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/items/low-stock` | Retrieve Low Stock Items |
| GET | `/items/expiring-soon` | Retrieve Expiring Items |
| GET | `/items/by-supplier?supplier=name` | Filter Items by Supplier |
| GET | `/users/{user_id}/items` | Retrieve User Items |
| GET | `/categories/{category_id}/items` | Retrieve Category Items |

---

## Validations

The project includes validations for:

- Empty Fields
- Email Validation
- Password Length
- Negative Values
- Invalid Prices
- Past Expiry Dates
- Duplicate Emails
- Duplicate Categories

---

## Error Handling

Structured error responses are implemented across all routes.

### Example

```json
{
  "success": false,
  "error_code": "USER_NOT_FOUND",
  "message": "User not found"
}
```

---

## Security Features

- Password Hashing using bcrypt
- JWT Access & Refresh Tokens
- Protected Routes
- Role-Based Access Control
- Secure Cookie Authentication

---



