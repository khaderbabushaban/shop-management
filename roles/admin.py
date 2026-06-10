"""
roles/admin.py
--------------
Business logic for the Admin role.
Receives a DBModel instance at construction; has no I/O of its own.
"""

from db.models import DBModel
from utils.logger import logger


class Admin:
    """Encapsulates all admin-level operations."""

    def __init__(self, username: str, db_model: DBModel):
        self.username = username
        self._db = db_model

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def add_section(self, section_name: str) -> int:
        section_id = self._db.create_section(section_name)
        print(f"  ✔ Section '{section_name}' added (ID {section_id}).")
        return section_id

    def remove_section(self, section_id: int) -> None:
        self._db.remove_section(section_id)
        print(f"  ✔ Section ID {section_id} removed.")

    def view_all_sections(self) -> None:
        sections = self._db.get_all_sections()
        if not sections:
            print("  No sections found.")
            return
        print(f"\n  {'ID':<6} {'Section Name'}")
        print(f"  {'-'*6} {'-'*30}")
        for row in sections:
            print(f"  {row['section_id']:<6} {row['section_name']}")

    # ------------------------------------------------------------------
    # Items
    # ------------------------------------------------------------------

    def add_item(self, item_name: str, section_id: int) -> int:
        item_id = self._db.create_item(item_name, section_id)
        print(f"  ✔ Item '{item_name}' added (ID {item_id}) to section ID {section_id}.")
        return item_id

    def remove_item(self, item_id: int) -> None:
        self._db.remove_item(item_id)
        print(f"  ✔ Item ID {item_id} removed.")

    def view_all_items(self) -> None:
        items = self._db.get_all_items()
        if not items:
            print("  No items found.")
            return
        print(f"\n  {'ID':<6} {'Item Name':<20} {'Section':<20} {'Seller':<20} {'Salary'}")
        print(f"  {'-'*6} {'-'*20} {'-'*20} {'-'*20} {'-'*10}")
        for row in items:
            print(
                f"  {row['item_id']:<6} {row['item_name']:<20} "
                f"{row['section_name']:<20} {row['seller_name']:<20} {row['salary']}"
            )

    def view_product_details(self, item_id: int) -> None:
        details = self._db.get_product_details(item_id)
        if not details:
            print(f"  No product found with ID {item_id}.")
            return
        print(f"\n  Product ID   : {details['item_id']}")
        print(f"  Name         : {details['item_name']}")
        print(f"  Section      : {details['section_name']}")
        print(f"  Seller       : {details['seller_name']}")
        print(f"  Seller Salary: {details['salary']}")

    def search_product(self, item_name: str) -> None:
        results = self._db.search_product(item_name)
        if not results:
            print("  No matching products found.")
            return
        print(f"\n  {'ID':<6} {'Item Name':<20} {'Section':<20} {'Seller':<20} {'Salary'}")
        print(f"  {'-'*6} {'-'*20} {'-'*20} {'-'*20} {'-'*10}")
        for row in results:
            print(
                f"  {row['item_id']:<6} {row['item_name']:<20} "
                f"{row['section_name']:<20} {row['seller_name']:<20} {row['salary']}"
            )

    # ------------------------------------------------------------------
    # Sellers
    # ------------------------------------------------------------------

    def add_seller(self, seller_name: str, section_id: int, salary: float) -> int:
        seller_id = self._db.create_seller(seller_name, section_id, salary)
        print(f"  ✔ Seller '{seller_name}' added (ID {seller_id}) to section ID {section_id}.")
        return seller_id

    def remove_seller(self, seller_id: int) -> None:
        self._db.remove_seller(seller_id)
        print(f"  ✔ Seller ID {seller_id} removed.")

    def view_all_sellers(self) -> None:
        sellers = self._db.get_all_sellers()
        if not sellers:
            print("  No sellers found.")
            return
        print(f"\n  {'ID':<6} {'Seller Name':<20} {'Section':<20} {'Salary'}")
        print(f"  {'-'*6} {'-'*20} {'-'*20} {'-'*10}")
        for row in sellers:
            print(
                f"  {row['seller_id']:<6} {row['seller_name']:<20} "
                f"{row['section_name']:<20} {row['salary']}"
            )
