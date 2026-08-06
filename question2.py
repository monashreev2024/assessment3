import json

class RailwaySystem:
    def __init__(self, trains_data):
        """Initializes the system with a list of train dictionaries."""
        self.trains = trains_data

    # 1. Calculate occupancy ratio
    def calculate_occupancy_ratio(self, train):
        if train["total_seats"] == 0:
            return 0.0
        return round(train["booked_seats"] / train["total_seats"], 4)

    # 2. Calculate actual revenue after cancellations
    def calculate_actual_revenue(self, train):
        effective_bookings = train["booked_seats"] - train["cancellation_count"]
        # Ensure we don't have negative bookings due to bad data
        effective_bookings = max(0, effective_bookings) 
        return effective_bookings * train["ticket_fare"]

    # 3. Identify overbooked or high-demand trains
    def is_high_demand(self, train):
        # High demand if occupancy is 100% or there are people waiting
        return train["booked_seats"] >= train["total_seats"] or train["waiting_list_count"] > 0

    # 4. Calculate revenue per kilometer
    def calculate_revenue_per_km(self, train):
        if train["distance"] == 0:
            return 0.0
        revenue = self.calculate_actual_revenue(train)
        return round(revenue / train["distance"], 2)

    # 5. Find the route with maximum revenue
    def find_max_revenue_route(self):
        route_revenue = {}
        for t in self.trains:
            rev = self.calculate_actual_revenue(t)
            route_revenue[t["route"]] = route_revenue.get(t["route"], 0) + rev
        
        if not route_revenue:
            return None, 0
        max_route = max(route_revenue, key=route_revenue.get)
        return max_route, route_revenue[max_route]

    # 6. Display trains with occupancy below 50%
    def get_low_occupancy_trains(self):
        low_occ = []
        for t in self.trains:
            if self.calculate_occupancy_ratio(t) < 0.5:
                low_occ.append(t["train_number"])
        return low_occ

    # 7. Sort trains by revenue (Descending)
    def sort_trains_by_revenue(self):
        return sorted(self.trains, key=lambda x: self.calculate_actual_revenue(x), reverse=True)

    # 8. Generate a reservation analytics report
    def generate_report(self):
        report = {
            "trains_analytics": [],
            "max_revenue_route": {},
            "low_occupancy_trains": self.get_low_occupancy_trains(),
            "top_3_trains": []
        }
        
        for t in self.trains:
            analytics = {
                "train_number": t["train_number"],
                "route": t["route"],
                "occupancy_ratio": self.calculate_occupancy_ratio(t),
                "actual_revenue": self.calculate_actual_revenue(t),
                "revenue_per_km": self.calculate_revenue_per_km(t),
                "high_demand": self.is_high_demand(t)
            }
            report["trains_analytics"].append(analytics)
            
        max_route, max_rev = self.find_max_revenue_route()
        report["max_revenue_route"] = {"route": max_route, "total_revenue": max_rev}
        
        sorted_t = self.sort_trains_by_revenue()
        report["top_3_trains"] = [t["train_number"] for t in sorted_t[:3]]
        
        return report

    # 9. Save and read the report from a file
    def save_report_to_file(self, filename="analytics_report.json"):
        report = self.generate_report()
        with open(filename, "w") as f:
            json.dump(report, f, indent=4)
        print(f"[INFO] Report successfully saved to {filename}\n")

    @staticmethod
    def read_report_from_file(filename="analytics_report.json"):
        print(f"[INFO] Reading report from {filename}...")
        with open(filename, "r") as f:
            data = json.load(f)
        return data


# --- EXECUTION ENGINE FOR PIPELINE COMPLIANCE ---
if __name__ == "__main__":
    # Sample Mock Dataset matching the required structure
    sample_trains = [
        {"train_number": "T101", "route": "NY-DC", "total_seats": 200, "booked_seats": 190, "waiting_list_count": 5, "ticket_fare": 50, "cancellation_count": 10, "distance": 350},
        {"train_number": "T102", "route": "LA-SF", "total_seats": 150, "booked_seats": 60, "waiting_list_count": 0, "ticket_fare": 80, "cancellation_count": 2, "distance": 600},
        {"train_number": "T103", "route": "CHI-DET", "total_seats": 100, "booked_seats": 100, "waiting_list_count": 12, "ticket_fare": 40, "cancellation_count": 0, "distance": 450},
        {"train_number": "T104", "route": "NY-DC", "total_seats": 300, "booked_seats": 280, "waiting_list_count": 20, "ticket_fare": 55, "cancellation_count": 15, "distance": 350},
        {"train_number": "T105", "route": "MIA-ORL", "total_seats": 250, "booked_seats": 80, "waiting_list_count": 0, "ticket_fare": 30, "cancellation_count": 5, "distance": 380}
    ]

    # Initialize System
    system = RailwaySystem(sample_trains)

    print("==================================================")
    print("Executing Requirements 1-10 Tasks")
    print("==================================================\n")

    # Tasks 1 to 4: Individual Calculations demonstration
    print("--- Train Specific Metrics (Tasks 1, 2, 3, 4) ---")
    for train in sample_trains:
        occ = system.calculate_occupancy_ratio(train)
        rev = system.calculate_actual_revenue(train)
        hd = system.is_high_demand(train)
        rpk = system.calculate_revenue_per_km(train)
        print(f"Train {train['train_number']}: Occupancy={occ*100:.1f}%, Revenue=${rev}, HighDemand={hd}, Rev/Km=${rpk}")
    print()

    # Task 5: Max Revenue Route
    route, route_rev = system.find_max_revenue_route()
    print(f"--- Task 5: Max Revenue Route ---\nRoute: {route} (Total Revenue: ${route_rev})\n")

    # Task 6: Low Occupancy (< 50%)
    print(f"--- Task 6: Low Occupancy Trains (<50%) ---\nTrains: {system.get_low_occupancy_trains()}\n")

    # Task 7: Sort by revenue
    print("--- Task 7: Trains Sorted By Revenue (Descending) ---")
    for t in system.sort_trains_by_revenue():
         print(f"Train {t['train_number']}: Revenue = ${system.calculate_actual_revenue(t)}")
    print()


    print("--- Task 8 & 9: File IO Management ---")
    filename = "railway_analytics.json"
    system.save_report_to_file(filename)
    loaded_report = RailwaySystem.read_report_from_file(filename)
    print("File Content verified successfully.\n")

    print("--- Task 10: Top Three Revenue Generating Trains ---")
    sorted_trains = system.sort_trains_by_revenue()
    for i, t in enumerate(sorted_trains[:3], 1):
        print(f"{i}. Train {t['train_number']} (Route: {t['route']}) - Revenue: ${system.calculate_actual_revenue(t)}")
    print("\n==================================================")
    print("Pipeline Execution Completed Successfully.")
    print("==================================================")
