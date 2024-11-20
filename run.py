import json
import os
import pkg_resources
from datetime import datetime
import matplotlib.pyplot as plt


class ExpenseTracker:
    def __init__(self):
        self.data_file=os.path.join(os.getcwd(), 'expenses.json')
        self.expenses = []
        self.load_data()    
        
    def load_data(self):
        """Load expenses data from a JSON file."""
        try:
            
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.expenses = json.load(file)
            else:
                self.expenses = []
        
        except(IOError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")
            self.expenses = []
    def save_data(self):
        """Save expenses data to a JSON file."""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.expenses, file, indent=4)
        
        except IOError as e:
            print(f"Error saving data: {e}")
        
    
    def add_expense(self):
        """Add a new expense entry."""
        try:
            amount = float(input("Enter amount: "))
            category = input("Enter category (e.g., food, rent, travel): ").lower()
            date = input("Enter date (YYYY-MM-DD) [Leave blank for today]: ")
            description = input("Enter description: ")
            
            if not date:
                date=datetime.today().strftime('%Y-%m-%d')
            
            expense =  {
                "amount": amount,
                "category": category,
                "date": date,
                "description": description
            }
            
            self.expenses.append(expense)
            self.save_data()
            print("Expense added successfully")
        
        except ValueError as e:
            print(f"Invalid input: {e}")
        
    def delete_expense(self):
        """Delete an expense entry by index."""
        try:
            self.view_expenses()
            index = int(input("Enter the index of the expense to delete: ")) - 1
            if 0 <= index < len(self.expenses):
                self.expenses.pop(index)
                self.save_data()
                print("Expense deleted successfully")
            else:
                print("Invalid index")
        
        except(ValueError, IndexError):
            print("Error: Invalid index or input.")
       
    def view_expenses(self, filter_by_category=None):
        """View all expenses or filter by category"""
        if filter_by_category:
            filtered_expenses = [e for e in self.expenses if e['category'] == filter_by_category]
        else:
            filtered_expenses = self.expenses
            
        if not filtered_expenses:
            print("No expenses to show")
            
        else:
            for i, expense in enumerate(filtered_expenses, start=1):
                print(f"{i}. {expense['date']} - {expense['category'].capitalize()}: {expense['amount']} ({expense['description']})")
    
    def generate_report(self):
        """Generate a bar chart of expenses by category"""
        try:
            categories = {}
            for expense in self.expenses:
                categories[expense['category']] = categories.get(expense['category'], 0) + expense['amount']
            
            if not categories:
                print("No expenses to report")
                return
            
            plt.figure(figsize=(8, 6))
            plt.bar(categories.keys(), categories.values(), color="skyblue")
            plt.title("Expense Distribution by Category")
            plt.xlabel("Category")
            plt.ylabel("Amount Spent")
            plt.show()
        
        except Exception as e:
            print(f"Error generating report: {e}")
        
    def run(self):
        """Main loop to run the Expense Tracker Application"""
        while True:
            print("\nPersonal Expense Tracker")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Delete Expense")
            print("4. Generate Report")
            print("5. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.add_expense()
            
            elif choice == '2':
                category = input("Filter by category? (Leave a blank for all): ").lower()
                self.view_expenses(category if category else None)
            
            elif choice == '3':
                self.delete_expense()
            
            elif choice == '4':
                self.generate_report()
            
            elif choice == '5':
                print("Exiting...")
                break
            
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
    