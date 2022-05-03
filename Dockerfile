FROM python:3.7.12
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock /code/
RUN poetry install
COPY . /code/
RUN python3 manage.py migrate
RUN python3 manage.py createsuperuser