# 🌑 Orbit

Orbit is a simple, feature-rich Discord bot designed to bring fun, utility, and entertainment to your server. It integrates various APIs to provide a wide range of commands from games to random facts and image generation.

## Features

- **Fun & Games:** 8ball, text encoding/decoding.
- **Random Content:** Facts, dad jokes, colors, and periodic table elements.
- **Images & Memes:** Random memes, user petting GIFs, and lynx photos.

## APIs Used

* [PopCat API](https://popcat.xyz/api)
* [TinyFox.dev API](https://tinyfox.dev/api-landing)
* [The Color API](https://www.thecolorapi.com/)
* [SingleColorImage API](https://singlecolorimage.com/)
* [icanhazdadjoke API](https://icanhazdadjoke.com/api)
* [Meme API](https://github.com/D3vd/Meme_Api)

## Setup

### Prerequisites

1. Create an application on the [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name.
   - Note down the Application ID for later.
   - Go to the "Bot" tab and click "Add Bot".
   - Under "TOKEN", click "Copy" to copy your bot token. (You might need to reset it to see it.)
2. Invite the bot to a Discord server
   - You can use the premade link in the usage section.

Now choose one of the following methods to run the bot!

### Docker

1. Pull the latest image from Docker Hub
   ```sh
   docker pull tibynx/orbit:latest
   ```
2. Run the container with the required environment variables and volume mounts
   - See the configuration section below for details!
   - Change `/path/to/logs` to a directory on your host where you want to store the logs.
   ```sh
   docker run -d \
      --name=orbit \
      -e BOT_TOKEN="your_bot_token_here" \
      -e USER_AGENT="Your Discord Bot (https://github.com/your_name/your_repository)" \
      -v /path/to/logs:/app/logs \
      tibynx/orbit:latest
   ```

### Source

1. Install **[Python 3.14 or newer](https://www.python.org/downloads/)**
2. Clone the repository and install all required packages!
   ```sh
   git clone https://github.com/tibynx/orbit.git
   cd orbit
   ```
   ```sh
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your settings.
   - See the configuration section below for details!
   - **Do not share your `.env` file publicly!**
4. Invite the bot to a Discord server
   - You can use the premade link in the usage section.
5. Start the bot
   ```sh
   python main.py
   ```

### Configuration

|   Variable   | Description                                                                  |
|:------------:|------------------------------------------------------------------------------|
| `BOT_TOKEN`  | Your bot token. Authenticates your bot with Discord.                         |
| `USER_AGENT` | Your bot's user agent. Used for API requests. Set this to avoid rate limits. |

## Usage

### Invite

Invite your bot to the server using this premade link! It already contains the proper permissions. Replace `YOUR_APP_ID` with your bot's application ID.

```text
https://discord.com/oauth2/authorize?client_id=YOUR_APP_ID&permissions=277025508352&integration_type=0&scope=bot+applications.commands
```

### Commands

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
