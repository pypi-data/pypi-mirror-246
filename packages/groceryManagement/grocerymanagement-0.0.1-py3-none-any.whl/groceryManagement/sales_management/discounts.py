# discounts.py

class DiscountManager:
    """Manages discounts for products in the supermarket.

    This manager allows the addition, removal, and application of discounts
    to products. Discounts are stored as a percentage off the original price
    and are applied when calculating the final sale price of an item.

    Attributes:
        discounts (dict): A dictionary mapping product IDs to their respective
                          discount rates.
    """
    def __init__(self):
        """Initializes the DiscountManager with an empty discounts dictionary."""
        self.discounts = {}

    def add_discount(self, product_id, discount_rate):
        """Adds a discount rate to a product.

        Args:
            product_id (str): The unique identifier for the product.
            discount_rate (float): The discount rate to apply to the product,
                                   represented as a decimal (e.g., 0.1 for 10%).

        Raises:
            ValueError: If the discount_rate is not between 0 and 1.
        """
        try:
            if not 0 <= discount_rate <= 1:
                raise ValueError("Discount rate must be between 0 and 1.")
            self.discounts[product_id] = discount_rate
        except ValueError as e:
            print(f"Error adding discount: {e}")

    def remove_discount(self, product_id):
        """Removes a previously assigned discount from a product.

        Args:
            product_id (str): The unique identifier for the product.

        Raises:
            KeyError: If the product_id is not found in the discounts dictionary.
        """
        try:
            if product_id not in self.discounts:
                raise KeyError(f"No discount found for product ID {product_id}.")
            del self.discounts[product_id]
        except KeyError as e:
            print(f"Error removing discount: {e}")
    
    def apply_discount(self, product_id, price):
        """Applies the discount rate to the given price of a product if a discount exists.

        Args:
            product_id (str): The unique identifier for the product.
            price (float): The original price of the product.

        Returns:
            float: The discounted price of the product if a discount is applied,
                   otherwise the original price.
        """
        try:
            if product_id not in self.discounts:
                return price
            return price * (1 - self.discounts[product_id])
        except Exception as e:
            print(f"Error applying discount: {e}")
            return price
