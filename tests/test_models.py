from datetime import datetime
from app.models import Expense


def test_create_expense_model():
    expense = Expense(id=0, date=datetime.now(), amount=1000, description="Example 1", category="Example 2")
    assert expense.id == 0
    assert expense.amount == 1000
    assert expense.description == "Example 1"
    assert expense.category == "Example 2"
