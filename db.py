from datetime import datetime, timezone

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DB_PATH
from models import Base, Student

engine = create_async_engine(
	f"sqlite+aiosqlite:///{DB_PATH}",
)

Session = async_sessionmaker(
	engine,
	class_=AsyncSession,
	expire_on_commit=False,
)

async def init_db():
	DB_PATH.parent.mkdir(parents=True, exist_ok=True)

	async with engine.begin() as connection:
		await connection.run_sync(Base.metadata.create_all)

async def student_exists(student_id: str) -> bool:
	async with Session() as session:
		result = await session.scalar(
			select(exists().where(Student.student_id == student_id))
		)

		return result

async def get_discord_id(student_id: str) -> str:
	async with Session() as session:
		student = await session.get(Student, student_id)

		return student.discord_id

async def update_discord_id(student_id: str, discord_id: str) -> None:
	async with Session() as session:
		student = await session.get(Student, student_id)

		student.discord_id = discord_id

		await session.commit()

async def update_student_verified_at(student_id: str) -> None:
	async with Session() as session:
		student = await session.get(Student, student_id)

		student.verified_at = datetime.now(timezone.utc)

		await session.commit()