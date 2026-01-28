from pydantic import BaseModel
from typing import Optional

class CauseListQuery(BaseModel):
    from_date: str
    to_date: str
    court: Optional[str] = None
