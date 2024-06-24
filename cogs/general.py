"Import modules"
import discord
from discord.ext import commands
from discord.ext.commands import Context

from settings import PREFIX, EMBED_COLOR


class General(commands.Cog):
    """ Create cog for commands """
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive",
    )
    async def ping(self, ctx: Context) -> None:
        """ Check if the bot is alive """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=EMBED_COLOR,
        )
        await ctx.send(embed=embed)



    @commands.hybrid_command(
        name="avatar", 
        description="Show user avatar"
        )
    async def avatar_primary(self, ctx: Context, member: discord.Member) -> None:
        """ Show user avatar """
        embed = discord.Embed(
            title=f"{member.display_name}'s primary avatar",
            color=EMBED_COLOR
        )
        embed.set_image(url=member.avatar)
        embed.set_author(name=member.name, icon_url=member.avatar)
        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="banner",
        description="Show user banner"
    )
    async def banner_user(self, ctx: Context, member: discord.Member) -> None:
        """ Show user banner """
        if member.banner == None:
            embed = discord.Embed(
                title=f"{member.display_name} doesn't have a banner",
                color=EMBED_COLOR
            )
            embed.set_author(name=member.name, icon_url=member.avatar)
        else:
            embed = discord.Embed(
                title=f"{member.display_name}'s banner",
                color=EMBED_COLOR
            )
            embed.set_image(url=member.banner)
        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="botinfo",
        description="Get some info about the bot"
    )
    async def botinfo(self, ctx: Context) -> None:
        """ Get some info about the bot """
        embed = discord.Embed(title="Bot Info", color=EMBED_COLOR)
        embed.add_field(
            name="Username",
            value=f"{self.bot.user.name}#{self.bot.user.discriminator}",
            inline=True
        )
        embed.add_field(
            name="Discord.py version", value=f"{discord.__version__}",
            inline=True
        )
        embed.add_field(
            name="Ping", value=f"{round(self.bot.latency * 1000)}ms",
            inline=True
        )
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(
            name="Prefix",
            value=f"/ (Slash Commands) or {PREFIX}",
            inline=False,
        )
        embed.set_author(
            name=f"{self.bot.user.name}#{self.bot.user.discriminator}",
            icon_url=self.bot.user.avatar
        )
        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="whois",
        description="Get info about a user"
    )
    async def whois(self, ctx: Context, member: discord.Member) -> None:
        """ Get info about a user """
        creation_time = int(member.created_at.timestamp())
        join_time = int(member.joined_at.timestamp())
        roles = " ".join([role.mention for role in member.roles])
        embed = discord.Embed(
            title="User info",
            description=f"{member.mention}",
            color=EMBED_COLOR
        )
        embed.add_field(name="Display name", value=member.display_name, inline=True)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
        embed.add_field(name="Account created", value=f"<t:{creation_time}:R>", inline=True)
        embed.add_field(name="Joined", value=f"<t:{join_time}:R>", inline=True)
        embed.add_field(name=f"Roles [{len(member.roles)}]", value=roles, inline=False)
        embed.set_author(name=member.name, icon_url=member.display_avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="serverinfo",
        description="Get info about the server",
    )
    async def serverinfo(self, ctx: Context) -> None:
        """ Get info about the server """
        roles = [role.name for role in ctx.guild.roles]
        created = int(ctx.guild.created_at.timestamp())
        num_roles = len(roles)
        num_members = len([member for member in ctx.guild.members if not member.bot])
        num_bots = len([bot for bot in ctx.guild.members if bot.bot])
        num_stickers = len(ctx.guild.stickers)
        num_emojis = len(ctx.guild.emojis)
        if num_roles > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying [50/{num_roles}] Roles")
        roles = ", ".join(roles)
        embed = discord.Embed(
            title="Server info",
            description=f"**Server name**\n{ctx.guild}",
            color=EMBED_COLOR
        )
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name="Owner", value=f"{ctx.guild.owner.name}", inline=True)
        embed.add_field(
            name="Member Count",
            value=f"{num_members} Members\n{num_bots} Apps/Bots",
            inline=True
        )
        embed.add_field(name="Channels", value=len(ctx.guild.channels), inline=True)
        embed.add_field(
            name="Emotes", value=f"{num_emojis} Emojis\n{num_stickers} Stickers", inline=True)
        embed.add_field(name=f"Created", value=f"<t:{created}:R>", inline=True)
        embed.add_field(name=f"Roles [{len(ctx.guild.roles)}]", value=roles, inline=False)
        embed.set_footer(text=f"Server ID: {ctx.guild.id}")
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        await ctx.send(embed=embed)
    


async def setup(bot):
    "Add the cog to the bot"
    await bot.add_cog(General(bot))