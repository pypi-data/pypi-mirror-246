from typing import List, Optional

from .thumbnail import Thumbnail
from telegram_types.base import Base


class Document(Base):
    owner_id: int
    file_id: str
    file_unique_id: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    date: Optional[int] = None
    thumbs: Optional[List[Thumbnail]] = None
