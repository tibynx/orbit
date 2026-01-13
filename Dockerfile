## Build stage
FROM python:3.14-alpine AS build-stage

# set environment
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# set venv and copy requirements
RUN python -m venv /app/venv
COPY requirements.txt .

# install packages
RUN pip install --no-cache-dir -r requirements.txt

## Runtime stage
FROM python:3.14-alpine AS runtime-stage

ARG IMAGE_BUILD_DATE
LABEL org.opencontainers.image.authors="tibynx"
LABEL org.opencontainers.image.created="${IMAGE_BUILD_DATE}"
LABEL org.opencontainers.image.description="A simple discord bot made with discord.py"
LABEL org.opencontainers.image.documentation="https://github.com/tibynx/orbit/blob/main/README.md"
LABEL org.opencontainers.image.licenses="GPL-3.0"
LABEL org.opencontainers.image.source="https://github.com/tibynx/orbit"
LABEL org.opencontainers.image.title="Orbit"
LABEL org.opencontainers.image.url="https://github.com/tibynx/orbit/packages"
LABEL org.opencontainers.image.vendor="tibynx"
LABEL org.opencontainers.image.base.name="python:3.14-alpine"
LABEL org.opencontainers.image.base.documentation="https://hub.docker.com/_/python"

# set environment
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# copy files from build-stage
COPY --from=build-stage /app/venv /app/venv
COPY . .

# run the app
CMD ["python", "main.py"]
VOLUME [ "logs" ]