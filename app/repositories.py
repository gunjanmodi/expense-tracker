from typing import List, Dict
from .boundaries import ExpenseRepositoryInterface, FileHandlerInterface
from .models import Expense

from .utils.logger_config import setup_logger
LOGGER = setup_logger()


class ExpenseJsonRepository(ExpenseRepositoryInterface):

    def __init__(self, file_handler: FileHandlerInterface, logger=LOGGER):
        self.file_handler = file_handler
        self.logger = logger

    def add_expense(self, new_expense: Expense) -> Expense:
        expenses = self.get_all_expenses()
        self._assign_new_id(new_expense, expenses)
        expenses.append(new_expense)
        self._save_expense(expenses)
        self.logger.info(f"Expense added successfully (ID: {new_expense.id})")
        return new_expense

    def get_all_expenses(self) -> List[Expense]:
        raw_data = self.file_handler.read()
        return [Expense(**data) for data in raw_data]

    def delete_expense(self, expense_id) -> None:
        expenses = self.get_all_expenses()
        updated_expenses = [expense for expense in expenses if expense.id != expense_id]
        if len(expenses) == len(updated_expenses):
            raise ValueError(f"Expense with ID {expense_id} not found.")
        self._save_expense(updated_expenses)
        self.logger.info(f"Deleted the Expense with ID: {expense_id}")

    def _assign_new_id(self, new_expense: Expense, expenses: List[Expense]) -> None:
        new_expense.id = max([expense.id for expense in expenses], default=0) + 1

    def _save_expense(self, expenses: List[Expense]):
        data: List[Dict] = [expense.model_dump() for expense in expenses]
        self.file_handler.write(data)


