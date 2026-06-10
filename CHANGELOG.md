# Changelog

All notable changes to this project are documented here.

## [2.0.0] – Refactor Release

### Fixed
- **Critical**: `get_all_items()` was joining on `Items.seller_id` which does not exist in the schema. Fixed to join via `section_id`.
- **Critical**: `get_items_by_seller()` filtered on `Items.seller_name` (non-existent column). Fixed to join through `Sellers` table.
- **Critical**: `get_orders_by_seller()` had the same non-existent column bug. Fixed.
- **Critical**: `login_user()` compared passwords as plaintext against bcrypt-hashed values stored by the DDL seed inserts. Fixed to use `crypt(%s, password)` comparison.
- **Critical**: `signup_customer()` stored passwords in plaintext. Fixed to hash with `crypt(gen_salt('bf'))`.
- **Critical**: `create_order()` received `username` instead of `customer_id`. Fixed; `main.py` now looks up and passes the correct integer ID.
- **Bug**: `update_item_price()` and `update_item_quantity()` were called by `Seller` but never implemented. Both are now implemented (with a schema note for quantity).
- **Bug**: Double admin login — removed redundant second authentication call.
- **Bug**: `Customer` menu was not looping. All role menus now loop correctly.
- **Bug**: `int()` and `float()` calls on raw input had no error handling; app would crash on bad input. All numeric input is now validated via `parse_int` / `parse_float`.

### Added
- `config/settings.py` — centralised settings loaded from `.env` via `python-dotenv`. No credentials in source code.
- `utils/validators.py` — pure validation helpers for strings, emails, integers, floats.
- `utils/logger.py` — application-wide structured logger.
- `db/connection.py` — `DBConnection` class wrapping psycopg2 with error handling and rollback.
- `db/models.py` — clean `DBModel` class with corrected SQL queries and docstrings.
- `roles/admin.py`, `roles/seller.py`, `roles/customer.py` — separated role logic from I/O.
- `tests/test_validators.py` — offline unit tests; no database required.
- `.env.example`, `.gitignore`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `PROJECT_STRUCTURE.md`, `README.md`.

### Removed
- `te.py`, `test.py` — experimental draft files replaced by the modular structure.
- `Main.py`, `Admin.py`, `Customer.py`, `User.py`, `DBModel.py` — superseded.
- `__pycache__/` — build artefacts should not be committed.
