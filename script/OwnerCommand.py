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
    async def debug(self, ctx: commands.context.Context, mode:bool = False):
        if mode:
            self.id_log = logger.add('logs/d_logs_{time:YY_M_D}.log', format=gv.FormatLog, level='DEBUG',
                                     rotation='1 MB', compression='zip')
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


async def setup(bot):
    await bot.add_cog(OwnerCommand(bot))
