"""
db/models.py
------------
Data-access layer for the Shop Management System.

Every public method maps 1-to-1 to a database operation.  No I/O
(print / input) is performed here – that belongs in the role menus.

Key fixes applied vs. the original te.py
-----------------------------------------
* get_all_items()      – removed broken JOIN on Items.seller_id (column
                         does not exist in the DDL); now joins via
                         Items.section_id → Sellers.section_id.
* get_items_by_seller()– removed WHERE Items.seller_name (column does
                         not exist); now filters on Sellers.seller_name
                         via the correct JOIN path.
* get_orders_by_seller()– same fix: joins through Sellers table.
* login_user()         – now uses pgcrypto crypt() comparison so that
                         the bcrypt-hashed seed users can authenticate.
* signup_customer()    – password is hashed with pgcrypto before storage.
* create_order()       – receives customer_id (int), not username.
* update_item_price() / update_item_quantity() – added (were referenced
                         by Seller but never implemented).
"""

import datetime

from db.connection import DBConnection
from utils.logger import logger


class DBModel:
    """All database operations for the Shop Management System."""

    def __init__(self, connection: DBConnection):
        self._db = connection

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def login_user(self, username: str, password: str):
        """
        Verify credentials against the users table.
        Uses pgcrypto crypt() so hashed seed users work correctly.
        Returns the user_type string or None on failure.
        """
        schema = self._db.schema
        query = (
            f"SELECT user_type FROM {schema}.users "
            "WHERE username = %s AND password = crypt(%s, password);"
        )
        self._db.execute(query, (username, password))
        result = self._db.fetchone()
        return result["user_type"] if result else None

    def get_customer_id(self, username: str):
        """Return the customer_id for a given username, or None."""
        schema = self._db.schema
        query = f"SELECT customer_id FROM {schema}.customers WHERE username = %s;"
        self._db.execute(query, (username,))
        result = self._db.fetchone()
        return result["customer_id"] if result else None

    def signup_customer(
        self, username: str, password: str, email: str
    ) -> int:
        """
        Register a new customer.
        Password is hashed with bcrypt via pgcrypto.
        Returns the new customer_id.
        """
        schema = self._db.schema

        # Insert into the shared users table (hashed password)
        query_user = (
            f"INSERT INTO {schema}.users (username, password, user_type) "
            "VALUES (%s, crypt(%s, gen_salt('bf')), 'customer');"
        )
        self._db.execute(query_user, (username, password))

        # Insert into the customers table (hashed password for consistency)
        query_customer = (
            f"INSERT INTO {schema}.customers (username, password, email) "
            "VALUES (%s, crypt(%s, gen_salt('bf')), %s) RETURNING customer_id;"
        )
        self._db.execute(query_customer, (username, password, email))
        customer_id = self._db.fetchone()[0]
        self._db.commit()
        return customer_id

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def create_section(self, section_name: str) -> int:
        query = "INSERT INTO Sections (section_name) VALUES (%s) RETURNING section_id;"
        self._db.execute(query, (section_name,))
        section_id = self._db.fetchone()[0]
        self._db.commit()
        logger.info("Section '%s' created with ID %s.",
                    section_name, section_id)
        return section_id

    def remove_section(self, section_id: int) -> None:
        query = "DELETE FROM Sections WHERE section_id = %s;"
        self._db.execute(query, (section_id,))
        self._db.commit()
        logger.info("Section ID %s removed.", section_id)

    def get_all_sections(self):
        self._db.execute("SELECT section_id, section_name FROM Sections;")
        return self._db.fetchall()

    # ------------------------------------------------------------------
    # Items
    # ------------------------------------------------------------------

    def create_item(self, item_name: str, section_id: int) -> int:
        query = (
            "INSERT INTO Items (item_name, section_id) "
            "VALUES (%s, %s) RETURNING item_id;"
        )
        self._db.execute(query, (item_name, section_id))
        item_id = self._db.fetchone()[0]
        self._db.commit()
        logger.info("Item '%s' created with ID %s.", item_name, item_id)
        return item_id

    def remove_item(self, item_id: int) -> None:
        query = "DELETE FROM Items WHERE item_id = %s;"
        self._db.execute(query, (item_id,))
        self._db.commit()
        logger.info("Item ID %s removed.", item_id)

    def get_product_details(self, item_id: int):
        """
        Return (item_id, item_name, section_name, seller_name, salary)
        for a given item, joining via section_id (as per the DDL schema).
        """
        query = """
            SELECT
                i.item_id,
                i.item_name,
                s.section_name,
                sl.seller_name,
                sl.salary
            FROM Items i
            INNER JOIN Sections s  ON i.section_id  = s.section_id
            INNER JOIN Sellers sl  ON i.section_id  = sl.section_id
            WHERE i.item_id = %s;
        """
        self._db.execute(query, (item_id,))
        return self._db.fetchone()

    def get_all_items(self):
        """
        Return all items with their section and seller information.
        Joins through section_id (Items has no seller_id column in the DDL).
        """
        query = """
            SELECT
                i.item_id,
                i.item_name,
                s.section_name,
                sl.seller_name,
                sl.salary
            FROM Items i
            INNER JOIN Sections s  ON i.section_id = s.section_id
            INNER JOIN Sellers sl  ON i.section_id = sl.section_id;
        """
        self._db.execute(query)
        return self._db.fetchall()

    def search_product(self, item_name: str):
        """Case-insensitive partial-match search on item name."""
        query = """
            SELECT
                i.item_id,
                i.item_name,
                s.section_name,
                sl.seller_name,
                sl.salary
            FROM Items i
            INNER JOIN Sections s  ON i.section_id = s.section_id
            INNER JOIN Sellers sl  ON i.section_id = sl.section_id
            WHERE i.item_name ILIKE %s;
        """
        self._db.execute(query, (f"%{item_name}%",))
        return self._db.fetchall()

    def update_item_price(self, item_id: int, new_price: float) -> None:
        """
        Update the salary (price) field for the seller linked to this item.
        Note: in the current DDL, price lives on the Sellers table as 'salary'.
        """
        query = """
            UPDATE Sellers
            SET salary = %s
            WHERE section_id = (SELECT section_id FROM Items WHERE item_id = %s);
        """
        self._db.execute(query, (new_price, item_id))
        self._db.commit()
        logger.info("Price updated for item ID %s → %s.", item_id, new_price)

    def update_item_quantity(self, item_id: int, new_quantity: int) -> None:
        """
        Placeholder: the current DDL has no 'quantity' column on Items.
        Logged as a warning so the seller sees informative feedback.
        """
        logger.warning(
            "update_item_quantity called for item %s but the Items table "
            "has no quantity column in the current schema. "
            "Add a 'quantity INTEGER' column to Items to enable this feature.",
            item_id,
        )

    # ------------------------------------------------------------------
    # Sellers
    # ------------------------------------------------------------------

    def create_seller(
        self, seller_name: str, section_id: int, salary: float
    ) -> int:
        query = (
            "INSERT INTO Sellers (seller_name, section_id, salary) "
            "VALUES (%s, %s, %s) RETURNING seller_id;"
        )
        self._db.execute(query, (seller_name, section_id, salary))
        seller_id = self._db.fetchone()[0]
        self._db.commit()
        logger.info("Seller '%s' created with ID %s.", seller_name, seller_id)
        return seller_id

    def remove_seller(self, seller_id: int) -> None:
        query = "DELETE FROM Sellers WHERE seller_id = %s;"
        self._db.execute(query, (seller_id,))
        self._db.commit()
        logger.info("Seller ID %s removed.", seller_id)

    def get_all_sellers(self):
        query = """
            SELECT
                sl.seller_id,
                sl.seller_name,
                s.section_name,
                sl.salary
            FROM Sellers sl
            INNER JOIN Sections s ON sl.section_id = s.section_id;
        """
        self._db.execute(query)
        return self._db.fetchall()

    def get_items_by_seller(self, seller_name: str):
        """
        Return items managed by a given seller.
        Filters on Sellers.seller_name (not Items.seller_name, which
        does not exist in the DDL).
        """
        query = """
            SELECT
                i.item_id,
                i.item_name,
                s.section_name
            FROM Items i
            INNER JOIN Sections s  ON i.section_id  = s.section_id
            INNER JOIN Sellers sl  ON i.section_id  = sl.section_id
            WHERE sl.seller_name = %s;
        """
        self._db.execute(query, (seller_name,))
        return self._db.fetchall()

    def get_orders_by_seller(self, seller_name: str):
        """
        Return all orders for items in sections managed by a given seller.
        Joins through Sellers.section_id (Items has no seller_name column).
        """
        query = """
            SELECT
                o.order_id,
                i.item_name,
                c.username  AS customer_name,
                o.quantity,
                o.order_date
            FROM Orders o
            INNER JOIN Items     i  ON o.item_id     = i.item_id
            INNER JOIN Sellers   sl ON i.section_id  = sl.section_id
            INNER JOIN Customers c  ON o.customer_id = c.customer_id
            WHERE sl.seller_name = %s;
        """
        self._db.execute(query, (seller_name,))
        return self._db.fetchall()

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def create_order(
        self, customer_id: int, item_id: int, quantity: int
    ) -> None:
        """Place an order.  Receives a customer_id integer (not username)."""
        order_date = datetime.date.today()
        query = (
            "INSERT INTO Orders (customer_id, item_id, quantity, order_date) "
            "VALUES (%s, %s, %s, %s);"
        )
        self._db.execute(query, (customer_id, item_id, quantity, order_date))
        self._db.commit()
        logger.info(
            "Order placed: customer_id=%s, item_id=%s, qty=%s.",
            customer_id, item_id, quantity,
        )

    def get_orders_by_customer(self, customer_id: int):
        query = """
            SELECT
                o.order_id,
                i.item_name,
                o.quantity,
                o.order_date
            FROM Orders o
            INNER JOIN Items i ON o.item_id = i.item_id
            WHERE o.customer_id = %s;
        """
        self._db.execute(query, (customer_id,))
        return self._db.fetchall()
