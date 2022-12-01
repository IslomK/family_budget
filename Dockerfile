FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /tmp

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8080

# Install Poetry
RUN pip install poetry
RUN export PATH="/etc/poetry/bin:$PATH"

RUN poetry config virtualenvs.create true

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry install --no-root --no-dev

COPY family_budget /app
