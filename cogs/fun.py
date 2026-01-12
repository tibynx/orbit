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



async def setup(bot):
    """Set up the Fun cog."""
    await bot.add_cog(Fun(bot))
