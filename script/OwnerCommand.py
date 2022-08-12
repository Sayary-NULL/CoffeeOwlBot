import discord
from discord.ext import commands
import utils.global_variables as gv
from loguru import logger
from decorators.decor_command import in_channel, is_owner, add_description


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

    @add_description('команда для публикации новостей')
    @commands.group()
    @in_channel(is_admin=True)
    @logger.catch
    @is_owner
    async def news(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid git command passed...')

    @news.command()
    @logger.catch
    async def desc(self, ctx: commands.context.Context, desc: str):
        self.desc = desc

    @news.command()
    @logger.catch
    async def title(self, ctx: commands.context.Context, title: str):
        self.title = title

    @news.command()
    @logger.catch
    async def image(self, ctx: commands.context.Context, url: str):
        self.url = url

    @news.command()
    @logger.catch
    async def post(self, ctx: commands.context.Context, channel: discord.TextChannel = None):
        if self.desc is None:
            return

        if self.channel_id is None:
            channel = ctx.channel

        try:
            await channel.send(self.url)
            if self.title is not None:
                await channel.send(self.title)
            await channel.send(self.desc)
            await channel.send(self.sign)
        except Exception as e:
            await ctx.send("Ошибка отправки сообщения.")
            logger.error(e)


def setup(bot):
    bot.add_cog(OwnerCommand(bot))
