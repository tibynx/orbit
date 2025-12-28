# 🌑 Orbit

Orbit is a simple discord bot made with discord.py. You can get funny memes, cool facts, and much more! This bot uses hybrid commands, which means you can use both slash commands and traditional prefixed commands.

## Setup

Create an application on the [Discord Developer Portal](https://discord.com/developers/applications), and copy the application ID and the bot token for later.

### Docker

If you prefer, you can set up the bot using Docker.

```sh
docker run -d \
  --name=orbit \
  -e BOT_TOKEN=your_bot_token_here \
  tibynx/orbit:latest
```

### Source

Clone the repo and install all required packages! Make sure you have at least Python 3.14 installed!

```sh
git clone https://github.com/tibynx/orbit.git
cd orbit
pip install -r requirements.txt
```

In the meantime, create an `.env` file according to the `.env.example` file! Do not share your bot token with anyone!

```sh
BOT_TOKEN="your_bot_token_here"
```

Then, you can run the bot using the `python main.py` command!

### Environment Variables

| Variable  | Description                                    |
|:---------:|------------------------------------------------|
| BOT_TOKEN | Your bot token. Do not share this with anyone! |


## Usage

After setting up, invite your bot to a server using this premade link! It already contains the proper permissions. Replace `<app-id>` with your bot's appication ID.

```sh
https://discord.com/oauth2/authorize?client_id=<app-id>&permissions=277025508352&integration_type=0&scope=bot+applications.commands
```
