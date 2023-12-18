from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr
from typing import Optional
from sqlalchemy import BaseModel

class Base(DeclarativeBase):
    pass

class User(Base, BaseModel):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Username:Mapped[str] = mapped_column(String(200), unique=True)
    Confirm_Username:Mapped[str] = mapped_column(String(200), unique=True)

    Password:Mapped[str] = mapped_column(String(255))
    Confirm_Password:Mapped[str] = mapped_column(String(255))