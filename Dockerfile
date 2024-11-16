FROM python:3.12-alpine

RUN apk update --no-cache && apk upgrade --no-cache --available

RUN apk add --no-cache postgresql-libs

RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

WORKDIR /code

RUN pip install --no-cache-dir poetry psycopg2 alembic

COPY pyproject.toml /code

RUN poetry install

COPY main.py /code/main.py

COPY src /code/src

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "run"]
