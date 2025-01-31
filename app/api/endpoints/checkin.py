from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.base import User
from app.database import get_db
from app.auth import get_current_user
from app.schemas.checkin import CheckinQuery, CheckinResponse, CheckinCreate
from app.crud.checkin import get_monthly_checkins, create_checkin

router = APIRouter()

@router.post("/records", response_model=CheckinResponse)
async def get_checkin_records(
    query: CheckinQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = await get_monthly_checkins(
        db=db,
        user_uid=current_user.uid,
        year=query.year,
        month=query.month
    )
    return CheckinResponse(records=records)

@router.post("/", response_model=dict)
async def create_user_checkin(
    checkin: CheckinCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = await create_checkin(
        db=db,
        user_uid=current_user.uid,
        checkin_date=checkin.checkin_date
    )
    return {"status": "success", "message": "簽到成功"}