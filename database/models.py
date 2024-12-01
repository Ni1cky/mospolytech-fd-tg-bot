import datetime

from sqlalchemy.orm import Mapped, mapped_column

from database.sqlalchemy_base import Base


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_user_id: Mapped[str] = mapped_column(unique=True, index=True)
    dttm_created: Mapped[datetime.datetime]
