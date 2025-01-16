import os
import json
from datetime import datetime
from typing import List
from .constants import DATA_FILE
from .boundaries import ExpenseRepositoryInterface
from .models import Expense

from .utils.logger_config import setup_logger
logger = setup_logger()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class ExpenseJsonRepository(ExpenseRepositoryInterface):
    """Handles loading and saving expenses to the json data file."""

    def save_expenses(self, new_expense: Expense) -> Expense:
        expenses = self.fetch_expenses()
        self._assign_new_id(new_expense, expenses)
        expenses.append(new_expense)
        self._write_expense_to_file(expenses)
        logger.info(f"Expense added successfully (ID: {new_expense.id})")
        return new_expense

    def fetch_expenses(self) -> List[Expense]:
        if not os.path.exists(DATA_FILE):
            return []
        if os.path.getsize(DATA_FILE) == 0:
            return []
        return self._read_json_file()

    def _read_json_file(self) -> List[Expense]:
        try:
            with open(DATA_FILE, "r") as expenses_data_file:
                raw_expense_data = json.load(expenses_data_file)
                return [Expense(**expense) for expense in raw_expense_data]
        except json.JSONDecodeError:
            raise ValueError(f"{DATA_FILE} contains invalid JSON.")
        except IOError as e:
            raise IOError(f"Failed to read {DATA_FILE}: {e}")
        except ValueError as e:
            raise ValueError(f"Data in {DATA_FILE} does not match the Expense model schema: {e}")

    def _write_expense_to_file(self, expenses: List[Expense]):
        try:
            with open(DATA_FILE, "w") as file:
                json.dump([expense.model_dump() for expense in expenses], file, indent=4, cls=DateTimeEncoder)

        except IOError as e:
            raise IOError(f"Failed to write to {DATA_FILE}: {e}")

    def _assign_new_id(self, new_expense: Expense, expenses: List[Expense]) -> None:
        new_expense.id = max([expense.id for expense in expenses], default=0) + 1

    def delete_expense(self, expense_id) -> None:
        expenses = self.fetch_expenses()
        updated_expenses = [expense for expense in expenses if expense.id != expense_id]
        if len(expenses) == len(updated_expenses):
            raise ValueError(f"Expense with ID {expense_id} not found.")
        self._write_expense_to_file(updated_expenses)
        logger.info(f"Deleted the Expense with ID: {expense_id}")
