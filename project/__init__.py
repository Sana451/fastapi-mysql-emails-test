from typing import Any, Annotated

from fastapi import FastAPI, Depends, status, Form
from fastapi_mail import MessageSchema, MessageType, FastMail
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse

from project.database import get_db
from project.filters import UserFilter
from project.models import User, Car, Profession, City
from project.send_mail import conf
from web_app import schemas
from web_app.schemas import CarModel, CityModel, ProModel
from web_app.service.car_service import CarService, CityService, ProfessionService, UserService


def create_app() -> FastAPI:
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")

    @app.get("/car", response_model=list[schemas.CarSchema])
    def read_car_list(car: CarService = Depends()):
        return car.get_all()

    @app.get("/car/{car_model}", response_model=schemas.CarSchema)
    def read_car(car_model: str, car: CarService = Depends()):
        return car.get(car_model)

    @app.post("/car", status_code=status.HTTP_201_CREATED, response_model=schemas.CarSchema)
    def create_car(new_car: schemas.CarSchema, car: CarService = Depends(), car_input: CarModel = None):
        if car_input:
            new_car.car_model = car_input.value
        return car.create(new_car)

    @app.post("/city", status_code=status.HTTP_201_CREATED, response_model=schemas.CitySchema)
    def create_city(new_city: schemas.CitySchema, city: CityService = Depends(), city_input: CityModel = None):
        if city_input:
            new_city.live_city = city_input.value
        return city.create(new_city)

    @app.post("/profession", status_code=status.HTTP_201_CREATED, response_model=schemas.ProfessionSchema)
    def create_profession(new_profession: schemas.ProfessionSchema, profession: ProfessionService = Depends(),
                          input_pro: ProModel = None):
        if input_pro:
            new_profession.type_profession = input_pro.value
        return profession.create(new_profession)

    @app.patch("/cars/{car_model}", response_model=schemas.CarSchema)
    def update_car(car_model: str, new_car_data: schemas.CarSchema, car: CarService = Depends()):
        updated_car = car.update(new_car_data, car_model)
        return updated_car

    @app.delete("/cars/{car_model}", status_code=status.HTTP_200_OK)
    def delete_car(car_model: str, car: CarService = Depends()):
        deleted_car = car.delete(car_model)
        return deleted_car

    @app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateSchema)
    def create_user(new_user: schemas.UserCreateSchema, user: UserService = Depends(),
                    car_input: CarModel = None,
                    pro_input: ProModel = None,
                    city_input: CityModel = None):
        if car_input:
            new_user.car_model = car_input.value
        if pro_input:
            new_user.type_profession = pro_input.value
        if city_input:
            new_user.live_city = city_input.value
        return user.create(new_user)

    @app.get("/user", response_model=list[schemas.UserSchema])
    def read_user_list(user: UserService = Depends()):
        return user.get_all()

    @app.get("/user-filter", response_model=list[schemas.UserSchema])
    def read_user_list_filter(find_car: CarModel = None,
                              find_pro: ProModel = None,
                              find_city: CityModel = None,
                              user: UserService = Depends()) -> Any:
        return user.search_users_by_filter(find_car, find_pro, find_city)

    @app.post("/send-mail-users-filter/", response_model=list[schemas.UserSchema])
    async def filter_users(find_car: CarModel = None,
                           find_pro: ProModel = None,
                           find_city: CityModel = None,
                           user: UserService = Depends(),
                           message: Annotated[str, Form()] = "") -> Any:
        users = user.search_users_by_filter(find_car, find_pro, find_city)
        mails = [user.email for user in users]

        html = f"""<p>{message}</p> """
        message = MessageSchema(
            subject="Рассылка спама fastapi-приложением",
            recipients=mails,
            body=html,
            subtype=MessageType.html)

        fm = FastMail(conf)
        try:
            await fm.send_message(message)
        except ValueError:
            return JSONResponse(status_code=200,
                                content={"Ошибка отправки сообщений": f"Не найдено адресатов для отправки"})

        return JSONResponse(status_code=200,
                            content={"Сообщения отправлены успешно": f"Получатели: {message.recipients}"})

    @app.get("/email-form/", response_class=HTMLResponse)
    async def get_email_form(request: Request, user: UserService = Depends()):
        users = user.get_all()
        return templates.TemplateResponse("index.html", {"request": request, "users": users})

    @app.post("/email-form/", response_class=HTMLResponse)
    async def post_email_form(request: Request, user: UserService = Depends()):
        async with request.form() as form:
            message = form.get('message')

            find_car = form.get('find_car')
            if find_car == "Выберите марку автомобиля":
                find_car = form.get('input_car')
            find_pro = form.get('find_pro')
            if find_pro == "Выберите профессию":
                find_pro = form.get('input_pro')
            find_city = form.get('find_city')
            if find_city == "Выберите город проживания":
                find_city = form.get('input_city')

        users = user.search_users_by_filter(find_car, find_pro, find_city)
        mails = [user.email for user in users]
        mails.append("sanamamail451@gmail.com")

        html = f"""<p>{message}</p> """
        message = MessageSchema(
            subject="Рассылка спама fastapi-приложением",
            recipients=mails,
            body=html,
            subtype=MessageType.html)

        fm = FastMail(conf)
        try:
            await fm.send_message(message)
        except ValueError:
            return JSONResponse(status_code=200,
                                content={"Ошибка отправки сообщений": f"Не найдено адресатов для отправки"})

        return JSONResponse(status_code=200,
                            content={"Сообщения отправлены успешно": f"Получатели: {message.recipients}"})

    return app
