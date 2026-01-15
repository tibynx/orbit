# 🌑 Orbit

Orbit is a simple, feature-rich Discord bot designed to bring fun, utility, and entertainment to your server. It integrates various APIs to provide a wide range of commands from games to random facts and image generation.

## Features

- **Fun & Games:** 8ball, text encoding/decoding.
- **Random Content:** Facts, dad jokes, colors, and periodic table elements.
- **Images & Memes:** Random memes, user petting GIFs, and lynx photos.
- **Easy Setup:** Support for both Docker and source-based installation.

## Commands

| Command    | Description                                       |
|:-----------|:--------------------------------------------------|
| `/8ball`   | Ask the magic 8ball a question.                   |
| `/encode`  | Encode text to binary.                            |
| `/decode`  | Decode binary to text.                            |
| `/fact`    | Get a random fact.                                |
| `/color`   | Get a random color with HEX, RGB, and HSL values. |
| `/element` | Get a random element from the periodic table.     |
| `/dadjoke` | Get a random dad joke.                            |
| `/meme`    | Send a random meme from Reddit.                   |
| `/pet`     | Generate a petting GIF of a user.                 |
| `/lynx`    | Send a random image of a lynx.                    |

## APIs Used

* [PopCat API](https://popcat.xyz/api)
* [TinyFox.dev API](https://tinyfox.dev/api-landing)
* [The Color API](https://www.thecolorapi.com/)
* [SingleColorImage API](https://singlecolorimage.com/)
* [icanhazdadjoke API](https://icanhazdadjoke.com/api)
* [Meme API](https://github.com/D3vd/Meme_Api)

## Setup

Create an application on the [Discord Developer Portal](https://discord.com/developers/applications), and copy the application ID and the bot token for later.

### Docker

If you prefer, you can set up the bot using Docker.

```sh
docker run -d \
  --name=orbit \
  -e BOT_TOKEN="your_bot_token_here" \
  -e USER_AGENT="Your Discord Bot (https://github.com/your_name/your_repository)" \
  -v /path/to/logs:/app/logs \
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
USER_AGENT="Your Discord Bot (https://github.com/your_name/your_repository)"
```

Then, you can run the bot using the `python main.py` command!

### Environment Variables

|  Variable  | Description                                                   |
|:----------:|---------------------------------------------------------------|
| BOT_TOKEN  | Your bot token. Do not share this with anyone!                |
| USER_AGENT | Your bot's user agent. Set this to avoid rate limits by APIs. |

## Usage

After setting up, invite your bot to a server using this premade link! It already contains the proper permissions. Replace `<app-id>` with your bot's appication ID.

```sh
https://discord.com/oauth2/authorize?client_id=<app-id>&permissions=277025508352&integration_type=0&scope=bot+applications.commands
```
