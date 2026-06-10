# Project Structure

```
shop_management/
│
├── main.py                  # Entry point: all CLI menus and input validation
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Loads DB config from .env
│
├── db/
│   ├── __init__.py
│   ├── connection.py        # DBConnection: psycopg2 wrapper with error handling
│   └── models.py            # DBModel: all SQL queries (data-access layer)
│
├── roles/
│   ├── __init__.py
│   ├── admin.py             # Admin class: section/item/seller operations
│   ├── seller.py            # Seller class: view items & orders, update price
│   └── customer.py          # Customer class: browse products, purchase, view orders
│
├── utils/
│   ├── __init__.py
│   ├── logger.py            # Application-wide logger
│   └── validators.py        # Input validation helpers (no I/O)
│
├── tests/
│   ├── __init__.py
│   └── test_validators.py   # Offline unit tests (no DB required)
│
├── DDL.sql                  # PostgreSQL schema + seed data
├── .env.example             # Template for environment variables
├── .gitignore
├── requirements.txt
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── PROJECT_STRUCTURE.md
└── README.md
```

## Layer responsibilities

| Layer | Package | Rules |
|-------|---------|-------|
| Presentation | `main.py` | `print`, `input`, menu loops, input validation |
| Business logic | `roles/` | Calls `DBModel`; no direct DB access |
| Data access | `db/models.py` | SQL only; no `print`/`input` |
| Infrastructure | `db/connection.py` | psycopg2 connection management |
| Cross-cutting | `utils/`, `config/` | Logging, validation, settings |
