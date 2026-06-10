# Shop Management System

A command-line store management application built with Python and PostgreSQL. Supports three roles — **Admin**, **Seller**, and **Customer** — each with their own menu and set of operations.

---

## Features

| Role | Capabilities |
|------|-------------|
| **Admin** | Add/remove sections, items, sellers; view all data; search products |
| **Seller** | View assigned items and orders; update item price/quantity |
| **Customer** | Browse products, purchase items, view past orders |
| **All** | Sign up (customer), login with bcrypt-hashed passwords |

---

## Technologies

- **Python 3.11+**
- **PostgreSQL** (with the `pgcrypto` extension for bcrypt password hashing)
- **psycopg2-binary** – PostgreSQL adapter
- **python-dotenv** – environment-variable management
- **pytest** – unit testing

---

## Installation

### Prerequisites

- Python 3.11 or newer
- PostgreSQL 13 or newer
- `pgcrypto` extension (included in most PostgreSQL distributions)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/khaderbabushaban/shop-management.git
cd shop-management

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_SCHEMA

# 5. Set up the database
psql -U postgres -c "CREATE DATABASE ShopManagement;"
psql -U postgres -d ShopManagement -f DDL.sql
```

---

## Database Setup

The `DDL.sql` file creates the following tables and seed data:

- `Sections` — product categories
- `Sellers` — store staff linked to sections
- `Items` — products linked to sections
- `Customers` — registered customers
- `Orders` — purchase records
- `users` — authentication table (bcrypt-hashed passwords via `pgcrypto`)

Seed users created by `DDL.sql`:

| Username | Password   | Role   |
|----------|------------|--------|
| khader   | khader123  | admin  |
| ahmed    | ahmed123   | seller |
| noor     | noor125    | seller |

---

## Usage

```bash
python main.py
```

You will be presented with:

```
==================================================
  Welcome to the Shop Management System
==================================================

  ─── Main Menu ───
  1. Sign Up
  2. Login
  0. Exit
```

---

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for a full breakdown of the codebase.

---

## Running Tests

```bash
pytest tests/ -v
```

The test suite covers input validation helpers and requires no database connection.

---

## License

[MIT](LICENSE)
