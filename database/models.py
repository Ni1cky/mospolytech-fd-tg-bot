import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.sqlalchemy_base import Base


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_user_id: Mapped[str] = mapped_column(unique=True, index=True)
    dttm_created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    personal_info: Mapped["PersonalInfo"] = relationship("PersonalInfo", back_populates="person", uselist=False)
    person_programs: Mapped[list["PersonProgram"]] = relationship("PersonProgram", back_populates="person")


class PersonProgram(Base):
    __tablename__ = "person_programs"

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id"), primary_key=True)
    dttm_created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    dttm_asked: Mapped[datetime.datetime | None]
    dttm_answered: Mapped[datetime.datetime | None]
    contract_signed: Mapped[bool] = mapped_column(default=False)

    person: Mapped["Person"] = relationship("Person", back_populates="person_programs")
    program: Mapped["Program"] = relationship("Program", back_populates="person_programs")


class PersonalInfo(Base):
    __tablename__ = "personal_info"

    user_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    full_name: Mapped[str]
    birthdate: Mapped[datetime.date]
    registration_address: Mapped[str | None]
    residential_address: Mapped[str | None]
    passport_number: Mapped[str]
    passport_given_by: Mapped[str]
    passport_given_date: Mapped[datetime.date]
    snils: Mapped[str | None]
    phone: Mapped[str]
    email: Mapped[str]

    person: Mapped["Person"] = relationship("Person", back_populates="personal_info")


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str | None]
    duration_hrs: Mapped[int]
    price: Mapped[int]
    study_mode: Mapped[str]
    qualification: Mapped[str | None]

    person_programs: Mapped[list["PersonProgram"]] = relationship("PersonProgram", back_populates="program")
