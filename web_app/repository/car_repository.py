from collections.abc import Sequence

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from project.database import get_db
from project.models import Car, City, Profession, User
from web_app import schemas
from sqlalchemy import select, or_


class CarRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = Car

    def get_car(self, car_model: str) -> Car:
        car = self.db.query(Car).filter(Car.car_model == car_model).first()
        if car:
            return car
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="car not found")

    def get_car_list(self) -> Sequence[Car]:
        return self.db.query(Car).all()

    def create_car(self, car: schemas.CarSchema) -> Car:
        new_car_db = self.model(car_model=car.car_model)
        self.db.add(new_car_db)
        self.db.commit()
        self.db.refresh(new_car_db)
        return new_car_db

    def update_car(self, new_car_data: schemas.CarSchema, car_model: str) -> Car:
        old_car = self.get_car(car_model)
        if old_car:
            old_car.car_model = new_car_data.car_model
            self.db.commit()
            self.db.refresh(old_car)
            return old_car
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="car not found")

    def delete_car(self, car_model: str):
        car = self.db.scalars(select(Car).filter_by(car_model=car_model)).first()
        if car:
            self.db.delete(car)
            self.db.commit()
            return {"status": True,
                    "message": "The car has been deleted"}
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="car not found")


class CityRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = City

    def create_city(self, city: schemas.CitySchema) -> City:
        new_city_db = self.model(live_city=city.live_city)
        self.db.add(new_city_db)
        self.db.commit()
        self.db.refresh(new_city_db)
        return new_city_db


class ProfessionRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = Profession

    def create_profession(self, profession: schemas.ProfessionSchema) -> Profession:
        new_profession_db = self.model(type_profession=profession.type_profession)
        self.db.add(new_profession_db)
        self.db.commit()
        self.db.refresh(new_profession_db)
        return new_profession_db


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = User

    def create_user(self, user: schemas.UserCreateSchema) -> User:
        new_user_db = self.model(username=user.username, email=user.email, car_model=user.car_model,
                                 type_profession=user.type_profession, live_city=user.live_city)
        self.db.add(new_user_db)
        self.db.commit()
        self.db.refresh(new_user_db)
        return new_user_db

    def get_user_list(self) -> Sequence[User]:
        return self.db.query(User).all()

    def get_users_by_filter(self, find_car, find_pro, find_city) -> Sequence[User]:
        not_none_filters = []
        query = select(User).outerjoin(Car).outerjoin(Profession).outerjoin(City).distinct()
        if find_car and find_car != "Выберите марку автомобиля":
            not_none_filters.append(Car.car_model == find_car)
        if find_pro and find_pro != "Выберите профессию":
            not_none_filters.append(Profession.type_profession == find_pro)
        if find_city and find_city != "Выберите город проживания":
            not_none_filters.append(City.live_city == find_city)
        if not_none_filters:
            query = query.where(or_(*not_none_filters))
        result = self.db.execute(query)
        return result.scalars().all()
