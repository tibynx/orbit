import logging
import os

import discord
from discord.ext import commands

# Import variables
from config import BOT_PREFIX, BOT_TOKEN


# TODO: Do pylint, and fix code
# TODO: Add more comments and docstrings
# TODO: Update README.md, Dockerfile, and poetry config
# TODO: Remove general commands like avatar, whois, etc.
# TODO: Add better error handling
# TODO: Fully move to app commands
# TODO: Add more commands and cogs
# TODO: Use buttons, components where applicable
# TODO: Update logging
# TODO: Update ignore files


# Set intents
intents = discord.Intents.default()
intents.members = True # Enable for user counting
intents.message_content = True  # Enable message content intent for prefixed commands

# Set up logging
logs_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(logs_dir, exist_ok=True)
timestamp = discord.utils.utcnow().strftime("%Y-%m-%d_%H-%M-%S") # UTC timestamp
log_filename = os.path.join(logs_dir, f"log_{timestamp}.log")

logger = logging.getLogger("discord.app")
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(filename=log_filename, encoding="utf-8", mode="w")
# Using Python's standard formatting style
log_format = "[{asctime}] [{levelname:<8}] {name}: {message}"
log_formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S", style="{")
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(BOT_PREFIX), intents=intents)
        self.logger = logger


    # Load cogs
    async def load_cogs(self) -> None:
        for file in os.listdir(os.path.join(os.path.realpath(os.path.dirname(__file__)), "cogs")):
            if file.endswith(".py"): # Only load python files
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info("Loaded extension '%s'", extension)
                except Exception as error:
                    self.logger.error(
                        "Failed to load extension '%s': %s", extension, type(error).__name__
                    )
                    self.logger.exception(error)


    async def setup_hook(self) -> None:
        self.logger.info(
            "Logged in as %s#%s (ID: %s)", self.user.name, self.user.discriminator, self.user.id
        )
        self.logger.info("discord.py version: %s", discord.__version__)
        self.logger.info("-------------------")
        await self.load_cogs()

        # Sync interactions
        try:
            synced = await self.tree.sync() # Sync all commands globally
            self.logger.info("Synced %d interactions globally", len(synced))
        except Exception as error:
            self.logger.error("Failed to sync interaction: %s", type(error).__name__)
            self.logger.exception(error)


    # Make sure the bot doesn't respond to itself
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)


    # Log guild join
    async def on_guild_join(self, guild: discord.Guild) -> None:
        self.logger.info(
            "Joined guild '%s' (ID: %s) with %d member(s), the guild owner is %s (ID: %s)",
            guild.name, guild.id, len(guild.members), guild.owner, guild.owner.id
        )

    # Log guild leave
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        self.logger.info(
            "Left guild '%s' (ID: %s) with %d member(s), the guild owner is %s (ID: %s)",
            guild.name, guild.id, len(guild.members), guild.owner, guild.owner.id
        )

    # Log command execution
    async def on_command_completion(self, ctx) -> None:
        if ctx.guild is not None:
            self.logger.info(
                "User %s (ID: %s) executed the '%s' interaction in guild '%s' (ID: %s)",
                ctx.author, ctx.author.id, ctx.command.qualified_name,
                ctx.guild.name, ctx.guild.id
            )
        else:
            self.logger.info(
                "User %s (ID: %s) executed the '%s' interaction in DMs",
                ctx.author.name, ctx.author.id, ctx.command.qualified_name
            )

    # Log command errors
    async def on_error(self, event_name: str, *args, **kwargs) -> None:
        self.logger.exception("An error occurred in %s", event_name)

    # Log command errors
    async def on_command_error(self, ctx, error) -> None:
        # Get the command name
        command_name = ctx.command.name if ctx.command else "Unknown command"

        # Command is on cooldown
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            await ctx.send(f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.")
            return None

        # User doesn't have permission to execute the command
        elif isinstance(error, (commands.MissingPermissions, commands.CheckFailure)):
            await ctx.send("You don't have permission to execute this command.")
            return None


        # Bot doesn't have permission to execute the command
        elif isinstance(error, (commands.BotMissingPermissions, discord.Forbidden)):
            await ctx.send("I don't have permission to execute this command.")
            return None

        # Missing command arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You're missing a required argument for this command.")
            return None

        # Invalid user
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("The specified user cannot be found.")
            return None

        # Command is executed in DMs but it shouldn't be
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in private messages.")
            return None

        # User is missing a required role
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You are missing the required role to execute this command.")
            return None

        # Ignore command not found errors
        elif isinstance(error, commands.CommandNotFound):
            return None

        # Network issues or rate limiting
        elif isinstance(error, discord.HTTPException):
            self.logger.warning(
                "HTTP exception occurred in interaction '%s' for user %s (ID: %s) in "
                "guild '%s' (ID: %s): %s",
                command_name, ctx.author.name, ctx.author.id,
                ctx.guild.name, ctx.guild.id, error
            )
            await ctx.send("I cannot complete this command because of network issues. I might have been rate limited. Please try again later.")
            return None

        # Command raised an unexpected error
        elif isinstance(error, commands.CommandInvokeError):
            original = getattr(error, "original", error)
            self.logger.error(
                "CommandInvokeError occurred in interaction '%s' by user %s (ID: %s) in "
                "guild '%s' (ID: %s): %r",
                command_name, ctx.author.name, ctx.author.id,
                ctx.guild.name, ctx.guild.id, original,
                exc_info=(type(original), original, original.__traceback__),
            )
            await ctx.send("An error occurred while executing the command.")
            return None


        # Other errors
        else:
            self.logger.error(
                "Unhandled app command error in interaction '%s' by user %s (ID: %s) in "
                "guild '%s' (ID: %s): %r",
                command_name, ctx.author.name, ctx.author.id,
                ctx.guild.name, ctx.guild.id, error,
                exc_info=(type(error), error, error.__traceback__),
            )
            await ctx.send("An unexpected error occurred while executing the command.")
            return None


# Run the bot
bot = DiscordBot()

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")
bot.run(BOT_TOKEN)
