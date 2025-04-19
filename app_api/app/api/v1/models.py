from sqlmodel import SQLModel
from sqlmodel import Field

class TopicBan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    topic: str
