FROM python:3.13-slim
RUN useradd -ms /bin/sh -u 1001 app

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/

COPY pyproject.toml poetry.lock ./
COPY --chown=app:app domus_backend ./domus_backend
RUN touch README.md

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

USER app

EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "--reload", "domus_backend.app:app" ]
