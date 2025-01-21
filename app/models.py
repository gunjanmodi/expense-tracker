from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Expense(BaseModel):
    id: int = None
    date: datetime = Field(default_factory=datetime.now)
    amount: float = Field()
    description: str = Field(min_length=1, max_length=100)
    category: Optional[str] = Field(default_factory=None, max_length=100)

    @field_validator('date',mode='after')
    @classmethod
    def validate_date(cls, date: datetime) -> datetime:
        now = datetime.now()
        if date > now:
            raise ValueError("Date cannot be in the future.")
        # Prevent excessively past dates
        min_date = now - timedelta(days=365 * 10)
        if date < min_date:
            raise ValueError(f"Date cannot be earlier than {min_date.strftime('%Y-%m-%d')}.")

        return date

    @field_validator('amount', mode='after')
    @classmethod
    def validate_amount(cls, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        if amount > 1e9:
            raise ValueError("Amount must not exceed 1 billion.")
        return amount
