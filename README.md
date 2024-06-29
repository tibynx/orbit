# 🌑 Orbit
Orbit is a simple discord bot made with discord.py. You can get funny memes, images of foxes, and some info about a server or member.

## Setup
You can run the bot using the docker cli, or from source. To run the bot, you will need a bot token, that you can get from the [discord developer portal](https://discord.com/developers/applications).

### Docker
```bash
docker run -d --name orbit -e BOT_TOKEN=your-bot-token -e BOT_PREFIX=your-bot-prefix ghcr.io/tibor309/orbit:latest
```

### Source
Clone the repo, then install all the required packages with the command below. At least python 3.10 is required for the bot to run!
```bash
pip3 install -r requirements.txt
```

Create an `.env` file and fill it out with your values, like below.
```
BOT_TOKEN=your-bot-token
BOT_PREFIX=your-bot-prefix
```

If you're ready, run the bot with this command:
```bash
python3 main.py
```

## Config
You can change the color for embeds in the `settings.py` file.
