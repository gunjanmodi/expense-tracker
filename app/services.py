from typing import List

from .models import Expense
from .utils.logger_config import setup_logger
from .boundaries import ExpenseRepositoryInterface


logger = setup_logger()


class ExpenseService:

    def __init__(self, expense_repository: ExpenseRepositoryInterface):
        self.repository = expense_repository

    def add_expense(self, description: str, amount: float) -> Expense:
        new_expense = self.repository.add_expense(Expense(description=description, amount=amount))
        return new_expense


    def list_expenses(self) -> List[Expense]:
        return self.repository.get_all_expenses()


    def summary(self, ):
        pass


    def delete(self, expense_id: int) -> None:
        self.repository.delete_expense(expense_id)