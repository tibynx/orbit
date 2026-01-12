"""Cog for random content commands."""
import random
import discord
from discord.ext import commands
from discord import app_commands
from utils.fetch import fetch_json


# TODO: Do pylint, and fix code


# Random commands
class Random(commands.Cog):
    """Commands for generating random content."""
    def __init__(self, bot):
        """Initialize the Random cog with a bot instance."""
        self.bot = bot



    # Get a random fact
    @app_commands.command(
        name="fact",
        description="Get a random fact."
    )
    async def random_fact(self, interaction: discord.Interaction):
        """Fetch and display a random fact from the PopCat API."""
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
        """Generate and display a random color."""
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
            embed.set_thumbnail(
                url=f"https://singlecolorimage.com/get/{data['hex']['clean']}/100x100"
            )
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


    # Get a random element
    @app_commands.command(
        name="element",
        description="Get a random element from the periodic table."
    )
    async def random_element(self, interaction: discord.Interaction):
        """Get a random element from the periodic table."""
        await interaction.response.defer()
        # Use API to get data
        data = await fetch_json(
            self.bot.session,
            "https://api.popcat.xyz/v2/periodic-table/random"
        )
        if data:
            embed = discord.Embed(
                title=data["message"]["name"],
                description=f"> {data["message"]["summary"]}",
                color=None
            )
            embed.add_field(name="Symbol", value=data["message"]["symbol"])
            embed.add_field(name="Phase", value=data["message"]["phase"])
            embed.add_field(name="Period", value=data["message"]["period"])
            embed.add_field(name="Atomic Number", value=data["message"]["atomic_number"])
            embed.add_field(name="Atomic Mass", value=data["message"]["atomic_mass"])
            embed.add_field(name="Discovered By", value=data["message"]["discovered_by"])
            embed.set_thumbnail(url=data["message"]["image"])
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                "There was an error with the API, try again later.",
                ephemeral=True
            )



async def setup(bot):
    """Set up the Random cog."""
    await bot.add_cog(Random(bot))
