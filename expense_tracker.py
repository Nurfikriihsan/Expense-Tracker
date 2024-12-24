import argparse
import json
import os
from datetime import datetime

# File to store expense data
EXPENSE_FILE = 'expenses.json'


def load_expenses():
    """Load expenses from the JSON file."""
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, 'r') as file:
            return json.load(file)
    return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    with open(EXPENSE_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)


def add_expense(description, amount):
    """Add a new expense."""
    expenses = load_expenses()
    expense_id = len(expenses) + 1
    date = datetime.now().strftime('%Y-%m-%d')
    expense = {
        'id': expense_id,
        'date': date,
        'description': description,
        'amount': amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f'Expense added successfully (ID: {expense_id})')


def list_expenses():
    """List all expenses."""
    expenses = load_expenses()
    print(f"{'ID':<5} {'Date':<12} {'Description':<20} {'Amount':<10}")
    for expense in expenses:
        print(f"{expense['id']:<5} {expense['date']:<12} {expense['description']:<20} ${expense['amount']:<10}")


def delete_expense(expense_id):
    """Delete an expense by ID."""
    expenses = load_expenses()
    expense = next((e for e in expenses if e['id'] == expense_id), None)
    if expense:
        expenses.remove(expense)
        save_expenses(expenses)
        print(f'Expense deleted successfully')
    else:
        print(f'Error: Expense with ID {expense_id} not found')


def summary(month=None):
    """Show the total expenses, optionally filtered by month."""
    expenses = load_expenses()
    if month:
        expenses = [e for e in expenses if datetime.strptime(e['date'], '%Y-%m-%d').month == month]

    total_expenses = sum(e['amount'] for e in expenses)
    if month:
        print(f'Total expenses for month {month}: ${total_expenses}')
    else:
        print(f'Total expenses: ${total_expenses}')


def main():
    parser = argparse.ArgumentParser(description='Expense Tracker CLI Application')

    subparsers = parser.add_subparsers(dest='command')

    # Add expense
    add_parser = subparsers.add_parser('add', help='Add an expense')
    add_parser.add_argument('--description', required=True, help='Description of the expense')
    add_parser.add_argument('--amount', type=float, required=True, help='Amount of the expense')

    # List expenses
    subparsers.add_parser('list', help='List all expenses')

    # Delete expense
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('--id', type=int, required=True, help='ID of the expense to delete')

    # Summary
    summary_parser = subparsers.add_parser('summary', help='Show a summary of expenses')
    summary_parser.add_argument('--month', type=int, help='Month of the year (1-12) to filter expenses')

    args = parser.parse_args()

    if args.command == 'add':
        add_expense(args.description, args.amount)
    elif args.command == 'list':
        list_expenses()
    elif args.command == 'delete':
        delete_expense(args.id)
    elif args.command == 'summary':
        summary(args.month)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
