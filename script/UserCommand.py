import json
import discord
from script import AdminCommand, OwnerCommand
from loguru import logger
from discord.ext import commands
from decorators.decor_command import in_channel
from utils.utils_methods import user_is_admin, user_is_owner, get_help_from_class


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
    @in_channel(is_command=True)
    async def ver(self, ctx: commands.context.Context):
        with open('version.json', 'r') as f:
            js = json.load(f)
        await ctx.send(f'версия: {js["ver"]}')

    @add_description('`>help` для большей подробности')
    @commands.command()
    @logger.catch
    @in_channel(is_command=True)
    async def help(self, ctx: commands.context.Context, func_name: str = None):
        if func_name is None:
            embed = discord.Embed(description='**Команды бота**', color=discord.colour.Colour.red())
            embed.add_field(name='**Параметры**', value='[] - обязательные\n<> - не обязательные', inline=False)

            embed.add_field(name='Group: User', value=get_help_from_class(UserCommand), inline=True)

            if user_is_admin(ctx.author):
                embed.add_field(name='Group: Admin', value=get_help_from_class(AdminCommand.AdminCommand), inline=True)

            if user_is_owner(ctx.author) and (rez := get_help_from_class(OwnerCommand.OwnerCommand)) != '':
                embed.add_field(name='Group: Owner', value=rez, inline=True)
                logger.debug(f'owner {rez}')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'**Справка по команде {func_name}**', color=discord.colour.Colour.blue())
            class_name = 'User'

            if (func := get_funcs_on_name_or_aliases(func_name, UserCommand)) is None:
                class_name = 'Admin'
                if (func := get_funcs_on_name_or_aliases(func_name, AdminCommand.AdminCommand)) is None:
                    class_name = 'Owner'
                    func = get_funcs_on_name_or_aliases(func_name, AdminCommand.AdminCommand)

            if func is None:
                embed.add_field(
                    name='**Описание**',
                    value='Команда не найдена',
                    inline=False
                )
                await ctx.send(embed=embed)
                return

            embed.add_field(
                name='**Оригинальное имя**',
                value=func.name,
                inline=False
            )

            embed.add_field(
                name='**Класс доступа**',
                value=class_name,
                inline=False
            )
            description = None
            if 'description' in dir(func):
                if func.description is not None:
                    if func.description.strip() != '':
                        description = func.description

            if description is None:
                description = 'Не установлено'

            embed.add_field(
                name='**Описание**',
                value=description,
                inline=False
            )

            if len(func.aliases) != 0:
                aliases = ''
                for i, alias in enumerate(func.aliases):
                    aliases += f'{i + 1}) {alias}\n'
                embed.add_field(
                    name='**Псевдонимы**',
                    value=aliases,
                    inline=False
                )

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UserCommand(bot))
