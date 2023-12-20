from typing import Optional, List

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy_utils import EmailType

from project.database import Base


class Car(Base):
    __tablename__ = "cars"
    car_model: Mapped[str] = mapped_column(String(30), primary_key=True, unique=True, nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates="car")


class City(Base):
    __tablename__ = "cities"
    live_city: Mapped[str] = mapped_column(String(30), primary_key=True, unique=True, nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates="city")


class Profession(Base):
    __tablename__ = "professions"
    type_profession: Mapped[str] = mapped_column(String(30), primary_key=True, unique=True, nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates="profession")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(EmailType, nullable=False)

    live_city: Mapped[Optional[str]] = mapped_column(
        ForeignKey("cities.live_city", onupdate="CASCADE", ondelete="CASCADE"))
    city: Mapped[Optional["City"]] = relationship(back_populates="users")

    type_profession: Mapped[Optional[str]] = mapped_column(
        ForeignKey("professions.type_profession", onupdate="CASCADE", ondelete="CASCADE"))
    profession: Mapped[Optional["Profession"]] = relationship(back_populates="users")

    car_model: Mapped[Optional[str]] = mapped_column(
        ForeignKey("cars.car_model", onupdate="CASCADE", ondelete="CASCADE"))
    car: Mapped[Optional["Car"]] = relationship(back_populates="users")
