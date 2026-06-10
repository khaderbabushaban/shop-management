"""
main.py
-------
Entry point for the Shop Management System CLI.

Responsibilities
----------------
* Present menus and collect user input.
* Validate all input before passing it to role objects.
* Delegate all business logic to roles (Admin / Seller / Customer).
* Delegate all database access to DBModel.

Run
---
    python main.py
"""

import sys

from config.settings import DatabaseConfig
from db.connection import DBConnection
from db.models import DBModel
from roles.admin import Admin
from roles.seller import Seller
from roles.customer import Customer
from utils.logger import logger
from utils.validators import (
    is_non_empty,
    is_valid_email,
    is_min_length,
    parse_int,
    parse_float,
)


# ---------------------------------------------------------------------------
# Helper: validated input prompt
# ---------------------------------------------------------------------------

def _prompt(message: str) -> str:
    """Read a line of input, stripping leading/trailing whitespace."""
    return input(message).strip()


def _prompt_int(message: str, field_name: str = "Value") -> int | None:
    """Prompt for a positive integer; returns None and prints error on failure."""
    raw = _prompt(message)
    value, error = parse_int(raw, field_name)
    if error:
        print(f"  ✘ {error}")
    return value


def _prompt_float(message: str, field_name: str = "Value") -> float | None:
    """Prompt for a positive float; returns None and prints error on failure."""
    raw = _prompt(message)
    value, error = parse_float(raw, field_name)
    if error:
        print(f"  ✘ {error}")
    return value


# ---------------------------------------------------------------------------
# Sign-up / Log-in flows
# ---------------------------------------------------------------------------

def handle_signup(db: DBModel) -> None:
    """Register a new customer account with validated inputs."""
    print("\n  ─── Sign Up ───")

    # Username
    username = _prompt("  Username: ")
    ok, err = is_non_empty(username, "Username")
    if not ok:
        print(f"  ✘ {err}")
        return
    ok, err = is_min_length(username, 3, "Username")
    if not ok:
        print(f"  ✘ {err}")
        return

    # Password
    password = _prompt("  Password: ")
    ok, err = is_min_length(password, 6, "Password")
    if not ok:
        print(f"  ✘ {err}")
        return

    # Email
    email = _prompt("  Email: ")
    ok, err = is_valid_email(email)
    if not ok:
        print(f"  ✘ {err}")
        return

    try:
        customer_id = db.signup_customer(username, password, email)
        print(f"  ✔ Account created! Your customer ID is {customer_id}.")
    except Exception as exc:
        logger.error("Sign-up failed: %s", exc)
        print("  ✘ Sign-up failed. The username may already be taken.")


def handle_login(db: DBModel) -> tuple[str | None, str | None]:
    """
    Authenticate a user.
    Returns (username, user_type) on success or (None, None) on failure.
    """
    print("\n  ─── Login ───")
    username = _prompt("  Username: ")
    password = _prompt("  Password: ")

    if not username or not password:
        print("  ✘ Username and password are required.")
        return None, None

    try:
        user_type = db.login_user(username, password)
    except Exception as exc:
        logger.error("Login error: %s", exc)
        print("  ✘ An error occurred during login. Please try again.")
        return None, None

    if user_type:
        print(f"  ✔ Welcome, {username}! Logged in as {user_type}.")
        return username, user_type

    print("  ✘ Incorrect username or password.")
    return None, None


# ---------------------------------------------------------------------------
# Role menus
# ---------------------------------------------------------------------------

def admin_menu(admin: Admin) -> None:
    options = {
        "1": "Add Section",
        "2": "Remove Section",
        "3": "Add Item",
        "4": "Remove Item",
        "5": "Add Seller",
        "6": "Remove Seller",
        "7": "View All Sections",
        "8": "View All Items",
        "9": "View All Sellers",
        "10": "Search Product",
        "11": "View Product Details",
        "0": "Logout",
    }

    while True:
        print("\n  ═══ Admin Menu ═══")
        for key, label in options.items():
            print(f"  {key:>2}. {label}")
        choice = _prompt("  Choice: ")

        if choice == "1":
            name = _prompt("  Section name: ")
            ok, err = is_non_empty(name, "Section name")
            if not ok:
                print(f"  ✘ {err}")
            else:
                admin.add_section(name)

        elif choice == "2":
            sid = _prompt_int("  Section ID to remove: ", "Section ID")
            if sid:
                confirm = _prompt(f"  Delete section ID {sid}? (y/n): ")
                if confirm.lower() == "y":
                    admin.remove_section(sid)

        elif choice == "3":
            name = _prompt("  Item name: ")
            ok, err = is_non_empty(name, "Item name")
            if not ok:
                print(f"  ✘ {err}")
                continue
            sid = _prompt_int("  Section ID: ", "Section ID")
            if sid:
                admin.add_item(name, sid)

        elif choice == "4":
            iid = _prompt_int("  Item ID to remove: ", "Item ID")
            if iid:
                confirm = _prompt(f"  Delete item ID {iid}? (y/n): ")
                if confirm.lower() == "y":
                    admin.remove_item(iid)

        elif choice == "5":
            name = _prompt("  Seller name: ")
            ok, err = is_non_empty(name, "Seller name")
            if not ok:
                print(f"  ✘ {err}")
                continue
            sid = _prompt_int("  Section ID: ", "Section ID")
            if not sid:
                continue
            salary = _prompt_float("  Salary: ", "Salary")
            if salary:
                admin.add_seller(name, sid, salary)

        elif choice == "6":
            slid = _prompt_int("  Seller ID to remove: ", "Seller ID")
            if slid:
                confirm = _prompt(f"  Delete seller ID {slid}? (y/n): ")
                if confirm.lower() == "y":
                    admin.remove_seller(slid)

        elif choice == "7":
            admin.view_all_sections()
        elif choice == "8":
            admin.view_all_items()
        elif choice == "9":
            admin.view_all_sellers()

        elif choice == "10":
            term = _prompt("  Search term: ")
            ok, err = is_non_empty(term, "Search term")
            if not ok:
                print(f"  ✘ {err}")
            else:
                admin.search_product(term)

        elif choice == "11":
            iid = _prompt_int("  Item ID: ", "Item ID")
            if iid:
                admin.view_product_details(iid)

        elif choice == "0":
            print(f"  Goodbye, {admin.username}!")
            break
        else:
            print("  ✘ Invalid choice. Please try again.")


def seller_menu(seller: Seller) -> None:
    options = {
        "1": "View Assigned Items",
        "2": "Update Item Price",
        "3": "Update Item Quantity",
        "4": "View Orders",
        "0": "Logout",
    }

    while True:
        print("\n  ═══ Seller Menu ═══")
        for key, label in options.items():
            print(f"  {key}. {label}")
        choice = _prompt("  Choice: ")

        if choice == "1":
            seller.view_assigned_items()

        elif choice == "2":
            iid = _prompt_int("  Item ID: ", "Item ID")
            if not iid:
                continue
            price = _prompt_float("  New price: ", "Price")
            if price:
                seller.update_item_price(iid, price)

        elif choice == "3":
            iid = _prompt_int("  Item ID: ", "Item ID")
            if not iid:
                continue
            qty = _prompt_int("  New quantity: ", "Quantity")
            if qty:
                seller.update_item_quantity(iid, qty)

        elif choice == "4":
            seller.view_orders()

        elif choice == "0":
            print(f"  Goodbye, {seller.username}!")
            break
        else:
            print("  ✘ Invalid choice. Please try again.")


def customer_menu(customer: Customer) -> None:
    options = {
        "1": "View Available Products",
        "2": "Purchase a Product",
        "3": "View Past Orders",
        "0": "Logout",
    }

    while True:
        print("\n  ═══ Customer Menu ═══")
        for key, label in options.items():
            print(f"  {key}. {label}")
        choice = _prompt("  Choice: ")

        if choice == "1":
            customer.view_available_products()

        elif choice == "2":
            iid = _prompt_int("  Item ID: ", "Item ID")
            if not iid:
                continue
            qty = _prompt_int("  Quantity: ", "Quantity")
            if qty:
                customer.purchase_product(iid, qty)

        elif choice == "3":
            customer.view_past_orders()

        elif choice == "0":
            print(f"  Goodbye, {customer.username}!")
            break
        else:
            print("  ✘ Invalid choice. Please try again.")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 50)
    print("  Welcome to the Shop Management System")
    print("=" * 50)

    # Establish database connection once for the entire session
    try:
        conn = DBConnection()
        db = DBModel(conn)
    except Exception:
        print("\n  ✘ Cannot connect to the database. Check your .env settings.")
        sys.exit(1)

    try:
        while True:
            print("\n  ─── Main Menu ───")
            print("  1. Sign Up")
            print("  2. Login")
            print("  0. Exit")
            choice = _prompt("  Choice: ")

            if choice == "1":
                handle_signup(db)

            elif choice == "2":
                username, user_type = handle_login(db)
                if user_type == "admin":
                    admin_menu(Admin(username, db))

                elif user_type == "seller":
                    seller_menu(Seller(username, db))

                elif user_type == "customer":
                    # Fetch customer_id so purchase/order queries work correctly
                    customer_id = db.get_customer_id(username)
                    if not customer_id:
                        print("  ✘ Customer record not found. Please contact support.")
                        continue
                    customer_menu(Customer(username, customer_id, db))

            elif choice == "0":
                print("\n  Exiting... Goodbye!")
                break
            else:
                print("  ✘ Invalid choice. Please try again.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
