from enum import Enum

from pydantic import BaseModel


class CarModel(str, Enum):
    jeep_wk2 = "Jeep Grand Cherokee WK2"
    jeep_wrangler = "Jeep Wrangler"
    bmw_x6 = "BMW x6"
    audi_a4 = "Audi a4"
    mercedes_ml300 = "Mercedes ML300"
    opel_astra = "Opel Astra gtc"
    ferrari_sf90 = "Ferrari SF90 STRADALE"


class CarSchema(BaseModel):
    car_model: str


class CitySchema(BaseModel):
    live_city: str


class CityModel(str, Enum):
    mcs = "Moscow"
    spb = "Saint-Petersburg"
    ny = "New York"
    la = "Los Angeles"
    london = "London"
    milan = "Milan"
    roma = "Roma"


class ProfessionSchema(BaseModel):
    type_profession: str


class ProModel(str, Enum):
    dev = "Developer"
    mus = "Musician"
    prog = "Programmer"
    dealer = "Dealer"
    dtr = "Doctor"
    bus = "Businessman"
    sport = "Sportsman"


class UserCreateSchema(BaseModel):
    username: str
    email: str
    car_model: str | None = None
    type_profession: str | None = None
    live_city: str | None = None


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    car_model: str | None = None
    type_profession: str | None = None
    live_city: str | None = None
