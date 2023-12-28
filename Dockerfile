FROM python:3.11.4-slim AS base

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

FROM base AS builder

RUN apt-get update \
  && apt-get -y install build-essential libpoppler-cpp-dev pkg-config

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM base AS test

RUN apt-get update \
  && apt-get -y install build-essential libpoppler-cpp-dev pkg-config

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

COPY monocloud ./monocloud
COPY tests ./tests
RUN poetry install

CMD ["python", "-m", "poetry", "run", "task", "full_test"]

FROM base AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN apt-get update \
  && apt-get -y install build-essential libpoppler-cpp-dev pkg-config
COPY monocloud ./monocloud

CMD ["python", "-m", "monocloud.main"]
