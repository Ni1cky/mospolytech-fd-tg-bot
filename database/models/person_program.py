import datetime
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.sqlalchemy_base import Base


class PersonProgram(Base):
    __tablename__ = "person_programs"

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id"), primary_key=True)
    dttm_created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow, nullable=False)
    dttm_asked: Mapped[datetime.datetime] = mapped_column(nullable=True)
    dttm_answered: Mapped[datetime.datetime] = mapped_column(nullable=True)
    contract_signed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    person: Mapped["Person"] = relationship("Person", back_populates="person_programs")
    program: Mapped["Program"] = relationship("Program", back_populates="person_programs")

    def __repr__(self):
        return f"<PersonProgram(person_id={self.person_id}, program_id={self.program_id})>"
