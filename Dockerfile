FROM python:3.12.3-slim-bullseye
WORKDIR /app

COPY requirements.txt ./
RUN apt update \
    && apt install -y --no-install-recommends \
       postgresql-client \
       build-essential \
       libjpeg-dev \
       zlib1g-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt remove -y build-essential libjpeg-dev zlib1g-dev \
    && apt autoremove -y \
    && apt clean

COPY . ./
CMD ["sh", "-c", "python manage.py migrate --noinput && exec python manage.py runserver 0.0.0.0:8000"]
