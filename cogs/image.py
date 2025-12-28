"""Cog for image-related commands."""
import urllib.parse
import discord
from discord.ext import commands
from discord import app_commands
from utils.fetch import fetch_json, fetch_img


# TODO: Do pylint, and fix code


# Image commands
class Image(commands.Cog):
    """Commands for fetching and displaying images."""
    def __init__(self, bot):
        """Initialize the Image cog."""
        self.bot = bot



    # Send random meme
    @app_commands.command(
        name="meme",
        description="Send a random meme from reddit."
    )
    async def meme(self, interaction: discord.Interaction):
        """Send a random meme from Reddit using the meme API."""
        await interaction.response.defer()
        # Fetch meme data
        data = await fetch_json(self.bot.session, "https://meme-api.com/gimme")
        if data:
            embed = discord.Embed(
                title=data["title"],
                url=data["postLink"],
                description=f"-# Posted by **@{data['author']}** on **r/{data['subreddit']}**",
                color=None
            )
            # Set meme image
            embed.set_image(url=data["url"])
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                "There was an error fetching a meme. Please try again later.",
                ephemeral=True
            )


    # Generate pet gif
    @app_commands.command(
        name="pet",
        description="Generate a petting GIF of a user."
    )
    @app_commands.describe(user="The user you want to pet.")
    async def pet(self, interaction: discord.Interaction, user: discord.User):
        """Generate a petting GIF animation for a specified user."""
        await interaction.response.defer()
        # Fetch petting GIF
        encoded_avatar = urllib.parse.quote(user.display_avatar.url, safe="")
        image = await fetch_img(
            self.bot.session,
            f"https://api.popcat.xyz/v2/pet?image={encoded_avatar}"
        )
        if image:
            await interaction.followup.send(file=discord.File(image, "pet.gif"))
        else:
            await interaction.followup.send(
                "There was an error fetching the image. Please try again later.",
                ephemeral=True
            )


    # Send random images of lynxes
    @app_commands.command(
        name="lynx",
        description="Send a random image of a lynx."
    )
    async def lynx(self, interaction: discord.Interaction):
        """Send a random image of a lynx from the TinyFox API."""
        await interaction.response.defer()
        # Fetch lynx image
        image = await fetch_img(self.bot.session, "https://api.tinyfox.dev/img?animal=lynx")
        if image:
            await interaction.followup.send(file=discord.File(image, "lynx.png"))
        else:
            await interaction.followup.send(
                "There was an error fetching the image. Please try again later.",
                ephemeral=True
            )



async def setup(bot):
    """Set up the Image cog."""
    await bot.add_cog(Image(bot))
