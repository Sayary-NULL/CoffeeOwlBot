import json
import discord
import random
from script import AdminCommand, OwnerCommand
from loguru import logger
from discord.ext import commands
from decorators.decor_command import in_channel, add_description
from utils.utils_methods import user_is_admin, user_is_owner, get_help_from_class, get_funcs_on_name_or_aliases, \
    get_all_group, get_param_on_func
from utils.global_variables import UserColor, OwnerID


class UserCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @add_description('Привет 0/')
    @commands.command(aliases=['привет'])
    @logger.catch
    @in_channel(is_base=True)
    async def hello(self, ctx: commands.context.Context):
        await ctx.send(f'{ctx.author.mention}, hello!')

    @add_description('Случайно выбирает элемент, разделитель = ","')
    @commands.command(aliases=['случай', 'random'])
    @logger.catch
    @in_channel(is_base=True, is_command=True)
    async def roll(self, ctx: commands.context.Context, *roll_text: str):
        if len(roll_text) == 1:
            roll_arr = roll_text[0].split(',')
        else:
            roll_arr = []
            for roll in roll_text:
                for item in roll.strip(',').split(','):
                    roll_arr.append(item)

        embed = discord.Embed(color=UserColor)
        random_id = random.randint(0, len(roll_arr)-1)
        result_text = ''

        for i, text in enumerate(roll_arr):
            if i == random_id:
                result_text += f'**{i+1}) {text}**\n'
            else:
                result_text += f'{i+1}) {text}\n'

        embed.add_field(
            name='Результаты',
            value=result_text,
            inline=False
        )
        await ctx.send(embed=embed)

    @add_description('Шуточная команда "бан"')
    @commands.command(aliases=['бан'])
    @logger.catch
    @in_channel(is_base=True, is_command=True)
    async def ban(self, ctx: discord.ext.commands.context.Context, user: discord.Member, text: str = None):
        if user.bot:
            return

        url_image = 'https://media.discordapp.net/attachments/462236317926031370/464149984619528193/tumblr_oda2o7m3NR1tydz8to1_500.gif'

        if user.id == OwnerID:
            await ctx.send(f"{ctx.author.mention}, я не пойду против своего создателя!")
            user = ctx.author
            text = "Не уважение к моему создателю!"
            url_image = 'https://media.discordapp.net/attachments/462236317926031370/1003226679403102248/1579887266_2020-01-24_19-57-45.gif'

        emd = discord.Embed(color=UserColor)
        emd.add_field(name='**Бан**', value=f'Пользователь: {user.mention} - забанен', inline=False)
        emd.add_field(name='**Причина**', value=f'{text if text is not None else "Не указанно"}', inline=False)
        emd.set_image(url=url_image)
        emd.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=emd)

    @add_description('Шуточная команда "warn"')
    @commands.command()
    @logger.catch
    @in_channel(is_base=True, is_command=True)
    async def warn(self, ctx: discord.ext.commands.context.Context, user: discord.Member):
        if user.bot:
            return

        emd = discord.Embed(color=UserColor)
        emd.add_field(name='**Предупреждение**', value=f'Пользователю: {user.mention} - вынесено предупреждение', inline=False)
        emd.set_image(url='https://media.discordapp.net/attachments/462236317926031370/1003229964843356190/--.jpg?width=975&height=671')
        emd.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=emd)

    @add_description('Показывает текущую версию бота')
    @commands.command(aliases=['версия'])
    @logger.catch
    @in_channel(is_command=True)
    async def ver(self, ctx: commands.context.Context):
        with open('version.json', 'r') as f:
            js = json.load(f)
        await ctx.send(f'версия: {js["ver"]}')

    @add_description('>help для большей подробности')
    @commands.command()
    @logger.catch
    @in_channel(is_command=True)
    async def help(self, ctx: commands.context.Context, func_name: str = None):
        if func_name is None:
            embed = discord.Embed(description='**Команды бота**', color=UserColor)
            embed.add_field(name='Group: User', value=get_help_from_class(UserCommand), inline=False)

            if user_is_admin(ctx.author):
                embed.add_field(name='Group: Admin', value=get_help_from_class(AdminCommand.AdminCommand), inline=False)

            if user_is_owner(ctx.author) and (rez := get_help_from_class(OwnerCommand.OwnerCommand)) != '':
                embed.add_field(name='Group: Owner', value=rez, inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'**Справка по команде {func_name}**', color=UserColor)
            class_name = 'User'

            if (func := get_funcs_on_name_or_aliases(func_name, UserCommand)) is None:
                class_name = 'Admin'
                if (func := get_funcs_on_name_or_aliases(func_name, AdminCommand.AdminCommand)) is None:
                    class_name = 'Owner'
                    func = get_funcs_on_name_or_aliases(func_name, OwnerCommand.OwnerCommand)

            if func is None:
                embed.add_field(
                    name='**Описание**',
                    value='Команда не найдена',
                    inline=False
                )
                await ctx.send(embed=embed)
                return

            if (group := get_all_group(func_name, UserCommand)) is None:
                if (group := get_all_group(func_name, AdminCommand.AdminCommand)) is None:
                    group = get_all_group(func_name, OwnerCommand.OwnerCommand)

            embed.add_field(
                name='**Оригинальное имя**',
                value='```' + func.name + '```',
                inline=False
            )

            embed.add_field(
                name='**Класс доступа**',
                value='```' + class_name + '```',
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
                value='```' + description + '```',
                inline=False
            )

            if group is not None:
                group_lst = '```'
                for i, item in enumerate(group):
                    group_lst += f'{i + 1}) {item}\n'
                group_lst += '```'

                embed.add_field(
                    name='**Элементы группы**',
                    value=group_lst,
                    inline=False
                )

            if group is None:
                embed.add_field(
                    name='**Параметры функции**',
                    value='[] - обязательные\n<> - не обязательные\n' + get_param_on_func(func),
                    inline=False
                )

            if len(func.aliases) != 0:
                aliases = '```'
                for i, alias in enumerate(func.aliases):
                    aliases += f'{i + 1}) {alias}\n'
                aliases = aliases[:-1] + '```'
                embed.add_field(
                    name='**Псевдонимы**',
                    value=aliases,
                    inline=False
                )

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UserCommand(bot))
