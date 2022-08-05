import discord
from discord.ext import commands
import utils.global_variables as gv
from loguru import logger
from decorators.decor_command import in_channel, is_owner


class OwnerCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.url = 'https://media.discordapp.net/attachments/462236317926031370/464447806887690240/news26052017.jpg' \
                   '?width=1193&height=671 '
        self.title = None
        self.desc = None
        self.channel_id = None
        self.sign = "Автор: <@329653972728020994>"

    @commands.command()
    @in_channel(is_admin=True)
    @logger.catch
    @is_owner
    async def test(self, ctx: commands.context.Context):
        await ctx.send('Ok')

    @commands.command()
    @in_channel(is_admin=True)
    @logger.catch
    @is_owner
    async def post_news(self, ctx: commands.context.Context):
        if self.desc is None:
            return

        if self.channel_id is not None:
            channel: discord.TextChannel = ctx.guild.get_channel(self.channel_id)
        else:
            channel = ctx.channel

        await channel.send(self.url)
        if self.title is not None:
            await channel.send(self.title)
        await channel.send(self.desc)
        await channel.send(self.sign)

    @commands.command()
    @in_channel(is_admin=True)
    @logger.catch
    @is_owner
    async def add_image(self, ctx: commands.context.Context, url: str):
        self.url = url

    @commands.command()
    @in_channel(is_admin=True)
    @logger.catch
    @is_owner
    async def add_title(self, ctx: commands.context.Context, title: str):
        self.title = title

    @commands.command()
    @in_channel(is_admin=True)
    @logger.catch
    @is_owner
    async def add_desc(self, ctx: commands.context.Context, desc: str):
        self.desc = desc

    @commands.command()
    @in_channel(is_admin=True)
    @logger.catch
    @is_owner
    async def add_sign(self, ctx: commands.context.Context, sign: str):
        self.sign = sign

    @commands.command()
    @in_channel(is_admin=True)
    @logger.catch
    @is_owner
    async def set_channel(self, ctx: commands.context.Context, channel_id: int):
        self.channel_id = channel_id


def setup(bot):
    bot.add_cog(OwnerCommand(bot))
