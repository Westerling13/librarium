FROM python:3.7-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential

RUN pip3 install poetry && poetry config virtualenvs.create false

WORKDIR /code
ARG secret_key
ENV SECRET_KEY=$secret_key
COPY poetry.lock pyproject.toml /code/

RUN poetry install

COPY . /code/
RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000