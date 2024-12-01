from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.sqlalchemy_base import Base


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    duration_hrs: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    study_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    qualification: Mapped[str] = mapped_column(String(100), nullable=True)

    person_programs: Mapped[list["PersonProgram"]] = relationship("PersonProgram", back_populates="program")

    def __repr__(self):
        return f"<Program(id={self.id}, title={self.title})>"
