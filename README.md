# fastapi-mysql-emails-test
Тестовое задание на FastAPI и MySQL.

## Описание задания: Сервис email-рассылок

В базе 3 произвольных справочника.
Таблица пользователей, у каждого есть emai и произвольный набор значений этих 3-х справочников (множественный выбор).
Возможность указать значения справочников и получить список пользователей, которые подходят под эти критерии.
Поле для ввода текстового сообщения и кнопка "Отправить".
При нажатии: "Отправить" отправляются Email с текстовым сообщением выбранным пользователям.
Должно работать асинхронно и быстро.
Итого необходимо:
1. сделать бэкэнд 
2. Оформить API эндпоинт с помощью fastapi, который будет возвращать эти данные
3. Небольшой фронт (символически)
4. Оформить всё в Docker

# Инструкция по развёртыванию
Скачать исходный код проекта: `git clone https://github.com/Sana451/restaurant_fastapi_celery.git`    
Перейти в папку с проектом: `cd restaurant_fastapi_celery/`    
Произвести сборку проекта: `docker compose build`    
Создать и запустить контейнеры: `docker compose up`    

## Проверка работы
Запустить тесты POSTMAN или тестировать API вручную    
[Swagger автоматическая документация: http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)