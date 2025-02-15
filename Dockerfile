FROM python:3.12-alpine

# set labels
ARG IMAGE_BUILD_DATE
LABEL org.opencontainers.image.authors="tibor309"
LABEL org.opencontainers.image.created="${IMAGE_BUILD_DATE}"
LABEL org.opencontainers.image.title="Orbit"
LABEL org.opencontainers.image.description="A simple discord bot made with discord.py"
LABEL org.opencontainers.image.source=https://github.com/tibor309/orbit
LABEL org.opencontainers.image.url=https://github.com/tibor309/orbit/packages
LABEL org.opencontainers.image.licenses=GPL-3.0
LABEL org.opencontainers.image.base.name="python:3.12-alpine"

# install packages 
RUN \
    apk add --no-interactive build-base

# copy files
WORKDIR /app
COPY . .

# install requirements
RUN \
    pip3 install -r requirements.txt

# run the bot
CMD ["python3", "main.py"]