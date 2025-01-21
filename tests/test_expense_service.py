from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models import Expense
from unittest.mock import MagicMock
from app.services import ExpenseService
from app.repositories import ExpenseJsonRepository
from app.utils.json_file_handler import JSONFileHandler
from app.constants import TESTS_DATA_FILE


def test_add_expense_valid_data():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    expense = expense_service.add_expense("Grocery", 5000)
    assert expense.description == "Grocery"
    assert expense.amount == 5000

    expense_service.clear_all_expenses()


def test_add_expense_with_valid_category():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    grocery_expense = expense_service.add_expense("Grocery", 5000, "Basic")
    electricity_bill_expense = expense_service.add_expense("Electricity Bill", 3000, "Basic")
    movie_expense = expense_service.add_expense("Movie", 500, "Entertainment")

    assert grocery_expense.category == "Basic"
    assert electricity_bill_expense.category == "Basic"
    assert movie_expense.category == "Entertainment"

    expense_service.clear_all_expenses()


def test_list_expenses():
    mock_repository = MagicMock(spec=ExpenseJsonRepository)
    expense_service = ExpenseService(mock_repository)

    mock_expenses = [
        Expense(id=1, date=datetime(2025, 1, 1, 10, 0, 0), amount=100.0,
                description="Grocery", category="Example"),
        Expense(id=2, date=datetime(2025, 1, 2, 14, 0, 0), amount=200.0,
                description="Rent", category="Example"),
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


def test_list_expenses_with_valid_category():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)
    expense_service.add_expense("Grocery", 5000, "Basic")
    expense_service.add_expense("Electricity Bill", 3000, "Basic")
    expense_service.add_expense("Movie", 500, "Entertainment")

    expenses = expense_service.list_expenses('Basic')

    assert len(expenses) == 2
    assert expenses[0].amount == 5000
    assert expenses[0].description == "Grocery"
    assert expenses[0].category == "Basic"
    assert expenses[1].amount == 3000
    assert expenses[1].description == "Electricity Bill"
    assert expenses[1].category == "Basic"

    expense_service.clear_all_expenses()


def test_delete_expense():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)
    expense = expense_service.add_expense("Shoes", 1500)

    expense_service.delete(expense.id)
    remaining_expenses = expense_service.list_expenses()

    expenses_set = {expense.id for expense in remaining_expenses}
    assert expense.id not in expenses_set

    expense_service.clear_all_expenses()


def test_summary_expense():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    expense_service.add_expense("Grocery", 5000)
    expense_service.add_expense("Rent", 10000)

    total_expense = expense_service.summary()

    assert total_expense == 15000

    expense_service.clear_all_expenses()


def test_monthly_summary_expense():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    january_date = datetime(2025, 1, 10)
    expense_service.add_expense("Grocery", 5500, category="Basic", date_time=january_date)
    expense_service.add_expense("Rent", 11500, category="Basic", date_time=january_date)

    january_total_expense = expense_service.summary(january_date.month)

    assert january_total_expense == 17000

    expense_service.clear_all_expenses()


def test_add_expense_negative_amount():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)
    with pytest.raises(ValidationError):
        expense_service.add_expense("Grocery", -5000)
    expense_service.clear_all_expenses()

def test_add_expense_boundary_values_for_amount():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    with pytest.raises(ValidationError):
        expense_service.add_expense("Grocery", 0)

    with pytest.raises(ValidationError):
        expense_service.add_expense("Grocery", 1e9+0.01)

    expense_service.add_expense("Grocery", 1e9-0.01)

    expense_service.add_expense("Grocery", 1e9)

    expenses = expense_service.list_expenses()
    assert len(expenses) == 2
    expense_service.clear_all_expenses()

def test_add_expense_invalid_types_for_amount():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    with pytest.raises(ValidationError):
        expense_service.add_expense("Grocery", False)

    with pytest.raises(ValidationError):
        expense_service.add_expense("Grocery", None) # noqa

def test_add_expense_boundary_values_for_description():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    # Blank description
    with pytest.raises(ValidationError):
        expense_service.add_expense("", 100)

    # description having characters greater than 100
    with pytest.raises(ValidationError):
        expense_service.add_expense("a"*101, 100)

    # Exactly 1 character
    expense_service.add_expense("a", 100)

    # Exactly 100 character
    expense_service.add_expense("a" * 100, 100)

    expenses = expense_service.list_expenses()
    assert len(expenses) == 2

    expense_service.clear_all_expenses()


def test_add_expense_invalid_types_for_description():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    with pytest.raises(ValidationError):
        expense_service.add_expense(123, 100) # noqa


    with pytest.raises(ValidationError):
        expense_service.add_expense(True, 100) # noqa


    with pytest.raises(ValidationError):
        expense_service.add_expense(None, 100) # noqa

    expense_service.clear_all_expenses()


def test_add_expense_special_cases_for_description():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    # A string with spaces only
    expense_service.add_expense(" ", 100)

    # Special Chars
    expense_service.add_expense("@#$%^&*", 100)

    expenses = expense_service.list_expenses()
    assert len(expenses) == 2

    expense_service.clear_all_expenses()


def test_list_expenses_with_boundary_values_for_category():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)
    expense_service.add_expense("Grocery", 100, "a"*100)

    with pytest.raises(ValidationError):
        expense_service.add_expense("Grocery", 100, "a"*101)

    expenses = expense_service.list_expenses()
    assert len(expenses) == 1

    expense_service.clear_all_expenses()


def test_add_expense_special_cases_for_category():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)
    expense_service.add_expense("Grocery", 100, None)
    expense_service.add_expense("Grocery", 100, " ")
    expense_service.add_expense("Grocery", 100, "!@#$%^&*()")

    expenses = expense_service.list_expenses()
    assert len(expenses) == 3

    expense_service.clear_all_expenses()


def test_add_expense_invalid_type_for_category():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    with pytest.raises(ValidationError):
        expense_service.add_expense("Grocery", 100, 123) # noqa

    with pytest.raises(ValidationError):
        expense_service.add_expense("Grocery", 100, True) # noqa

    expenses = expense_service.list_expenses()
    assert len(expenses) == 0

    expense_service.clear_all_expenses()


def test_add_expense_invalid_date():
    repository = ExpenseJsonRepository(JSONFileHandler(TESTS_DATA_FILE))
    expense_service = ExpenseService(repository)

    with pytest.raises(ValidationError):
        future_date = datetime(2030, 1, 15)
        expense_service.add_expense("Grocery", 100, "Basic", future_date)

    with pytest.raises(ValidationError):
        extreme_past_date = datetime(2000, 5, 21)
        expense_service.add_expense("Grocery", 100, "Basic", extreme_past_date)

    expenses = expense_service.list_expenses()
    assert len(expenses) == 0

    expense_service.clear_all_expenses()


