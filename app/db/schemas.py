from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json


class BudgetEntered(BaseModel):
    project_id: str
    year: int
    month: int
    budget: int
    modified_at: str
