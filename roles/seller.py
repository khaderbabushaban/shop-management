"""
roles/seller.py
---------------
Business logic for the Seller role.
"""

from db.models import DBModel


class Seller:
    """Encapsulates all seller-level operations."""

    def __init__(self, username: str, db_model: DBModel):
        self.username = username
        self._db = db_model

    def view_assigned_items(self) -> None:
        items = self._db.get_items_by_seller(self.username)
        if not items:
            print(f"  No items assigned to seller '{self.username}'.")
            return
        print(f"\n  Items assigned to '{self.username}':")
        print(f"  {'ID':<6} {'Item Name':<20} {'Section'}")
        print(f"  {'-'*6} {'-'*20} {'-'*20}")
        for row in items:
            print(f"  {row['item_id']:<6} {row['item_name']:<20} {row['section_name']}")

    def update_item_price(self, item_id: int, new_price: float) -> None:
        details = self._db.get_product_details(item_id)
        if not details:
            print(f"  Item ID {item_id} not found.")
            return
        self._db.update_item_price(item_id, new_price)
        print(f"  ✔ Price of '{details['item_name']}' updated to {new_price}.")

    def update_item_quantity(self, item_id: int, new_quantity: int) -> None:
        details = self._db.get_product_details(item_id)
        if not details:
            print(f"  Item ID {item_id} not found.")
            return
        self._db.update_item_quantity(item_id, new_quantity)
        print(
            f"  ✔ Quantity update requested for '{details['item_name']}'. "
            "Note: quantity column not yet in schema – see logs."
        )

    def view_orders(self) -> None:
        orders = self._db.get_orders_by_seller(self.username)
        if not orders:
            print(f"  No orders found for seller '{self.username}'.")
            return
        print(f"\n  Orders for '{self.username}':")
        print(f"  {'Order ID':<10} {'Item':<20} {'Customer':<20} {'Qty':<6} {'Date'}")
        print(f"  {'-'*10} {'-'*20} {'-'*20} {'-'*6} {'-'*12}")
        for row in orders:
            print(
                f"  {row['order_id']:<10} {row['item_name']:<20} "
                f"{row['customer_name']:<20} {row['quantity']:<6} {row['order_date']}"
            )
