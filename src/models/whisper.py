import datetime
from typing import Dict, Optional
from pydantic import BaseModel


class Whisper(BaseModel):
    id: Optional[str]
    name: str
    text: str
    language: str
    english: Optional[str]
    processing_time: datetime.timedelta

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "text": self.text,
            "language": self.language,
            "english": self.english,  # Format date as string
            "processing_time": self.processing_time.total_seconds()  # Format date as string
        }