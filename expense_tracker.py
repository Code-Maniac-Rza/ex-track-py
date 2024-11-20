import argparse
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self):
        self.data_file = "expenses.json"
        self.expenses = []
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.expenses = json.load(file)
            else:
                self.expenses = []
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")
            self.expenses = []

    def save_data(self):
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.expenses, file, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_expense(self, amount, category, date=None, description=""):
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')
        expense = {
            "amount": amount,
            "category": category,
            "date": date,
            "description": description,
        }
        self.expenses.append(expense)
        self.save_data()
        print("Expense added successfully.")

    def view_expenses(self, filter_by_category=None):
        filtered_expenses = (
            [e for e in self.expenses if e['category'] == filter_by_category]
            if filter_by_category
            else self.expenses
        )
        if not filtered_expenses:
            print("No expenses to show.")
        else:
            for i, expense in enumerate(filtered_expenses, start=1):
                print(
                    f"{i}. {expense['date']} - {expense['category'].capitalize()}: {expense['amount']} ({expense['description']})"
                )

    def generate_report(self):
        categories = {}
        for expense in self.expenses:
            categories[expense['category']] = categories.get(expense['category'], 0) + expense['amount']
        if not categories:
            print("No expenses to report.")
            return
        plt.figure(figsize=(8, 6))
        plt.bar(categories.keys(), categories.values(), color="skyblue")
        plt.title("Expense Distribution by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount Spent")
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    parser.add_argument("action", choices=["add", "view", "report"], help="Action to perform")
    parser.add_argument("--amount", type=float, help="Amount of the expense")
    parser.add_argument("--category", help="Category of the expense")
    parser.add_argument("--date", help="Date of the expense (YYYY-MM-DD)")
    parser.add_argument("--description", help="Description of the expense")
    args = parser.parse_args()

    tracker = ExpenseTracker()

    if args.action == "add":
        if not args.amount or not args.category:
            print("Amount and category are required for adding an expense.")
            return
        tracker.add_expense(args.amount, args.category, args.date, args.description)
    elif args.action == "view":
        tracker.view_expenses(args.category)
    elif args.action == "report":
        tracker.generate_report()

if __name__ == "__main__":
    main()
