import csv
import json
from collections import defaultdict
import os

class RailwayReservationSystem:
    def __init__(self):
        self.trains = []
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample train data"""
        self.trains = [
            {
                'Train Number': 'T101',
                'Route': 'Mumbai-Delhi',
                'Total Seats': 500,
                'Booked Seats': 480,
                'Waiting List Count': 25,
                'Ticket Fare': 1500,
                'Cancellation Count': 30,
                'Distance': 1400
            },
            {
                'Train Number': 'T102',
                'Route': 'Delhi-Chennai',
                'Total Seats': 400,
                'Booked Seats': 180,
                'Waiting List Count': 0,
                'Ticket Fare': 2000,
                'Cancellation Count': 15,
                'Distance': 2200
            },
            {
                'Train Number': 'T103',
                'Route': 'Mumbai-Bangalore',
                'Total Seats': 350,
                'Booked Seats': 340,
                'Waiting List Count': 15,
                'Ticket Fare': 1200,
                'Cancellation Count': 20,
                'Distance': 980
            },
            {
                'Train Number': 'T104',
                'Route': 'Chennai-Kolkata',
                'Total Seats': 300,
                'Booked Seats': 120,
                'Waiting List Count': 0,
                'Ticket Fare': 1800,
                'Cancellation Count': 10,
                'Distance': 1650
            },
            {
                'Train Number': 'T105',
                'Route': 'Delhi-Kolkata',
                'Total Seats': 450,
                'Booked Seats': 430,
                'Waiting List Count': 20,
                'Ticket Fare': 1600,
                'Cancellation Count': 25,
                'Distance': 1500
            }
        ]
    
    def calculate_occupancy_ratio(self):
        """Calculate occupancy ratio for each train"""
        for train in self.trains:
            train['Occupancy Ratio'] = (train['Booked Seats'] / train['Total Seats']) * 100
        return self.trains
    
    def calculate_actual_revenue(self):
        """Calculate actual revenue after cancellations"""
        for train in self.trains:
            # Revenue = (Booked Seats - Cancellation Count) * Ticket Fare
            actual_booked = max(0, train['Booked Seats'] - train['Cancellation Count'])
            train['Actual Revenue'] = actual_booked * train['Ticket Fare']
        return self.trains
    
    def identify_overbooked_trains(self):
        """Identify overbooked or high-demand trains"""
        overbooked = []
        for train in self.trains:
            if train['Booked Seats'] > train['Total Seats'] or train['Waiting List Count'] > 0:
                overbooked.append(train)
        return overbooked
    
    def calculate_revenue_per_km(self):
        """Calculate revenue per kilometer"""
        for train in self.trains:
            train['Revenue per KM'] = train['Actual Revenue'] / train['Distance'] if train['Distance'] > 0 else 0
        return self.trains
    
    def find_max_revenue_route(self):
        """Find the route with maximum revenue"""
        route_revenue = defaultdict(float)
        for train in self.trains:
            route_revenue[train['Route']] += train['Actual Revenue']
        if route_revenue:
            return max(route_revenue.items(), key=lambda x: x[1])
        return None
    
    def display_low_occupancy_trains(self):
        """Display trains with occupancy below 50%"""
        low_occupancy = [train for train in self.trains if train['Occupancy Ratio'] < 50]
        return low_occupancy
    
    def sort_trains_by_revenue(self):
        """Sort trains by revenue"""
        return sorted(self.trains, key=lambda x: x['Actual Revenue'], reverse=True)
    
    def generate_analytics_report(self, filename='railway_report.json'):
        """Generate a reservation analytics report"""
        report = {
            'timestamp': str(datetime.now()),
            'total_trains': len(self.trains),
            'trains': self.trains,
            'summary': {
                'total_revenue': sum(train['Actual Revenue'] for train in self.trains),
                'average_occupancy': sum(train['Occupancy Ratio'] for train in self.trains) / len(self.trains),
                'total_waiting': sum(train['Waiting List Count'] for train in self.trains),
                'total_cancellations': sum(train['Cancellation Count'] for train in self.trains)
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Analytics report saved to {filename}")
        return report
    
    def read_report(self, filename='railway_report.json'):
        """Read the report from a file"""
        try:
            with open(filename, 'r') as f:
                report = json.load(f)
            return report
        except FileNotFoundError:
            print(f"Report file {filename} not found")
            return None
    
    def display_top_revenue_trains(self):
        """Display top three revenue-generating trains"""
        sorted_trains = self.sort_trains_by_revenue()
        print("\n=== Top 3 Revenue-Generating Trains ===")
        for i, train in enumerate(sorted_trains[:3], 1):
            print(f"{i}. Train {train['Train Number']} ({train['Route']}) - Revenue: ${train['Actual Revenue']:,.2f}")
    
    def run_all_operations(self):
        """Run all operations in sequence"""
        print("=" * 60)
        print("SMART RAILWAY RESERVATION AND REVENUE OPTIMIZATION SYSTEM")
        print("=" * 60)
        
        # Calculate all metrics
        self.calculate_occupancy_ratio()
        self.calculate_actual_revenue()
        self.calculate_revenue_per_km()
        
        print("\n✓ Occupancy ratio calculated")
        print("✓ Actual revenue after cancellations calculated")
        print("✓ Revenue per kilometer calculated")
        
        # Identify overbooked trains
        overbooked = self.identify_overbooked_trains()
        print(f"✓ {len(overbooked)} trains are overbooked or have waiting lists")
        
        # Find max revenue route
        max_route = self.find_max_revenue_route()
        if max_route:
            print(f"✓ Route with maximum revenue: {max_route[0]} (${max_route[1]:,.2f})")
        
        # Display low occupancy trains
        low_occ = self.display_low_occupancy_trains()
        print(f"✓ {len(low_occ)} trains have occupancy below 50%")
        
        # Sort trains by revenue
        self.sort_trains_by_revenue()
        print("✓ Trains sorted by revenue")
        
        # Generate report
        self.generate_analytics_report()
        print("✓ Analytics report generated")
        
        # Read report
        report = self.read_report()
        if report:
            print("✓ Report read successfully")
        
        # Display results
        self.display_results()
        
        # Display top revenue trains
        self.display_top_revenue_trains()
    
    def display_results(self):
        """Display all results"""
        print("\n" + "=" * 60)
        print("RESERVATION REPORT")
        print("=" * 60)
        
        print("\n--- Train Details ---")
        for train in self.trains:
            print(f"\nTrain {train['Train Number']} - {train['Route']}")
            print(f"  Occupancy: {train['Occupancy Ratio']:.1f}%")
            print(f"  Booked Seats: {train['Booked Seats']}/{train['Total Seats']}")
            print(f"  Waiting List: {train['Waiting List Count']}")
            print(f"  Actual Revenue: ${train['Actual Revenue']:,.2f}")
            print(f"  Revenue per KM: ${train['Revenue per KM']:.2f}")
        
        print("\n--- Low Occupancy Trains (< 50%) ---")
        low_occ = self.display_low_occupancy_trains()
        if low_occ:
            for train in low_occ:
                print(f"  - Train {train['Train Number']}: {train['Occupancy Ratio']:.1f}% occupancy")
        else:
            print("  All trains have good occupancy")
        
        print("\n--- Overbooked/High-Demand Trains ---")
        overbooked = self.identify_overbooked_trains()
        if overbooked:
            for train in overbooked:
                if train['Booked Seats'] > train['Total Seats']:
                    print(f"  - Train {train['Train Number']}: Overbooked by {train['Booked Seats'] - train['Total Seats']} seats")
                elif train['Waiting List Count'] > 0:
                    print(f"  - Train {train['Train Number']}: {train['Waiting List Count']} on waiting list")

from datetime import datetime

def main():
    system = RailwayReservationSystem()
    system.run_all_operations()

if __name__ == "__main__":
    main()
