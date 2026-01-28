from fastapi import APIRouter, Query
from .models import CauseListQuery
from .services.cause_list_service import fetch_cause_list

router = APIRouter()

@router.get("/cause-list")
async def cause_list(
    from_date: str = Query(...),
    to_date: str = Query(...),
    court: str | None = Query(None)
):
    params = CauseListQuery(from_date=from_date, to_date=to_date, court=court)
    return await fetch_cause_list(params)
