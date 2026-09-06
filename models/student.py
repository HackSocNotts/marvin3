from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Student(Base):
	__tablename__ = "students"

	student_id: Mapped[str] = mapped_column(String, primary_key=True)
	discord_id: Mapped[str | None] = mapped_column(String, unique=True)
	join_date: Mapped[datetime | None]
	verified_at: Mapped[datetime | None]
