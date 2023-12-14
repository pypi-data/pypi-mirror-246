# products.py

class ProductManager:
    """Manages product information in the supermarket.

    This manager allows adding, removing, and updating product information
    including product name and price.

    Attributes:
        products (dict): A dictionary mapping product IDs to their respective
                         information, including name and price.
    """

    def __init__(self):
        """Initializes the ProductManager with an empty products dictionary."""
        self.products = {}

    def add_product(self, product_id, name, price):
        """Add a new product to the product inventory.

        Args:
            product_id (str): The unique identifier for the product.
            name (str): The name of the product.
            price (float): The price of the product.

        Raises:
            ValueError: If the product_id already exists in the inventory.
        """
        if product_id in self.products:
            raise ValueError("Product ID already exists.")
        self.products[product_id] = {"name": name, "price": price}

    def remove_product(self, product_id):
        """Remove a product from the product inventory.

        Args:
            product_id (str): The unique identifier for the product to remove.

        Raises:
            KeyError: If the product_id is not found in the inventory.
        """
        if product_id not in self.products:
            raise KeyError("Product not found.")
        del self.products[product_id]

    def update_product(self, product_id, name=None, price=None):
        """Update product information for a given product.

        Args:
            product_id (str): The unique identifier for the product to update.
            name (str, optional): The new name for the product. Default is None.
            price (float, optional): The new price for the product. Default is None.

        Raises:
            KeyError: If the product_id is not found in the inventory.
        """
        if product_id not in self.products:
            raise KeyError("Product not found.")
        if name:
            self.products[product_id]['name'] = name
        if price:
            self.products[product_id]['price'] = price
