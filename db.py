from datetime import datetime, timedelta, timezone, date

from sqlalchemy import exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DB_PATH, IGNORED_STUDENT_IDS
from models import Base, Student
from sums_api.member import Member

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

async def discord_id_exists(discord_id: str) -> bool:
	async with Session() as session:
		result = await session.scalar(
			select(exists().where(Student.discord_id == discord_id))
		)

		return result

async def get_student(student_id: str) -> Student | None:
	async with Session() as session:
		return await session.get(Student, student_id)

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

async def sync_members(members: list[Member]) -> int:
	new_members = 0
	async with Session() as session:
		for member in members:
			if member.student_id in IGNORED_STUDENT_IDS:
				continue # all this because of ASSOC150476

			student = await session.get(Student, member.student_id) 

			if student is None: # avoids overwriting existing students
				student = Student(
					student_id=member.student_id,
					join_date=member.join_date,
				)
				session.add(student)
				new_members += 1
			else:
				student.join_date = member.join_date

		await session.commit()
	return new_members

async def update_expired_members() -> int:
	cutoff = date.today() - timedelta(days=365)

	async with Session() as session:
		result = await session.execute(
			update(Student).where(
				Student.expired.is_(False),
				Student.join_date < cutoff,
			)
			.values(expired=True)
		)

		await session.commit()

		return result.rowcount or 0