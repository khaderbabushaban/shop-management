"""
roles/customer.py
-----------------
Business logic for the Customer role.
"""

from db.models import DBModel


class Customer:
    """Encapsulates all customer-level operations."""

    def __init__(self, username: str, customer_id: int, db_model: DBModel):
        self.username = username
        self.customer_id = customer_id  # needed for order queries
        self._db = db_model

    def view_available_products(self) -> None:
        products = self._db.get_all_items()
        if not products:
            print("  No products available at the moment.")
            return
        print(f"\n  {'ID':<6} {'Item Name':<20} {'Section':<20} {'Seller':<20} {'Price'}")
        print(f"  {'-'*6} {'-'*20} {'-'*20} {'-'*20} {'-'*10}")
        for row in products:
            print(
                f"  {row['item_id']:<6} {row['item_name']:<20} "
                f"{row['section_name']:<20} {row['seller_name']:<20} {row['salary']}"
            )

    def purchase_product(self, item_id: int, quantity: int) -> None:
        details = self._db.get_product_details(item_id)
        if not details:
            print(f"  Product ID {item_id} not found.")
            return
        item_name = details["item_name"]
        price = details["salary"]
        total_cost = price * quantity
        print(f"\n  Item  : {item_name}")
        print(f"  Qty   : {quantity}")
        print(f"  Total : {total_cost:.2f}")
        confirm = input("  Confirm purchase? (y/n): ").strip().lower()
        if confirm == "y":
            self._db.create_order(self.customer_id, item_id, quantity)
            print(f"  ✔ Purchase successful! {quantity}× {item_name} for {total_cost:.2f}.")
        else:
            print("  Purchase cancelled.")

    def view_past_orders(self) -> None:
        orders = self._db.get_orders_by_customer(self.customer_id)
        if not orders:
            print("  You have no past orders.")
            return
        print(f"\n  {'Order ID':<10} {'Item':<20} {'Qty':<6} {'Date'}")
        print(f"  {'-'*10} {'-'*20} {'-'*6} {'-'*12}")
        for row in orders:
            print(
                f"  {row['order_id']:<10} {row['item_name']:<20} "
                f"{row['quantity']:<6} {row['order_date']}"
            )
