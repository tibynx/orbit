import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
from utils.fetch import fetch_json, fetch_img


# TODO: Do pylint, and fix code
# TODO: Add more comments


# Image commands
class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # Send random meme
    @app_commands.command(
        name="meme",
        description="Send a random meme from reddit."
    )
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            data = await fetch_json(session, "https://meme-api.com/gimme")
            if data:
                embed = discord.Embed(
                    title=data["title"],
                    url=data["postLink"],
                    description=f"-# Posted by **@{data['author']}** on **r/{data['subreddit']}**",
                    color=None
                )
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
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            image = await fetch_img(
                session,
                f"https://api.popcat.xyz/v2/pet?image={user.display_avatar.url}"
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
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            image = await fetch_img(session, "https://api.tinyfox.dev/img?animal=lynx")
            if image:
                await interaction.followup.send(file=discord.File(image, "lynx.png"))
            else:
                await interaction.followup.send(
                    "There was an error fetching the image. Please try again later.",
                    ephemeral=True
                )



async def setup(bot):
    await bot.add_cog(Image(bot))
