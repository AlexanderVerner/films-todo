FROM python:3.10.3-slim-bullseye
WORKDIR /app

COPY Pipfile* ./
RUN apt update \
    && pip install --no-cache-dir pipenv \
    && pipenv install --system --deploy

COPY . ./
CMD ["sh", "-c", "python manage.py migrate --noinput && exec python manage.py runserver 0.0.0.0:8000"]
