import aiohttp
import random
import discord
from discord.ext import commands
from discord import app_commands
from utils.fetch import fetch_json


# TODO: Do pylint, and fix code
# TODO: Add more comments


# Random commands
class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # Get a random fact
    @app_commands.command(
        name="fact",
        description="Get a random fact."
    )
    async def random_fact(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            data = await fetch_json(session, "https://api.popcat.xyz/v2/fact")
            if data:
                text = data["message"]["fact"]
                await interaction.followup.send(text.replace("`", "'"))
            else:
                await interaction.followup.send(
                    "There was an error with the API, try again later.",
                    ephemeral=True
                )


    # Get a random color
    @app_commands.command(
        name="color",
        description="Get a random color."
    )
    async def random_color(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # Generate random RGB values
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        # Use API to get data
        async with aiohttp.ClientSession() as session:
            data = await fetch_json(
                session,
                f"https://www.thecolorapi.com/id?rgb=rgb({r},{g},{b})"
            )
            if data:
                embed = discord.Embed(
                    title=data["name"]["value"],
                    color=None
                )
                embed.add_field(name="HEX", value=data["hex"]["value"], inline=True)
                embed.add_field(name="RGB", value=f"rgb({r},{g},{b})", inline=True)
                embed.add_field(name="HSL", value=data["hsl"]["value"], inline=True)
                # Use different URL for an image
                embed.set_thumbnail(url=f"https://singlecolorimage.com/get/{data['hex']['clean']}/100x100")
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    "There was an error with the API, try again later.",
                    ephemeral=True
                )



async def setup(bot):
    await bot.add_cog(Random(bot))
