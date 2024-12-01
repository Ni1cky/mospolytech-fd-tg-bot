import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.sqlalchemy_base import Base


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_user_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    dttm_created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow, nullable=False)

    personal_info: Mapped["PersonalInfo"] = relationship("PersonalInfo", back_populates="person", uselist=False)
    person_programs: Mapped[list["PersonProgram"]] = relationship("PersonProgram", back_populates="person")

    def __repr__(self):
        return f"<Person(id={self.id}, telegram_user_id={self.telegram_user_id})>"
