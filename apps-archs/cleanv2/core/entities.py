from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    title: str
    content: str
    created_at: datetime = datetime.now()
