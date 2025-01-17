from datetime import datetime

from app.models import Expense
from unittest.mock import MagicMock
from app.services import ExpenseService
from app.repositories import ExpenseJsonRepository
from app.utils.json_file_handler import JSONFileHandler
from app.constants import TESTS_DATA_FILE


def test_add_expense():
    mock_repository = MagicMock()
    expense_service = ExpenseService(mock_repository)

    expense_service.add_expense("Grocery", 5000)

    mock_repository.add_expense.assert_called_once()
    saved_expense = mock_repository.add_expense.call_args[0][0]
    assert saved_expense.description == "Grocery"
    assert saved_expense.amount == 5000


def test_list_expenses():
    mock_repository = MagicMock(spec=ExpenseJsonRepository)
    expense_service = ExpenseService(mock_repository)

    mock_expenses = [
        Expense(id=1, date=datetime(2025, 1, 1, 10, 0, 0), amount=100.0, description="Grocery"),
        Expense(id=2, date=datetime(2025, 1, 2, 14, 0, 0), amount=200.0, description="Rent"),
    ]
    mock_repository.get_all_expenses.return_value = mock_expenses

    expenses = expense_service.list_expenses()
    assert len(expenses) == 2
    assert expenses[0].id == 1
    assert expenses[0].amount == 100.0
    assert expenses[0].description == "Grocery"
    assert expenses[0].date == datetime(2025, 1, 1, 10, 0, 0)

    assert expenses[1].id == 2
    assert expenses[1].amount == 200.0
    assert expenses[1].description == "Rent"
    assert expenses[1].date == datetime(2025, 1, 2, 14, 0, 0)

    mock_repository.get_all_expenses.assert_called_once()


def test_delete_expense():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)
    expense = expense_service.add_expense("Shoes", 1500)

    expense_service.delete(expense.id)
    remaining_expenses = expense_service.list_expenses()

    expenses_set = {expense.id for expense in remaining_expenses}
    assert expense.id not in expenses_set


def test_summary_expense():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    expense_service.add_expense("Grocery", 5000)
    expense_service.add_expense("Rent", 10000)

    total_expense = expense_service.summary()

    assert total_expense == 15000

    expense_service.clear_all_expenses()


