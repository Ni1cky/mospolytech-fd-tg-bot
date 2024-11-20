import datetime
from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.sqlalchemy_base import Base


class PersonalInfo(Base):
    __tablename__ = "personal_info"

    user_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    birthdate: Mapped[datetime.date] = mapped_column(nullable=False)
    registration_address: Mapped[str] = mapped_column(Text, nullable=True)
    residential_address: Mapped[str] = mapped_column(Text, nullable=True)
    passport_number: Mapped[str] = mapped_column(String(10), nullable=False)
    passport_given_by: Mapped[str] = mapped_column(Text, nullable=False)
    passport_given_date: Mapped[datetime.date] = mapped_column(nullable=False)
    snils: Mapped[str] = mapped_column(String(11), nullable=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)

    person: Mapped["Person"] = relationship("Person", back_populates="personal_info")

    def __repr__(self):
        return f"<PersonalInfo(user_id={self.user_id}, full_name={self.full_name})>"
