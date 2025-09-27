FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install chromium + driver
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    fonts-liberation \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "main.py"]

