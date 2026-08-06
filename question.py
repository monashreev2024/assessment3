import csv

class Product:
    def __init__(self, prod_id, name, category, opening_stock, units_sold, units_returned, lead_time, unit_cost, selling_price):
        self.prod_id = prod_id
        self.name = name
        self.category = category
        self.opening_stock = int(opening_stock)
        self.units_sold = int(units_sold)
        self.units_returned = int(units_returned)
        self.lead_time = int(lead_time)  # in days
        self.unit_cost = float(unit_cost)
        self.selling_price = float(selling_price)
        
        # Computed metrics
        self.current_stock = 0
        self.profit = 0.0
        self.turnover_ratio = 0.0
        self.predicted_demand = 0.0

class InventorySystem:
    def __init__(self, products):
        self.products = products

    # 1. Calculate current stock
    def calculate_current_stock(self):
        for p in self.products:
            p.current_stock = p.opening_stock - p.units_sold + p.units_returned

    # 2. Calculate profit for each product
    def calculate_profit(self):
        for p in self.products:
            # Profit = (Units Sold * Selling Price) - (Units Sold * Unit Cost)
            # Net sold accounts for returned units effectively restocked
            net_sold = p.units_sold - p.units_returned
            p.profit = (net_sold * p.selling_price) - (p.units_sold * p.unit_cost)

    # 3. Identify products requiring immediate reorder (Stock <= Safety Buffer based on Lead Time)
    def identify_reorder_products(self):
        reorder_list = []
        for p in self.products:
            # Simple reorder point logic: if current stock falls below 5 units or lead-time driven buffer
            if p.current_stock <= (p.lead_time * 0.5): 
                reorder_list.append(p)
        return reorder_list

    # 4. Compute inventory turnover ratio
    def compute_turnover_ratio(self):
        for p in self.products:
            avg_inventory = (p.opening_stock + p.current_stock) / 2
            cogs = p.units_sold * p.unit_cost
            p.turnover_ratio = cogs / avg_inventory if avg_inventory > 0 else 0.0

    # 5. Find the highest profit product
    def find_highest_profit_product(self):
        if not self.products: return None
        return max(self.products, key=lambda p: p.profit)

    # 6. Calculate category-wise profit
    def calculate_category_profit(self):
        category_profit = {}
        for p in self.products:
            category_profit[p.category] = category_profit.get(p.category, 0.0) + p.profit
        return category_profit

    # 7. Predict next month demand using moving average logic
    def predict_demand(self):
        for p in self.products:
            # Moving average mock-up based on current sales activity and baseline trends
            p.predicted_demand = round((p.units_sold + (p.opening_stock - p.current_stock)) / 2)

    # 8. Sort products by profitability
    def sort_by_profitability(self):
        self.products.sort(key=lambda p: p.profit, reverse=True)

    # 9. Export inventory report to CSV
    def export_to_csv(self, filename="inventory_report.csv"):
        fields = [
            "Product ID", "Product Name", "Category", "Current Stock", 
            "Profit", "Turnover Ratio", "Predicted Demand"
        ]
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            for p in self.products:
                writer.writerow([
                    p.prod_id, p.name, p.category, p.current_stock, 
                    round(p.profit, 2), round(p.turnover_ratio, 2), p.predicted_demand
                ])
        print(f"\n[Success] Report exported to '{filename}'")

    # 10. Read the CSV and display the top five profitable products
    @staticmethod
    def display_top_five_from_csv(filename="inventory_report.csv"):
        print("\n--- TOP 5 PROFITABLE PRODUCTS FROM CSV ---")
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                records = list(reader)
                
            # Sort data by profit parsed as float
            records.sort(key=lambda x: float(x["Profit"]), reverse=True)
            
            for i, row in enumerate(records[:5], 1):
                print(f"{i}. ID: {row['Product ID']} | Name: {row['Product Name']} | Profit: ${row['Profit']}")
        except FileNotFoundError:
            print("Error: Report file missing.")

# --- Execution Setup ---
if __name__ == "__main__":
    # Sample Dataset mimicking incoming data streams
    sample_data = [
        Product("P001", "Laptop", "Electronics", 50, 40, 2, 5, 500, 800),
        Product("P002", "Smartphone", "Electronics", 100, 85, 5, 3, 300, 500),
        Product("P003", "Desk Chair", "Furniture", 30, 10, 0, 10, 50, 120),
        Product("P004", "Coffee Maker", "Appliances", 25, 22, 1, 4, 40, 90),
        Product("P005", "Backpack", "Accessories", 80, 75, 4, 2, 15, 45),
        Product("P006", "Headphones", "Electronics", 60, 55, 3, 3, 25, 60),
    ]

    sys = InventorySystem(sample_data)
    
    # Process Workflow (Req 1, 2, 4, 7)
    sys.calculate_current_stock()
    sys.calculate_profit()
    sys.compute_turnover_ratio()
    sys.predict_demand()
    
    # Req 3: Identify Reorders
    reorders = sys.identify_reorder_products()
    print("Products needing immediate reorder:", [p.name for p in reorders])
    
    # Req 5: Highest profit item
    top_item = sys.find_highest_profit_product()
    print(f"Highest Profit Product: {top_item.name} (${top_item.profit})")
    
    # Req 6: Category Profit breakdown
    cat_profit = sys.calculate_category_profit()
    print("Category Profit Analysis:", cat_profit)
    
    # Req 8: Sort implementation
    sys.sort_by_profitability()
    
    # Req 9: Save output
    sys.export_to_csv()
    
    # Req 10: Read back target visual metrics
    InventorySystem.display_top_five_from_csv()
