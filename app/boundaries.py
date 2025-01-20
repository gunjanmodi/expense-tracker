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
    def get_all_expenses_by_category(self, category: str) -> List[Expense]:
        pass

    @abstractmethod
    def delete_expense(self, expense_id: int) -> None:
        pass

    @abstractmethod
    def total_expense(self) -> float:
        pass

    @abstractmethod
    def total_expense_by_month(self, month) -> float:
        pass

    @abstractmethod
    def clear_all_expenses(self) -> None:
        pass


class FileHandlerInterface(ABC):
    @abstractmethod
    def read(self) -> List[Dict]:
        pass

    @abstractmethod
    def write(self, data: List[Dict]) -> None:
        pass
