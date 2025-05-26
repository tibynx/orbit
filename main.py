import logging
import os

import discord
from discord.ext import commands

# Import variables
from settings import PREFIX, TOKEN

# TODO: Remove unnecessary docstrings
# TODO: Add descriptions to slash command options

# Set intents
intents = discord.Intents.default()
intents.members = True # Enable for user counting
intents.message_content = True  # Enable message content intent for prefixed commands

# Setup both of the loggers
class LoggingFormatter(logging.Formatter):
    """ Configure appearance of logs """
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"

    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        log_format = "(black)[{asctime}](reset) (levelcolor)[{levelname:<8}](reset) (green){name}:(reset) {message}"
        log_format = log_format.replace("(black)", self.black + self.bold)
        log_format = log_format.replace("(reset)", self.reset)
        log_format = log_format.replace("(levelcolor)", log_color)
        log_format = log_format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_log_format = "[{asctime}] [{levelname:<8}] {name}: {message}"
file_handler_formatter = logging.Formatter(file_handler_log_format, "%Y-%m-%d %H:%M:%S", style="{")
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class DiscordBot(commands.Bot):
    """ Create discord bot """
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(PREFIX), intents=intents)
        self.logger = logger


    # Load cogs
    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(f"Failed to load extension '{extension}'\n{exception}")


    async def setup_hook(self) -> None:
        self.logger.info(f"Logged in as {self.user.name}#{self.user.discriminator} (ID: {self.user.id})")
        self.logger.info(f"discord.py version: {discord.__version__}")
        self.logger.info("-------------------")
        await self.load_cogs()

        # Sync interactions
        try:
            synced = await bot.tree.sync()
            self.logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            self.logger.error(f"Failed to sync commands\n{exception}")


    # Make sure the bot doesn't respond to itself
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)


    # Log command execution
    async def on_command_completion(self, ctx) -> None:
        full_command_name = ctx.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if ctx.guild is not None:
            self.logger.info(f"User {ctx.author} (ID: {ctx.author.id}) executed '{executed_command}' command in the guild '{ctx.guild.name}' (ID: {ctx.guild.id})")
        else:
            self.logger.info(f"User {ctx.author} (ID: {ctx.author.id}) executed '{executed_command}' command")


    # Log command errors
    async def on_command_error(self, ctx, error) -> None:
        # Get the command name
        command_name = ctx.command.name if ctx.command else "Unknown command"

        # Create embed
        embed = discord.Embed(
            title="Error",
            color=0xE02B2B
        )

        # command is on cooldown
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed.description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}."
            return await ctx.send(embed=embed)

        # bot owner only command
        elif isinstance(error, commands.NotOwner):
            embed.description="You are not the owner of the bot!"
            await ctx.send(embed=embed)

            if ctx.guild:
                self.logger.warning(f"User {ctx.author} (ID: {ctx.author.id}) tried to execute an owner only command in the guild '{ctx.guild.name}' (ID: {ctx.guild.id})")
                return None
            else:
                self.logger.warning(f"User {ctx.author} (ID: {ctx.author.id}) tried to execute an owner only command")
                return None

        # user doesn't have enough permissions
        elif isinstance(error, commands.MissingPermissions):
            embed.description="You are missing permission(s) to execute this command:\n`" + ", ".join(error.missing_permissions) + "`"
            return await ctx.send(embed=embed)

        # bot doesn't have enough permissions
        elif isinstance(error, commands.BotMissingPermissions):
            embed.description="I am missing the permission(s) to execute this command:\n`" + ", ".join(error.missing_permissions) + "`"
            return await ctx.send(embed=embed)

        # missing command arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            # We need to capitalize because the command arguments have no capital letter in the code, and they're the first word in the error message.
            embed.description="You're missing a required argument for this command:\n" + f"`{str(error).capitalize()}`"
            return await ctx.send(embed=embed)

        # bot lacks permissions (discord.errors.Forbidden)
        elif isinstance(error, discord.errors.Forbidden):
            embed.description="I do not have the required permissions to execute this command!",
            return await ctx.send(embed=embed)

        # handle other errors
        else:
            embed.description="An unhandled exception occurred while executing the command:\n" + f"`{str(error)}`"
            self.logger.error(f"Unhandled exception in command '{command_name}': {str(error)}")
            return await ctx.send(embed=embed)


# Run the bot
bot = DiscordBot()
bot.run(TOKEN)