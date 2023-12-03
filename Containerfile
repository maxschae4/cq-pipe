FROM python:3.10-slim-buster as builder

# we could instead convert the poetry.lock to requirements.txt
# that would avoid using poetry here
RUN pip install --no-cache-dir poetry==1.1.12

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.10-slim-buster as runtime

WORKDIR /app

# we could avoid using the virtual environment entirely for a production-ready build.
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY cq_pipe ./cq_pipe

ENTRYPOINT ["celery", "--app", "cq_pipe", "worker", "--loglevel", "INFO"]
