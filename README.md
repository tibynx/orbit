# 🌑 Orbit

Orbit is a simple discord bot made with discord.py. You can get funny memes, cool facts, and much more! This bot uses hybrid commands, which means you can use both slash commands and traditional prefixed commands.

## Setup

To run the bot, you can use docker or source. For authentication, get a bot token from the [Discord Developer Portal](https://discord.com/developers/applications)! Make sure to enable the `Server Members Intent` and the `Message Content Intent` for your bot!

### Docker

```bash
docker run -d \
  --name=orbit \
  -e BOT_TOKEN=your-bot-token \
  ghcr.io/tibor309/orbit:latest
```

### Source

Before running the bot, make sure to install all the required python packages with the command below. At least python 3.10 is required!
```bash
pip3 install -r requirements.txt
```

Create an `.env` file according to the `.env.example` file! Do not share your bot token with anyone!

```
BOT_TOKEN=your_bot_token_here
```

If you're ready, run the bot with the `python3 main.py` command!

### Environment Variables

|  Variable  | Description                                                                                                     |
|:----------:|-----------------------------------------------------------------------------------------------------------------|
| BOT_TOKEN  | Your bot token. Do not share this with anyone!                                                                  |
| BOT_PREFIX | The prefix for the bot. Instead of slash commands, you can also use the bot with traditional prefixed commands. |
| BOT_COLOR  | The color of the embeds in integral format. (Example: `#B4BEFE` to `0xB4BEFE`.) This value is optional.         |
