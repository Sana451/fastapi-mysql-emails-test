from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from project.models import User


class UserFilter(Filter):
    car_model: Optional[str]
    type_profession: Optional[str]
    live_city: Optional[str]

    class Constants(Filter.Constants):
        model = User
