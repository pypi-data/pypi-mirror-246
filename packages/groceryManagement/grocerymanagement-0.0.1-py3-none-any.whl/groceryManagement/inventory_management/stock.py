# stock.py

class StockManager:
    """Manages stock inventory for non-perishable products in the supermarket.

    This manager allows adding and removing stock quantities for products.

    Attributes:
        stock (dict): A dictionary mapping product IDs to their respective stock quantities.
    """
    def __init__(self):
        """Initializes the StockManager with an empty stock dictionary."""
        self.stock = {}

    def add_stock(self, product_id, quantity):
        """Add products to the stock inventory.

        Args:
            product_id (str): The unique identifier for the product.
            quantity (int): The quantity of products to add to stock.
        """

        self.stock[product_id] = self.stock.get(product_id, 0) + quantity

    def remove_stock(self, product_id, quantity):
        if product_id not in self.stock or self.stock[product_id] < quantity:
            raise ValueError("Insufficient stock.")
        self.stock[product_id] -= quantity

class PerishableStockManager(StockManager):
    """Remove products from the stock inventory.

        Args:
            product_id (str): The unique identifier for the product.
            quantity (int): The quantity of products to remove from stock.

        Raises:
            ValueError: If there is insufficient stock for the specified quantity.
        """
    def __init__(self):
        """Initializes the PerishableStockManager with empty stock and perishable_stock dictionaries."""
        super().__init__()
        self.perishable_stock = {}

    def add_perishable_stock(self, product_id, quantity, expiry_date):
        """Add perishable products to the stock inventory.

        Args:
            product_id (str): The unique identifier for the product.
            quantity (int): The quantity of perishable products to add to stock.
            expiry_date (str): The expiry date of the perishable products.
        """
        super().add_stock(product_id, quantity)
        if product_id not in self.perishable_stock:
            self.perishable_stock[product_id] = []
        self.perishable_stock[product_id].append({'quantity': quantity, 'expiry_date': expiry_date})

    def check_expiry(self, current_date):
        """Check for expired perishable stock items.

        Args:
            current_date (str): The current date for checking expiry.

        Returns:
            dict: A dictionary mapping product IDs to the total quantity of expired items.

        """
        expired_items = {}
        for product_id, stock_items in self.perishable_stock.items():
            expired_items[product_id] = sum(item['quantity'] for item in stock_items if item['expiry_date'] < current_date)
        return expired_items

    def remove_expired_stock(self, current_date):
        """Remove expired perishable stock items.

        Args:
            current_date (str): The current date for removing expired items.

        """
        for product_id, stock_items in list(self.perishable_stock.items()):
            self.perishable_stock[product_id] = [item for item in stock_items if item['expiry_date'] >= current_date]
            if not self.perishable_stock[product_id]:
                del self.perishable_stock[product_id]
                self.stock[product_id] = 0
