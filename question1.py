import csv
import json
from datetime import datetime
from collections import defaultdict
import os

class RetailInventorySystem:
    def __init__(self):
        self.products = []
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample product data"""
        self.products = [
            {
                'Product ID': 'P001',
                'Product Name': 'Laptop',
                'Category': 'Electronics',
                'Opening Stock': 100,
                'Units Sold': 45,
                'Units Returned': 5,
                'Supplier Lead Time': 7,
                'Unit Cost': 500,
                'Selling Price': 800
            },
            {
                'Product ID': 'P002',
                'Product Name': 'Smartphone',
                'Category': 'Electronics',
                'Opening Stock': 200,
                'Units Sold': 120,
                'Units Returned': 8,
                'Supplier Lead Time': 5,
                'Unit Cost': 300,
                'Selling Price': 500
            },
            {
                'Product ID': 'P003',
                'Product Name': 'T-Shirt',
                'Category': 'Apparel',
                'Opening Stock': 500,
                'Units Sold': 200,
                'Units Returned': 15,
                'Supplier Lead Time': 10,
                'Unit Cost': 15,
                'Selling Price': 30
            },
            {
                'Product ID': 'P004',
                'Product Name': 'Jeans',
                'Category': 'Apparel',
                'Opening Stock': 300,
                'Units Sold': 150,
                'Units Returned': 10,
                'Supplier Lead Time': 8,
                'Unit Cost': 25,
                'Selling Price': 50
            },
            {
                'Product ID': 'P005',
                'Product Name': 'Coffee Maker',
                'Category': 'Home Appliances',
                'Opening Stock': 150,
                'Units Sold': 80,
                'Units Returned': 6,
                'Supplier Lead Time': 6,
                'Unit Cost': 40,
                'Selling Price': 70
            }
        ]
    
    def calculate_current_stock(self):
        """Calculate current stock for each product"""
        for product in self.products:
            product['Current Stock'] = product['Opening Stock'] - product['Units Sold'] + product['Units Returned']
        return self.products
    
    def calculate_profit(self):
        """Calculate profit for each product"""
        for product in self.products:
            revenue = product['Units Sold'] * product['Selling Price']
            cost = product['Units Sold'] * product['Unit Cost']
            product['Profit'] = revenue - cost
        return self.products
    
    def identify_reorder_products(self):
        """Identify products requiring immediate reorder (stock < safety threshold)"""
        reorder_products = []
        for product in self.products:
            # Safety stock = 20% of opening stock
            safety_stock = product['Opening Stock'] * 0.2
            if product['Current Stock'] < safety_stock:
                reorder_products.append(product)
        return reorder_products
    
    def calculate_inventory_turnover(self):
        """Calculate inventory turnover ratio"""
        for product in self.products:
            avg_inventory = product['Opening Stock'] / 2
            product['Turnover Ratio'] = product['Units Sold'] / avg_inventory if avg_inventory > 0 else 0
        return self.products
    
    def find_highest_profit_product(self):
        """Find the product with highest profit"""
        if not self.products:
            return None
        return max(self.products, key=lambda x: x['Profit'])
    
    def calculate_category_profit(self):
        """Calculate category-wise profit"""
        category_profit = defaultdict(float)
        for product in self.products:
            category_profit[product['Category']] += product['Profit']
        return dict(category_profit)
    
    def predict_next_month_demand(self):
        """Predict next month demand using moving average (last 3 months)"""
        # Simulating monthly sales data for moving average
        for product in self.products:
            # Simulated monthly sales (last 3 months)
            monthly_sales = [
                product['Units Sold'] * 0.3,  # Month 1
                product['Units Sold'] * 0.35, # Month 2
                product['Units Sold'] * 0.35  # Month 3
            ]
            product['Predicted Demand'] = sum(monthly_sales) / 3
        return self.products
    
    def sort_by_profitability(self):
        """Sort products by profitability"""
        return sorted(self.products, key=lambda x: x['Profit'], reverse=True)
    
    def export_to_csv(self, filename='inventory_report.csv'):
        """Export inventory report to CSV"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Product ID', 'Product Name', 'Category', 'Opening Stock', 
                         'Units Sold', 'Units Returned', 'Current Stock', 'Profit', 
                         'Turnover Ratio', 'Predicted Demand']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    'Product ID': product['Product ID'],
                    'Product Name': product['Product Name'],
                    'Category': product['Category'],
                    'Opening Stock': product['Opening Stock'],
                    'Units Sold': product['Units Sold'],
                    'Units Returned': product['Units Returned'],
                    'Current Stock': product['Current Stock'],
                    'Profit': product['Profit'],
                    'Turnover Ratio': round(product['Turnover Ratio'], 2),
                    'Predicted Demand': round(product['Predicted Demand'], 2)
                })
        print(f"Report exported to {filename}")
    
    def read_csv_and_display_top_profitable(self, filename='inventory_report.csv'):
        """Read CSV and display top five profitable products"""
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                products = list(reader)
                top_five = sorted(products, key=lambda x: float(x['Profit']), reverse=True)[:5]
                
                print("\n=== Top 5 Profitable Products ===")
                for i, product in enumerate(top_five, 1):
                    print(f"{i}. {product['Product Name']} - Profit: ${float(product['Profit']):,.2f}")
        except FileNotFoundError:
            print(f"File {filename} not found. Please export the report first.")
    
    def run_all_operations(self):
        """Run all operations in sequence"""
        print("=" * 60)
        print("SMART RETAIL INVENTORY AND DEMAND FORECASTING SYSTEM")
        print("=" * 60)
        
        # 1. Calculate current stock
        self.calculate_current_stock()
        print("\n✓ Current stock calculated")
        
        # 2. Calculate profit
        self.calculate_profit()
        print("✓ Profit calculated")
        
        # 3. Identify reorder products
        reorder_products = self.identify_reorder_products()
        print(f"✓ {len(reorder_products)} products require immediate reorder")
        
        # 4. Calculate inventory turnover
        self.calculate_inventory_turnover()
        print("✓ Inventory turnover ratio calculated")
        
        # 5. Find highest profit product
        highest_profit = self.find_highest_profit_product()
        if highest_profit:
            print(f"✓ Highest profit product: {highest_profit['Product Name']} (${highest_profit['Profit']:,.2f})")
        
        # 6. Calculate category-wise profit
        category_profit = self.calculate_category_profit()
        print("✓ Category-wise profit calculated")
        
        # 7. Predict next month demand
        self.predict_next_month_demand()
        print("✓ Next month demand predicted")
        
        # 8. Sort by profitability
        sorted_products = self.sort_by_profitability()
        print("✓ Products sorted by profitability")
        
        # 9. Export to CSV
        self.export_to_csv()
        print("✓ Report exported to CSV")
        
        # Display results
        self.display_results()
        
        # 10. Read CSV and display top five
        self.read_csv_and_display_top_profitable()
    
    def display_results(self):
        """Display all results in a formatted way"""
        print("\n" + "=" * 60)
        print("INVENTORY REPORT")
        print("=" * 60)
        
        print("\n--- Product Details ---")
        for product in self.products:
            print(f"\nProduct: {product['Product Name']} ({product['Product ID']})")
            print(f"  Category: {product['Category']}")
            print(f"  Current Stock: {product['Current Stock']}")
            print(f"  Profit: ${product['Profit']:,.2f}")
            print(f"  Turnover Ratio: {product['Turnover Ratio']:.2f}")
            print(f"  Predicted Demand: {product['Predicted Demand']:.2f}")
        
        print("\n--- Reorder Products ---")
        reorder = self.identify_reorder_products()
        if reorder:
            for product in reorder:
                print(f"  - {product['Product Name']}: Stock {product['Current Stock']}")
        else:
            print("  No products require reorder")
        
        print("\n--- Category-wise Profit ---")
        for category, profit in self.calculate_category_profit().items():
            print(f"  {category}: ${profit:,.2f}")

def main():
    system = RetailInventorySystem()
    system.run_all_operations()

if __name__ == "__main__":
    main()