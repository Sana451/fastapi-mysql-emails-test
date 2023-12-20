from fastapi import Depends

from project.models import Car, User
from web_app.repository.car_repository import CarRepository, CityRepository, ProfessionRepository, UserRepository
from web_app import schemas


class CarService:
    def __init__(self, db_repository: CarRepository = Depends()):
        self.db_repository = db_repository

    def get_all(self) -> list[Car]:
        db_menus = self.db_repository.get_car_list()
        return db_menus

    def get(self, car_model: str) -> Car:
        db_item = self.db_repository.get_car(car_model)
        return db_item

    def create(self, car: schemas.CarSchema):
        db_item = self.db_repository.create_car(car)
        return db_item

    def update(self, new_car_data: schemas.CarSchema, car_model: str):
        db_item = self.db_repository.update_car(new_car_data, car_model)
        return db_item

    def delete(self, car_model: str):
        item = self.db_repository.delete_car(car_model)
        return item


class CityService:
    def __init__(self, db_repository: CityRepository = Depends()):
        self.db_repository = db_repository

    def create(self, city: schemas.CitySchema):
        db_item = self.db_repository.create_city(city)
        return db_item


class ProfessionService:
    def __init__(self, db_repository: ProfessionRepository = Depends()):
        self.db_repository = db_repository

    def create(self, profession: schemas.ProfessionSchema):
        db_item = self.db_repository.create_profession(profession)
        return db_item


class UserService:
    def __init__(self, db_repository: UserRepository = Depends()):
        self.db_repository = db_repository

    def create(self, user: schemas.UserCreateSchema):
        db_item = self.db_repository.create_user(user)
        return db_item

    def get_all(self) -> list[User]:
        db_users = self.db_repository.get_user_list()
        return db_users

    def search_users_by_filter(self, find_car, find_pro, find_city) -> list[User]:
        db_users = self.db_repository.get_users_by_filter(find_car, find_pro, find_city)
        return db_users
