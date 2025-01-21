#!/usr/bin/env python3

import argparse

from pydantic import ValidationError

from app.services import ExpenseService
from app.repositories import ExpenseJsonRepository
from app.utils.json_file_handler import JSONFileHandler
from app.constants import DATA_FILE


def main():
    parser = argparse.ArgumentParser(prog="expense-tracker", description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add expense command
    add_parser = subparsers.add_parser(name="add", help="Add a new expense")
    add_parser.add_argument("--description", type=str, required=True, help="Description of the expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount of the expense")
    add_parser.add_argument("--category", type=str, required=False, help="Category of the expense")

    # List expenses command
    list_parser = subparsers.add_parser(name="list", help="List all expenses")
    list_parser.add_argument("--category", type=str, required=False,help="Category of the expense")

    # Summary command
    summary_parser = subparsers.add_parser(name="summary", help="Show total expense summary")
    summary_parser.add_argument("--month", type=int, required=False,help="Get Summary by month")

    # Delete expense command
    delete_parser = subparsers.add_parser(name="delete", help="Delete an expense by ID")
    delete_parser.add_argument("--id", type=int, required=True, help="ID of the expense to delete")

    # Export expenses command
    csv_export_parser = subparsers.add_parser(name="export", help="Export expenses to a csv file")
    csv_export_parser.add_argument("--file-path", required=True, help="Path to save the exported CSV file")


    # Clear all expenses command
    subparsers.add_parser(name="clear", help="Clear all expenses")

    # Parse the arguments
    args = parser.parse_args()

    repository = ExpenseJsonRepository(JSONFileHandler(DATA_FILE))
    expense_service = ExpenseService(repository)

    if args.command == "add":
        try:
            new_expense = expense_service.add_expense(args.description, args.amount, args.category)
            print(f"Added expense: ID={new_expense.id}, Description={new_expense.description},"
                  f" Amount={new_expense.amount}, Category={new_expense.category}")
        except ValidationError as ve:
            for error in ve.errors():
                print(f"Error in field '{error['loc'][0]}': {error['msg']}")

    elif args.command == "list":
        expenses = expense_service.list_expenses(args.category)
        if not expenses:
            print("No expenses found.")
        else:
            print("Expenses:")
            for expense in expenses:
                print(f"ID: {expense.id}, Description: {expense.description},"
                      f" Amount: {expense.amount}, Category: {expense.category}, Date: {expense.date}")

    elif args.command == "summary":
        total = expense_service.summary(args.month)
        print(f"Total expense: {total}")

    elif args.command == "delete":
        try:
            expense_service.delete(args.id)
            print(f"Deleted expense with ID: {args.id}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "export":
        expense_service.export_expenses_to_csv(args.file_path)
        print(f"Expenses exported successfully to {args.file_path}")

    elif args.command == "clear":
        expense_service.clear_all_expenses()
        print("All expenses cleared.")

if __name__ == "__main__":
    main()
