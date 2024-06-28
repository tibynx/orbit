FROM python:3.12-slim-bookworm

# set labels
LABEL org.opencontainers.image.title="Orbit"
LABEL org.opencontainers.image.description="A simple discord bot made with discord.py"
LABEL org.opencontainers.image.source=https://github.com/tibor309/orbit
LABEL org.opencontainers.image.url=https://github.com/tibor309/orbit/packages
LABEL org.opencontainers.image.licenses=GPL-3.0

# install packages 
RUN apt update && apt install -y gcc

# set working directory
WORKDIR /app

# install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy files
COPY . .

# run the bot
CMD ["python3", "main.py"]