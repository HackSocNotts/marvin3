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

async def verify_student_exists(student_id: str) -> bool:
	async with Session() as session:
		result = await session.scalar(
			select(exists().where(Student.student_id == student_id))
		)

		return result