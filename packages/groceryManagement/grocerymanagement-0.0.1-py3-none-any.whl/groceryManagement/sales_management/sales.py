# sales.py

class SalesManager:
    """Manages sales records and calculates total sales in the supermarket.

    This manager allows recording individual sales transactions and provides
    a method to calculate the total sales revenue based on the recorded sales
    records.

    Attributes:
        sales_records (list): A list of dictionaries representing individual
                              sales transactions, each containing the product_id,
                              quantity, and price.
    """
    def __init__(self):
        """Initializes the SalesManager with an empty list of sales records."""
        self.sales_records = []

    def record_sale(self, product_id, quantity, price):
        """Records a sales transaction for a product.

        Args:
            product_id (str): The unique identifier for the product sold.
            quantity (int): The quantity of the product sold in this transaction.
            price (float): The price per unit of the product.

        Notes:
            This method appends a dictionary representing the sales transaction
            to the sales_records list.

        Example:
            To record the sale of 3 units of "P001" at $2.99 each:
            >>> sales_manager.record_sale("P001", 3, 2.99)
        """
        try:
            if quantity < 0 or price < 0:
                raise ValueError("Quantity and price must be non-negative.")
            self.sales_records.append({"product_id": product_id, "quantity": quantity, "price": price})
        except ValueError as e:
            print(f"Error recording sale: {e}")

    def total_sales(self):
        """Calculates the total sales revenue based on recorded sales transactions.

        Returns:
            float: The total sales revenue, which is the sum of the price * quantity
                   for all recorded sales transactions.
        """
        try:
            return sum(record['price'] * record['quantity'] for record in self.sales_records)
        except Exception as e:
            print(f"Error calculating total sales: {e}")
            return 0
