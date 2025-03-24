FROM python:3.12-slim

ENV POETRY_VERSION=1.8.4 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y curl build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /project/

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --with dev

COPY app/data /project/data
COPY ./alembic.ini /project/alembic.ini
COPY ./app /project/app

CMD ["sh", "-c", "alembic -c alembic.ini upgrade head && python app/main.py"]
