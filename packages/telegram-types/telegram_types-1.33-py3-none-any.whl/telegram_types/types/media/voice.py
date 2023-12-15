from typing import Optional

from telegram_types.base import Base


class Voice(Base):
    owner_id: int
    file_id: str
    file_unique_id: str
    duration: int
    waveform: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    date: Optional[int] = None
