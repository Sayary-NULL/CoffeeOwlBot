import json
import discord
from script import AdminCommand, OwnerCommand
from loguru import logger
from discord.ext import commands
from decorators.decor_command import in_channel
from utils.class_for_help_command import InitialClass
from utils.utils_methods import user_is_admin, user_is_owner


class UserCommand(commands.Cog, InitialClass):

    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.set_help_str(UserCommand)

    @commands.command()
    @logger.catch
    @in_channel(is_base=True)
    async def hello(self, ctx: commands.context.Context):
        await ctx.send(f'{ctx.author.mention}, hello!')

    @commands.command()
    @logger.catch
    @in_channel(is_command=True)
    async def ver(self, ctx: commands.context.Context):
        with open('version.json', 'r') as f:
            js = json.load(f)
        await ctx.send(f'версия: {js["ver"]}')

    @commands.command()
    @logger.catch
    @in_channel(is_command=True)
    async def help(self, ctx: commands.context.Context, func_name: str = None):
        if func_name is None:
            embed = discord.Embed(description='**Команды бота**', color=discord.colour.Colour.red())
            embed.add_field(name='**Параметры**', value='[] - обязательные\n<> - не обязательные', inline=False)
            embed.add_field(name='Group: User', value=UserCommand.help_str, inline=True)
            if user_is_admin(ctx.author):
                embed.add_field(name='Group: Admin', value=AdminCommand.AdminCommand.help_str, inline=True)
            if user_is_owner(ctx.author):
                embed.add_field(name='Group: Owner', value=OwnerCommand.OwnerCommand.help_str, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('HEEELP')


def setup(bot):
    bot.add_cog(UserCommand(bot))
