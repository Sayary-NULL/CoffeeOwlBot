import json
import discord
from loguru import logger
from discord.ext import commands
from decorators.decor_command import in_channel


class UserCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    @logger.catch
    @in_channel(is_base=True)
    async def hello(self, ctx: commands.context.Context):
        await ctx.send(f'{ctx.author.mention}, hello!')

    @commands.command()
    @logger.catch
    @in_channel(is_base=True)
    async def help(self, ctx: commands.context.Context):
        await ctx.send(f'{ctx.author.mention}, у меня обед!')

    @commands.command()
    @logger.catch
    @in_channel(is_command=True)
    async def ver(self, ctx: commands.context.Context):
        with open('version.json', 'r') as f:
            js = json.load(f)
        await ctx.send(f'версия: {js["ver"]}')


def setup(bot):
    bot.add_cog(UserCommand(bot))
