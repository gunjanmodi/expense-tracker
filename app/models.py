from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Expense(BaseModel):
    id: Optional[int] = None
    date: datetime = Field(default_factory=datetime.now)
    amount: float
    description: str
    category: Optional[str] = None