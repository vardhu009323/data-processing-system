
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="completed"
    )

    input_size: Mapped[int] = mapped_column(Integer)

    result: Mapped[dict] = mapped_column(JSON)
