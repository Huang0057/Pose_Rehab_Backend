from pydantic import BaseModel
from datetime import date, time, timedelta

class GameRecordCreate(BaseModel):
    part: str
    play_date: date
    level_name: str
    start_time: time
    end_time: time
    duration_time: timedelta
    exercise_count: int
    coins_earned: int

class GameRecordResponse(GameRecordCreate):
    id: int
    user_uid: str

    class Config:
        from_attributes = True
