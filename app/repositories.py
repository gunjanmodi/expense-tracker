from datetime import datetime
from typing import List, Dict
import csv

from .boundaries import ExpenseRepositoryInterface, FileHandlerInterface
from .models import Expense

from .utils.logger_config import setup_logger
LOGGER = setup_logger()


class ExpenseJsonRepository(ExpenseRepositoryInterface):

    def __init__(self, expense_file_handler: FileHandlerInterface, logger=LOGGER):
        self.expense_file_handler = expense_file_handler
        self.logger = logger

    def add_expense(self, new_expense: Expense) -> Expense:
        expenses = self.get_all_expenses()
        self._assign_new_id(new_expense, expenses)
        expenses.append(new_expense)
        self._save_expense(expenses)
        self.logger.info(f"Expense added successfully (ID: {new_expense.id})")
        return new_expense

    def get_all_expenses(self) -> List[Expense]:
        raw_data = self.expense_file_handler.read()
        return [Expense(**data) for data in raw_data]

    def get_all_expenses_by_category(self, category: str) -> List[Expense]:
        raw_data = self.expense_file_handler.read()
        return [Expense(**data) for data in raw_data if data["category"] == category]

    def delete_expense(self, expense_id) -> None:
        expenses = self.get_all_expenses()
        updated_expenses = [expense for expense in expenses if expense.id != expense_id]
        if len(expenses) == len(updated_expenses):
            raise ValueError(f"Expense with ID {expense_id} not found.")
        self._save_expense(updated_expenses)
        self.logger.info(f"Deleted the Expense with ID: {expense_id}")

    def total_expense(self) -> float:
        return sum([expense.amount for expense in self.get_all_expenses()])

    def total_expense_by_month(self, month: int) -> float:
        year: int = datetime.now().year
        total_monthly_expense = 0
        for expense in self.get_all_expenses():
            if expense.date.month == month and expense.date.year == year:
                total_monthly_expense += expense.amount
        return total_monthly_expense

    def export_expenses_to_csv(self, file_path: str) -> None:
        expenses = self.get_all_expenses()
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["ID", "Description", "Category", "Amount", "Date"])
            for expense in expenses:
                writer.writerow([expense.id, expense.description, expense.category, expense.amount, expense.date])

    def clear_all_expenses(self) -> None:
        self._save_expense([])

    def _assign_new_id(self, new_expense: Expense, expenses: List[Expense]) -> None:
        new_expense.id = max([expense.id for expense in expenses], default=0) + 1

    def _save_expense(self, expenses: List[Expense]):
        data: List[Dict] = [expense.model_dump() for expense in expenses]
        self.expense_file_handler.write(data)
