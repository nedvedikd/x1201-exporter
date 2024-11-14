############################################
# REQUIREMENTS STAGE
############################################
FROM python:3.12-alpine3.20 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

############################################
# BUILD STAGE
############################################
FROM python:3.12-alpine3.20 AS build

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./x1201_exporter /code/x1201_exporter

############################################
# TEST STAGE
############################################
FROM build AS test

RUN apk update && apk add pre-commit git gcc python3-dev musl-dev

RUN git init

COPY .pre-commit-config.yaml /code

RUN pre-commit run -a --show-diff-on-failure

############################################
# PRODUCTION STAGE
############################################
FROM build AS production

ENTRYPOINT ["uvicorn", "x1201_exporter.exporter:app", "--host", "0.0.0.0", "--port", "80"]
