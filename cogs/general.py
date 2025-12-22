import discord
from discord.ext import commands
from discord.ext.commands import Context

from config import BOT_PREFIX, EMBED_COLOR


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: Context) -> None:
        """
        Check bot latency

        Parameters
        ------------
        ctx: Context
            Command context
        """
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {latency}ms.",
            color=EMBED_COLOR,
        )
        await ctx.send(embed=embed)



    @commands.hybrid_command(name="avatar")
    async def avatar_primary(self, ctx: Context, member: discord.Member) -> None:
        """
        Shows the selected member's avatar

        Parameters
        ------------
        ctx: Context
            Command context

        member: discord.Member
            The member you want to see the avatar of
        """
        embed = discord.Embed(
            title=f"{member.display_name}'s avatar",
            color=EMBED_COLOR
        )
        embed.set_image(url=member.avatar)
        embed.set_author(name=member.name, icon_url=member.avatar)
        await ctx.send(embed=embed)


    @commands.hybrid_command(name="banner")
    async def banner_primary(self, ctx: Context, member: discord.Member) -> None:
        """
        Shows the selected member's banner

        Parameters
        ------------
        ctx: Context
            Command context

        member: discord.Member
            The member you want to see the banner of
        """
        if member.banner is None:
            await ctx.send(f"{member.mention} doesn't have a banner.", allowed_mentions=discord.AllowedMentions.none())
        else:
            embed = discord.Embed(
                title=f"{member.display_name}'s banner",
                color=EMBED_COLOR
            )
            embed.set_image(url=member.banner)
            await ctx.send(embed=embed)


    @commands.hybrid_command(name="serveravatar")
    async def avatar_server(self, ctx: Context, member: discord.Member) -> None:
        """
        Shows the selected member's server avatar

        Parameters
        ------------
        ctx: Context
            Command context

        member: discord.Member
            The member you want to see the server avatar of
        """
        if member.guild_avatar is None:
            await ctx.send(f"{member.mention} doesn't have a server avatar.", allowed_mentions=discord.AllowedMentions.none())
        else:
            embed = discord.Embed(
                title=f"{member.display_name}'s server avatar",
                color=EMBED_COLOR
            )
            embed.set_image(url=member.guild_avatar)
            await ctx.send(embed=embed)


    @commands.hybrid_command(name="serverbanner")
    async def banner_server(self, ctx: Context, member: discord.Member) -> None:
        """
        Shows the selected member's server banner

        Parameters
        ------------
        ctx: Context
            Command context

        member: discord.Member
            The member you want to see the server banner of
        """
        if member.guild_banner is None:
            await ctx.send(f"{member.mention} doesn't have a server banner.", allowed_mentions=discord.AllowedMentions.none())
        else:
            embed = discord.Embed(
                title=f"{member.display_name}'s server banner",
                color=EMBED_COLOR
            )
            embed.set_image(url=member.guild_banner)
            await ctx.send(embed=embed)


    @commands.hybrid_command(name="botinfo")
    async def info_bot(self, ctx: Context) -> None:
        """
        Get info about the bot

        Parameters
        ------------
        ctx: Context
            Command context
        """
        embed = discord.Embed(title="Bot Info", color=EMBED_COLOR)
        embed.add_field(
            name="Username",
            value=f"{self.bot.user.name}#{self.bot.user.discriminator}",
            inline=True
        )
        embed.add_field(
            name="Discord.py Version", value=f"{discord.__version__}",
            inline=True
        )
        embed.add_field(
            name="Ping", value=f"{round(self.bot.latency * 1000)}ms",
            inline=True
        )
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(
            name="Prefix",
            value=f"{PREFIX}",
            inline=False,
        )
        embed.set_author(
            name=f"{self.bot.user.name}#{self.bot.user.discriminator}",
            icon_url=self.bot.user.avatar
        )
        await ctx.send(embed=embed)


    @commands.hybrid_command(name="whois")
    async def info_member(self, ctx: Context, member: discord.Member) -> None:
        """
        Get info about a member

        Parameters
        ------------
        ctx: Context
            Command context

        member: discord.Member
            The member you want to see the info of
        """
        creation_time = int(member.created_at.timestamp())
        join_time = int(member.joined_at.timestamp())
        roles = " ".join([role.mention for role in member.roles])
        embed = discord.Embed(
            title="Member info",
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


    @commands.hybrid_command(name="serverinfo")
    @commands.guild_only()
    async def info_server(self, ctx: Context) -> None:
        """
        Get info about this server

        Parameters
        ------------
        ctx: Context
            Command context
        """
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
    await bot.add_cog(General(bot))