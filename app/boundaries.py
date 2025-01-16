from abc import ABC, abstractmethod
from app.models import Expense
from typing import List, Dict


class ExpenseRepositoryInterface(ABC):

    @abstractmethod
    def add_expense(self, expense: Expense) -> Expense:
        pass

    @abstractmethod
    def get_all_expenses(self) -> List[Expense]:
        pass

    @abstractmethod
    def delete_expense(self, expense_id: int) -> None:
        pass


class FileHandlerInterface(ABC):
    @abstractmethod
    def read(self) -> List[Dict]:
        pass

    @abstractmethod
    def write(self, data: List[Dict]):
        pass

