FROM python:3.7.12
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
RUN pip3 install poetry && poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-dev
COPY . /code/
RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000