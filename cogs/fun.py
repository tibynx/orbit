"""Cog for fun commands."""
import random
import discord
from discord.ext import commands
from discord import app_commands


# Fun commands
class Fun(commands.Cog):
    """Commands for fun and interesting things."""
    def __init__(self, bot):
        """Initialize the Fun cog with a bot instance."""
        self.bot = bot

    # 8ball command
    @app_commands.command(
        name="8ball",
        description="Ask the magic 8ball a question."
    )
    @app_commands.describe(question="The question you want the 8ball to answer.")
    async def ball(self, interaction: discord.Interaction, question: str):
        """Ask the magic 8ball a question."""
        answer = random.choice([
            "It is certain.",
            "It is decidedly so.",
            "You may rely on it.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again later.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
            "Probably, yes.",
            "Probably, not."
        ])
        embed = discord.Embed(
            title="🎱 8ball",
            description=f"> {question}\n\n{answer}",
            color=None
        )
        await interaction.response.send_message(embed=embed)

    # Encode text to binary
    @app_commands.command(
        name="encode",
        description="Encode text to binary."
    )
    @app_commands.describe(text="The text to encode.")
    async def binary(self, interaction: discord.Interaction, text: str):
        """Encode text to binary."""
        binary = bin(int.from_bytes(text.encode(), "big"))[2:]
        embed = discord.Embed(
            title="📝 Text to Binary",
            description=f"> {text}\n\n{binary}",
            color=None
        )
        await interaction.response.send_message(embed=embed)

    # Decode binary to text
    @app_commands.command(
        name="decode",
        description="Decode binary to text."
    )
    @app_commands.describe(binary="The binary to decode.")
    async def decode(self, interaction: discord.Interaction, binary: str):
        """Decode binary to text."""
        try:
            # Convert binary string to integer, then to bytes
            n = int(binary, 2)
            text = n.to_bytes((n.bit_length() + 7) // 8, "big").decode()

            embed = discord.Embed(
                title="📝 Binary to Text",
                description=f"> {binary}\n\n{text}",
                color=None
            )
            await interaction.response.send_message(embed=embed)
        except Exception:
            await interaction.response.send_message("Invalid binary input.", ephemeral=True)


async def setup(bot):
    """Set up the Fun cog."""
    await bot.add_cog(Fun(bot))
