FROM python:3.12.2-alpine AS build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    APP_HOME=/usr/src/web \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR $APP_HOME

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev libpq-dev bash

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY ./web/pyproject.toml ./web/poetry.lock ./

RUN poetry install --no-interaction --no-root

FROM python:3.12.2-alpine AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/usr/src/web

WORKDIR $APP_HOME

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu

RUN addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID"

COPY --from=build $APP_HOME /app

ENV PATH="/app/.venv/bin:$PATH"

RUN chown -R $USER:$USER $APP_HOME

RUN mkdir -p /usr/src/logs

RUN chown -R $USER:$USER /usr/src/logs

EXPOSE 8000

USER $USER

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
