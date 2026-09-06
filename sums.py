import asyncio

import db
from sums_api.client import SumsClient

async def sync():
	def extract():
		sc = SumsClient()

		try:
			return sc.extract_members()
		finally:
			sc.driver.quit()

	members = await asyncio.to_thread(extract) # to_thread will avoid blocking anything else marvin does

	new_members = await db.sync_members(members)
	return new_members