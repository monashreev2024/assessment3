import json

class PortfolioManager:
    def __init__(self, records):
        """
        Initializes the manager with a list of portfolio records.
        Each record is a dictionary containing the required fields.
        """
        self.records = records

    def calculate_investment_value(self, record):
        """Calculate investment value = Quantity * Buy Price"""
        return record["Quantity"] * record["Buy Price"]

    def calculate_current_value(self, record):
        """Calculate current value = Quantity * Current Price"""
        return record["Quantity"] * record["Current Price"]

    def calculate_profit_loss(self, record):
        """Calculate profit/loss = Current Value - Investment Value + Dividend Received"""
        invested = self.calculate_investment_value(record)
        current = self.calculate_current_value(record)
        return current - invested + record["Dividend Received"]

    def calculate_percentage_return(self, record):
        """Calculate percentage return = (Profit/Loss / Investment Value) * 100"""
        invested = self.calculate_investment_value(record)
        if invested == 0:
            return 0.0
        p_l = self.calculate_profit_loss(record)
        return (p_l / invested) * 100

    def find_best_performing_stock(self):
        """Find the stock with the highest percentage return"""
        if not self.records:
            return None
        return max(self.records, key=self.calculate_percentage_return)

    def find_worst_performing_stock(self):
        """Find the stock with the lowest percentage return"""
        if not self.records:
            return None
        return min(self.records, key=self.calculate_percentage_return)

    def calculate_sector_wise_exposure(self):
        """Calculate the total current value exposure per sector"""
        sectors = {}
        for r in self.records:
            sector = r["Sector"]
            current_val = self.calculate_current_value(r)
            sectors[sector] = sectors.get(sector, 0.0) + current_val
        return sectors

    def rank_investors_by_portfolio_return(self):
        """Ranks unique investors by their total overall portfolio percentage return"""
        investor_data = {}
        
        # Aggregate investment values and total profits/losses per investor
        for r in self.records:
            inv_id = r["Investor ID"]
            if inv_id not in investor_data:
                investor_data[inv_id] = {"total_invested": 0.0, "total_pl": 0.0}
            
            investor_data[inv_id]["total_invested"] += self.calculate_investment_value(r)
            investor_data[inv_id]["total_pl"] += self.calculate_profit_loss(r)
        
        # Calculate overall return rate for each investor
        ranked_investors = []
        for inv_id, metrics in investor_data.items():
            if metrics["total_invested"] > 0:
                overall_return = (metrics["total_pl"] / metrics["total_invested"]) * 100
            else:
                overall_return = 0.0
            ranked_investors.append((inv_id, overall_return))
        
        # Sort descending by return performance
        ranked_investors.sort(key=lambda x: x[1], reverse=True)
        return ranked_investors

    def generate_portfolio_report(self):
        """Generates a structured dictionary containing all calculated metrics"""
        best = self.find_best_performing_stock()
        worst = self.find_worst_performing_stock()
        
        report = {
            "Detailed Records": [],
            "Best Performing Stock": best["Stock Symbol"] if best else "N/A",
            "Worst Performing Stock": worst["Stock Symbol"] if worst else "N/A",
            "Sector Exposure": self.calculate_sector_wise_exposure(),
            "Investor Rankings (ID, % Return)": self.rank_investors_by_portfolio_return()
        }
        
        for r in self.records:
            record_analysis = {
                "Investor ID": r["Investor ID"],
                "Stock Symbol": r["Stock Symbol"],
                "Investment Value": self.calculate_investment_value(r),
                "Current Value": self.calculate_current_value(r),
                "Profit/Loss": self.calculate_profit_loss(r),
                "Percentage Return": round(self.calculate_percentage_return(r), 2)
            }
            report["Detailed Records"].append(record_analysis)
            
        return report

    def save_report(self, filename="portfolio_report.json"):
        """Saves the generated report to a physical text/JSON file"""
        report_data = self.generate_portfolio_report()
        with open(filename, "w") as file:
            json.dump(report_data, file, indent=4)
        print(f"[SUCCESS] Report successfully saved to '{filename}'")

    @staticmethod
    def read_report(filename="portfolio_report.json"):
        """Reads and displays the saved report file"""
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                print("\n" + "="*50)
                print("             SAVED PORTFOLIO REPORT            ")
                print("="*50)
                print(json.dumps(data, indent=4))
                print("="*50)
        except FileNotFoundError:
            print(f"[ERROR] File '{filename}' not found.")


# --- Execution Block ---
if __name__ == "__main__":
    # Sample Dataset matching all requested fields
    sample_portfolio = [
        {"Investor ID": "INV001", "Stock Symbol": "AAPL", "Quantity": 10, "Buy Price": 150.0, "Current Price": 175.0, "Sector": "Technology", "Dividend Received": 20.0},
        {"Investor ID": "INV001", "Stock Symbol": "XOM", "Quantity": 20, "Buy Price": 80.0, "Current Price": 75.0, "Sector": "Energy", "Dividend Received": 45.0},
        {"Investor ID": "INV002", "Stock Symbol": "TSLA", "Quantity": 5, "Buy Price": 200.0, "Current Price": 240.0, "Sector": "Automotive", "Dividend Received": 0.0},
        {"Investor ID": "INV003", "Stock Symbol": "NVDA", "Quantity": 15, "Buy Price": 400.0, "Current Price": 480.0, "Sector": "Technology", "Dividend Received": 10.0}
    ]

    # Process Portfolio
    manager = PortfolioManager(sample_portfolio)
    
    # Save Report
    manager.save_report()
    
    # Read Report
    manager.read_report()
