############################################
# BASE
############################################
FROM python:3.12-alpine3.20 AS base

ARG POETRY_VERSION="2.1.1"

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./

RUN pip install --upgrade pip && pip install poetry==$POETRY_VERSION

############################################
# BUILD
############################################
FROM base AS build

WORKDIR /app

RUN poetry install --no-root --only main

COPY ./x1201_exporter ./x1201_exporter
COPY ./README.md ./README.md

RUN poetry build

############################################
# TEST STAGE
############################################
FROM build AS test

RUN apk add --no-cache pre-commit git gcc python3-dev musl-dev

RUN git init

COPY ./.pre-commit-config.yaml ./.pre-commit-config.yaml
COPY ./pytest.ini ./pytest.ini

RUN pre-commit run -a --show-diff-on-failure

RUN pytest -v -m unit

############################################
# PRODUCTION STAGE
############################################
FROM python:3.12-alpine3.20 AS production

COPY --from=build /app/dist/*.whl /app/

RUN pip install --no-cache-dir /app/*.whl

EXPOSE 80

ENTRYPOINT ["uvicorn", "x1201_exporter.exporter:app", "--host", "0.0.0.0", "--port", "80"]
