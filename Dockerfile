FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for building any wheels (minimize)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r /app/requirements.txt

# copy app
COPY . /app

# add non-root user and prepare writable data dir for SQLite
RUN groupadd -r app && useradd -r -g app app \
  && mkdir -p /data \
  && chown -R app:app /app /data
USER app

# Default port (can be overridden by platform)
ENV PORT=5000

EXPOSE 5000

# run idempotent seeding, then start gunicorn bound to $PORT; keep workers low by default on small instances
CMD ["sh", "-c", "python -c 'from seed_data import ensure_seed_products; ensure_seed_products()' && gunicorn app:app --bind 0.0.0.0:${PORT} --workers ${WEB_CONCURRENCY:-1}"]
