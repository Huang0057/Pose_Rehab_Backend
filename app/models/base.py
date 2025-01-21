from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Time, Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    uid = Column(String(8), unique=True, nullable=False)
    coins = Column(Integer, default=0)

class GameRecord(Base):
    __tablename__ = "game_records"
    id = Column(Integer, primary_key=True)
    user_uid = Column(String(30), ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
    part = Column(String(50), nullable=False)
    play_date = Column(Date, nullable=False)
    level_name = Column(String(100), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_time = Column(Interval, nullable=False)
    exercise_count = Column(Integer, nullable=False)
    coins_earned = Column(Integer, nullable=False)

class UserCheckin(Base):
    __tablename__ = "user_checkin"
    id = Column(Integer, primary_key=True)
    user_uid = Column(String(30), ForeignKey('users.uid', ondelete='CASCADE'), nullable=False)
    checkin_date = Column(Date, nullable=False)
    signed_in = Column(Boolean, default=False, nullable=False)