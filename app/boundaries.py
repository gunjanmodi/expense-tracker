from abc import ABC, abstractmethod
from app.models import Expense
from typing import List


class ExpenseRepositoryInterface(ABC):

    @abstractmethod
    def save_expenses(self, expense: Expense) -> Expense:
        pass

    @abstractmethod
    def fetch_expenses(self) -> List[Expense]:
        pass

