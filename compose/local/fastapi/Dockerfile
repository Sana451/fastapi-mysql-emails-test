FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt
COPY . /app

COPY ./compose/local/fastapi/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start




#RUN apt-get update \
#  # dependencies for building Python packages
#  && apt-get install -y build-essential \
#
## Requirements are installed here to ensure they will be cached.
#COPY ./requirements.txt /requirements.txt
#
#RUN pip install -r /requirements.txt
#
##COPY ./compose/local/fastapi/entrypoint /entrypoint
##RUN sed -i 's/\r$//g' /entrypoint
##RUN chmod +x /entrypoint
#
COPY ./compose/local/fastapi/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
#
#
#WORKDIR /app
#
##ENTRYPOINT ["/entrypoint"]


