from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    Используется для наследования таблиц и работы с ORM.
    """
    metadata = MetaData()

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Автоматическое создание имени таблицы на основе имени класса.
        """
        return cls.__name__.lower()
