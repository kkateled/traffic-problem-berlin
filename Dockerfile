FROM python:3.11.9-slim

COPY . /app

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install poetry
RUN poetry install

CMD ["python", "main.py"]