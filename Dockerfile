FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8080

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - && \
    poetry config virtualenvs.create true

# Copy using poetry.lock* in case it doesn't exist yet
COPY pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY family_budget /app
