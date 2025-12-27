import random
import discord
from discord.ext import commands
from discord import app_commands
from utils.fetch import fetch_json


# TODO: Do pylint, and fix code


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
        # Use API to get data
        data = await fetch_json(self.bot.session, "https://api.popcat.xyz/v2/fact")
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
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        # Use API to get data
        data = await fetch_json(
            self.bot.session,
            f"https://www.thecolorapi.com/id?rgb=rgb({red},{green},{blue})"
        )
        if data:
            embed = discord.Embed(
                title=data["name"]["value"],
                color=None
            )
            embed.add_field(name="HEX", value=data["hex"]["value"], inline=True)
            embed.add_field(name="RGB", value=f"rgb({red},{green},{blue})", inline=True)
            embed.add_field(name="HSL", value=data["hsl"]["value"], inline=True)
            # Use different URL for an image
            embed.set_thumbnail(url=f"https://singlecolorimage.com/get/{data['hex']['clean']}/100x100")
            # Create a view with a link button
            hex_clean = data["hex"]["clean"]
            view = discord.ui.View()
            view.add_item(
                discord.ui.Button(
                    label="View on ColorHexa",
                    url=f"https://www.colorhexa.com/{hex_clean}"
                )
            )
            await interaction.followup.send(embed=embed, view=view)
        else:
            await interaction.followup.send(
                "There was an error with the API, try again later.",
                ephemeral=True
            )



async def setup(bot):
    await bot.add_cog(Random(bot))
