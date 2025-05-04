""" Import modules """
import aiohttp
import io
import random
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from settings import EMBED_COLOR


class Fun(commands.Cog):
    """ Create cog for commands """
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name="petpet",
        description="Generate a petpet gif"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def petpet(self, ctx: Context, member: discord.Member) -> None:
        """ Generate a petpet gif """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.popcat.xyz/v2/pet?image={member.display_avatar}"
            ) as request:
                if request.status == 200:
                    image = io.BytesIO(await request.read())
                    await ctx.send(file=discord.File(image, "pet.gif"))
                else:
                    await ctx.send("There was an error with the API, try again later.")


    @commands.hybrid_command(
        name="randomfact",
        description="Get a random fact"
    )
    async def randomfact(self, ctx: Context) -> None:
        """ Tell a random fact """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    text = data["text"]
                    await ctx.send(text.replace("`", "'"))
                else:
                    await ctx.send("There was an error with the API, try again later.")


    @commands.hybrid_command(
        name="meme",
        description="Send a random meme from reddit"
    )
    async def meme(self, ctx: Context) -> None:
        """ Send a random meme """
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://meme-api.com/gimme"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        title=data['title'],
                        url=data['postLink'],
                        color=EMBED_COLOR
                        )
                    embed.set_image(url=data['url'])
                    embed.set_footer(text=f"Posted by @{data['author']} on r/{data['subreddit']}")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("There was an error with the API, try again later.")


    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot",
    )
    @app_commands.describe(question="The question you want to ask")
    async def eight_ball(self, ctx: Context, *, question: str) -> None:
        """ Ask any question to the bot """
        answers = [
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
        ]
        embed = discord.Embed(
            description=f"🎱 **{random.choice(answers)}**",
            color=EMBED_COLOR,
        )
        embed.set_footer(text=f"The question was: {question}")
        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="randomelement",
        description="Get a random element from the periodic table"
    )
    async def randomelement(self, ctx: Context) -> None:
        """ Get a random element from the periodic table"""
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.popcat.xyz/v2/periodic-table/random"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        title=data['message']['name'], description=data['message']['summary'], color=EMBED_COLOR
                    )
                    embed.add_field(name="Symbol", value=data['message']['symbol'])
                    embed.add_field(name="Phase", value=data['message']['phase'])
                    embed.add_field(name="Period", value=data['message']['period'])
                    embed.add_field(name="Atomic Number", value=data['message']['atomic_number'])
                    embed.add_field(name="Atomic Mass", value=data['message']['atomic_mass'])
                    embed.add_field(name="Discovered By", value=data['message']['discovered_by'])
                    embed.set_thumbnail(url=data['message']['image'])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("There was an error with the API, please try again later.")


    @commands.hybrid_command(
        name="randomcolor",
        description="Get a random color"
    )
    async def randomcolor(self, ctx: Context):
        """ Get a random color """
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.popcat.xyz/v2/randomcolor"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    hex = data['message']['hex']
                    def rgb(hex): # convert to rgb
                        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
                    embed = discord.Embed(title=data['message']['name'], color=EMBED_COLOR)
                    embed.add_field(name="HEX", value=f"#{hex}")
                    embed.add_field(name="RGB", value=f"rgb{rgb(hex)}")
                    embed.set_thumbnail(url=data['message']['image'])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("There was an error with the API, please try again later.")


    @commands.hybrid_command(
        name="fox",
        description="Get some cute fox pictures"
    )
    async def fox(self, ctx: Context) -> None:
        """ Get some cute fox pictures """
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.tinyfox.dev/img?animal=fox"
            ) as request:
                if request.status == 200:
                    image = io.BytesIO(await request.read())
                    await ctx.send(file=discord.File(image, "fox.png"))
                else:
                    await ctx.send("There was an error with the API, try again later.")



async def setup(bot):
    """ Add the cog to the bot """
    await bot.add_cog(Fun(bot))