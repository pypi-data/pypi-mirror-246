import sys
sys.path.append('/Users/chenshiyi/Desktop/Data533/SupermarketManagementSystem')

from inventory_management.products import ProductManager
from inventory_management.stock import StockManager, PerishableStockManager
from sales_management.sales import SalesManager
from sales_management.discounts import DiscountManager
from utilities import *

# Initialize managers
product_manager = ProductManager()
stock_manager = StockManager()
perishable_stock_manager = PerishableStockManager()
sales_manager = SalesManager()
discount_manager = DiscountManager()

initial_products = {
    "P001": {"name": "Milk", "price": 2.99},
    "P002": {"name": "Bread", "price": 1.99},
    "P003": {"name": "Eggs", "price": 3.50},
    "P004": {"name": "Apples", "price": 0.99},
    "P005": {"name": "Chicken", "price": 5.99},
    "P006": {"name": "Orange Juice", "price": 3.99},
    "P007": {"name": "Chocolate Bar", "price": 1.50},
    "P008": {"name": "Pasta", "price": 1.20},
    "P009": {"name": "Tomato Sauce", "price": 2.50},
    "P010": {"name": "Cheese", "price": 4.50},
    "P011": {"name": "Cereal", "price": 3.40},
    "P012": {"name": "Yogurt", "price": 0.80},
    "P013": {"name": "Butter", "price": 2.50},
    "P014": {"name": "Bananas", "price": 0.60},
    "P015": {"name": "Spinach", "price": 2.00}
}
initial_stock = {
    "P001": 100,  # 100 units of Milk
    "P002": 50,   # 50 units of Bread
    "P003": 200,  # 200 units of Eggs
    "P004": 75,   # 75 units of Apples
    "P005": 40,   # 40 units of Chicken
    "P006": 80,   # 80 units of Orange Juice
    "P007": 150,  # 150 units of Chocolate Bar
    "P008": 100,  # 100 units of Pasta
    "P009": 60,   # 60 units of Tomato Sauce
    "P010": 70,   # 70 units of Cheese
    "P011": 85,   # 85 units of Cereal
    "P012": 120,  # 120 units of Yogurt
    "P013": 50,   # 50 units of Butter
    "P014": 150,  # 150 units of Bananas
    "P015": 90    # 90 units of Spinach
}
initial_sales = [
    {"product_id": "P001", "quantity": 2, "total_price": 5.98, "date": "2023-11-20"},
    {"product_id": "P004", "quantity": 5, "total_price": 4.95, "date": "2023-11-21"},
    {"product_id": "P007", "quantity": 3, "total_price": 4.50, "date": "2023-11-22"},
    {"product_id": "P010", "quantity": 1, "total_price": 4.50, "date": "2023-11-23"},
    {"product_id": "P012", "quantity": 4, "total_price": 3.20, "date": "2023-11-24"},
    {"product_id": "P015", "quantity": 2, "total_price": 4.00, "date": "2023-11-25"},
    {"product_id": "P008", "quantity": 10, "total_price": 12.00, "date": "2023-11-26"},
    
]
initial_discounts = {
    "P001": 0.10,  # 10% discount on Milk
    "P005": 0.15,  # 15% discount on Chicken
    "P006": 0.05,  # 5% discount on Orange Juice
    "P008": 0.10,  # 10% discount on Pasta
    "P011": 0.20,  # 20% discount on Cereal
    "P014": 0.07,  # 7% discount on Bananas
}

initial_perishable_stock = {
    "P012": {"quantity": 30, "expiry_date": "2023-12-31"},  # Yogurt
    "P010": {"quantity": 20, "expiry_date": "2023-11-15"},  # Cheese
    "P006": {"quantity": 15, "expiry_date": "2023-10-10"},  # Orange Juice
}

# Pre-load some data
initialize_data(product_manager, stock_manager, perishable_stock_manager, 
                sales_manager, discount_manager, initial_products, 
                initial_stock, initial_perishable_stock, initial_sales, 
                initial_discounts)

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            product_management(product_manager)
        elif choice == "2":
            stock_management(stock_manager,perishable_stock_manager)
        elif choice == "3":
            sales_management(product_manager,sales_manager)
        elif choice == "4":
            discount_management(discount_manager)
        elif choice == "5":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()