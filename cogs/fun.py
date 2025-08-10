import aiohttp
import io
import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from utils.fetch import fetch_json
from utils.fetch import fetch_img

from settings import EMBED_COLOR


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name="petpet")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def petpet(self, ctx: Context, member: discord.Member) -> None:
        """
        Generate a petting GIF of a member

        Parameters
        ------------
        ctx: Context
            Command context

        member: discord.Member
            The member you want to pet
        """
        async with aiohttp.ClientSession() as session:
            image = await fetch_img(session, f"https://api.popcat.xyz/v2/pet?image={member.display_avatar}")
            if image:
                await ctx.send(file=discord.File(image, "pet.gif"))
            else:
                await ctx.send("There was an error with the API, try again later.")


    @commands.hybrid_command(name="randomfact")
    async def random_fact(self, ctx: Context) -> None:
        """
        Get a random fact

        Parameters
        ------------
        ctx: Context
            Command context
        """
        async with aiohttp.ClientSession() as session:
            data = await fetch_json(session, "https://api.popcat.xyz/v2/fact")
            if data:
                text = data["message"]["fact"]
                await ctx.send(text.replace("`", "'"))
            else:
                await ctx.send("There was an error with the API, try again later.")


    @commands.hybrid_command(name="meme")
    async def meme(self, ctx: Context) -> None:
        """
        Send a random meme from reddit

        Parameters
        ------------
        ctx: Context
            Command context
        """
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            data = await fetch_json(session, "https://meme-api.com/gimme")
            if data:
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


    @commands.hybrid_command(name="8ball")
    async def eight_ball(self, ctx: Context, *, question: str) -> None:
        """
        Ask any question to the bot

        Parameters
        ------------
        ctx: Context
            Command context

        question: str
            The question you want to ask the bot
        """
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


    @commands.hybrid_command(name="randomelement")
    async def random_element(self, ctx: Context) -> None:
        """
        Get a random element from the periodic table

        Parameters
        ------------
        ctx: Context
            Command context
        """
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            data = await fetch_json(session, "https://api.popcat.xyz/v2/periodic-table/random")
            if data:
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


    @commands.hybrid_command(name="randomcolor")
    async def random_color(self, ctx: Context):
        """
        Get a random color

        Parameters
        ------------
        ctx: Context
            Command context
        """
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            data = await fetch_json(session, "https://api.popcat.xyz/v2/randomcolor")
            if data:
                hex_code = data['message']['hex']
                def rgb(hex_str): # convert to rgb
                    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
                embed = discord.Embed(title=data['message']['name'], color=EMBED_COLOR)
                embed.add_field(name="HEX", value=f"#{hex_code}")
                embed.add_field(name="RGB", value=f"rgb{rgb(hex_code)}")
                embed.set_thumbnail(url=data['message']['image'])
                await ctx.send(embed=embed)
            else:
                await ctx.send("There was an error with the API, please try again later.")


    @commands.hybrid_command(name="fox")
    async def fox(self, ctx: Context) -> None:
        """
        Send some cute fox pictures

        Parameters
        ------------
        ctx: Context
            Command context
        """
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            image = await fetch_img(session, "https://api.tinyfox.dev/img?animal=fox")
            if image:
                await ctx.send(file=discord.File(image, "fox.png"))
            else:
                await ctx.send("There was an error with the API, try again later.")



async def setup(bot):
    await bot.add_cog(Fun(bot))