from dataclasses import dataclass
from datetime import date

@dataclass
class Member:
	student_id: str
	join_date: date