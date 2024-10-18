import os
import discord
from discord.ext import commands
import utils.global_variables as gv
from loguru import logger
from decorators.chekers import checks, only_false, is_owner, in_channel
from decorators.decor_command import write_log


class Dropdown(discord.ui.Select):
    def __init__(self, files: list):

        options = []

        for file in files:
            options.append(discord.SelectOption(label=file, emoji='📝'))

        super().__init__(placeholder='Выбирете файл для отправки', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Отправлен файл {self.values[0]}',
                                                file=discord.File(f'./logs/{self.values[0]}'))


class DropdownView(discord.ui.View):
    def __init__(self, files: list):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(files))


class OwnerCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.id_log = None

    @commands.command(description='Команда запускающая тесты для бота')
    @write_log('test')
    @logger.catch
    @checks(is_owner, in_channel(is_admin=True))
    async def test(self, ctx: commands.context.Context):
        await ctx.send('Ok')

    @commands.command()
    @write_log('ehco')
    @logger.catch
    @checks(is_owner, in_channel(is_base=True))
    async def echo(self, ctx: commands.context.Context, channel: discord.TextChannel, text):
        await channel.send(text)

    @commands.command()
    @write_log('sleep')
    @logger.catch
    @checks(is_owner, in_channel(is_base=True))
    async def sleep(self, ctx: commands.context.Context):
        await ctx.send('Доугукался, пора спать)')
        await self.bot.close()

    @commands.command()
    @write_log('debug')
    @logger.catch
    @checks(is_owner, in_channel(is_base=True))
    async def debug(self, ctx: commands.context.Context, mode: bool = False):
        if mode:
            self.id_log = logger.add('logs/d_logs_{time:YY_M_D}.log', level='DEBUG')
            await ctx.send(f'{ctx.author.mention}, режим дебага включен')
        else:
            if self.id_log is not None:
                logger.remove(self.id_log)
                self.id_log = None
                await ctx.send(f'{ctx.author.mention}, режим дебага выключен')

    @commands.command()
    @write_log('logs')
    @logger.catch
    @checks(is_owner, in_channel(is_base=True))
    async def logs(self, ctx: commands.context.Context):
        view = DropdownView(os.listdir('./logs'))
        await ctx.send('Send view', view=view)

    @commands.command()
    @write_log('sql')
    @logger.catch
    @checks(is_owner, in_channel(is_admin=True, is_command=True))
    async def sql(self, ctx: commands.context.Context, *, sql_command: str):
        if sql_command == '.tables':
            sql_command = 'select tbl_name from sqlite_master'
        status, result, column_name = gv.DataBaseClass.execute(sql_command)
        text = ''
        if status == 'ERROR':
            text = str(result)
        elif status == 'OK':
            text = '```'
            result = list(map(lambda x: list(map(str, x)), result))
            len_column = [len(column) for column in column_name]
            for row in result:
                for i, cell in enumerate(row):
                    len_column[i] = max(len_column[i], len(cell))

            text += '| ' + ' | '.join([x + ' '*(len_column[i] - len(x)) for i, x in enumerate(column_name)]) + ' |\n'
            text += '-'*(len(text)-4) + '\n'
            for row in result:
                for i, cell in enumerate(row):
                    row[i] = cell + ' '*(len_column[i] - len(cell))
                text += '| ' + ' | '.join(row) + ' |\n'
            text += '```'
        else:
            text = 'result is None'

        await ctx.message.reply(text)


async def setup(bot):
    await bot.add_cog(OwnerCommand(bot))
