from pydantic import BaseModel
from typing import List

class CauseItem(BaseModel):
    title: str
    court: str
    no_of_entries: int
    pdf_file: str
    file_size: str
    cause_date: str

class CauseListResponse(BaseModel):
    success: bool
    data: List[CauseItem]
    total_records: int
    message: str
