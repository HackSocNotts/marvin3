import aiosqlite
from config import DB_PATH

async def init():
	DB_PATH.parent.mkdir(parents=True, exist_ok=True)

	async with aiosqlite.connect(DB_PATH) as db:
		await db.execute(
			"""
			CREATE TABLE IF NOT EXISTS students (
				student_id TEXT PRIMARY_KEY,
				join_date TEXT NOT NULL,
				discord_id TEXT UNIQUE,
				verified_at TEXT
			)
			"""
		)

		await db.commit()