from pydantic import BaseModel
from datetime import date
from typing import List


class CheckinQuery(BaseModel):
    year: int
    month: int

class CheckinRecord(BaseModel):
    user_uid: str
    checkin_date: date
    signed_in: bool
    class Config:
        from_attributes = True

class CheckinResponse(BaseModel):
    records: List[CheckinRecord]

class CheckinCreate(BaseModel):
    checkin_date: date