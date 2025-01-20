from typing import List, Optional

from .models import Expense
from .utils.logger_config import setup_logger
from .boundaries import ExpenseRepositoryInterface


logger = setup_logger()


class ExpenseService:

    def __init__(self, expense_repository: ExpenseRepositoryInterface):
        self.repository = expense_repository

    def add_expense(self, description: str, amount: float, category: Optional[str]='') -> Expense:
        new_expense = self.repository.add_expense(Expense(description=description, amount=amount, category=category))
        return new_expense

    def list_expenses(self, category: Optional[str]='') -> List[Expense]:
        if category:
            return self.repository.get_all_expenses_by_category(category)
        return self.repository.get_all_expenses()

    def summary(self):
        return self.repository.total_expense()

    def delete(self, expense_id: int) -> None:
        self.repository.delete_expense(expense_id)

    def clear_all_expenses(self) -> None:
        self.repository.clear_all_expenses()