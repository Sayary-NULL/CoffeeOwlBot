import discord
from loguru import logger
from discord.ext import commands
import utils.global_variables as gv
from decorators.decor_command import in_channel, is_admin as d_is_admin


class AdminCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    @d_is_admin
    @logger.catch
    async def select_channel_permissions(self, ctx: commands.context.Context):
        if (per := gv.DataBaseClass.get_channel_status(ctx.channel.id)) is not None:
            await ctx.send(per)
        else:
            await ctx.send('Не установлено')

    @commands.command()
    @d_is_admin
    @logger.catch
    async def set_permissions_channel(self, ctx: commands.context.Context,
                                      is_base: bool = False,
                                      is_command: bool = False,
                                      is_admin: bool = False,
                                      is_test: bool = False,
                                      channel_id: int = None):
        if channel_id is None:
            channel_id = ctx.channel.id
        if gv.DataBaseClass.get_channel_status(channel_id) is None:
            gv.DataBaseClass.set_channel_status(channel_id=channel_id,
                                                is_base=is_base,
                                                is_command=is_command,
                                                is_admin=is_admin,
                                                is_test=is_test)
            await ctx.send('Установлено')
        else:
            gv.DataBaseClass.update_channel_status(channel_id=channel_id,
                                                   is_base=is_base,
                                                   is_command=is_command,
                                                   is_admin=is_admin,
                                                   is_test=is_test)
            await ctx.send('Обновлено')

    @commands.command()
    @d_is_admin
    @logger.catch
    @in_channel(is_admin=True, is_command=True)
    async def select_triggers(self, ctx: commands.context.Context):
        str_out = ''
        for i, item in enumerate(gv.DataBaseClass.get_trigger_form_text()):
            str_out += f'{item[0]}) {item[1]} => {item[2]}\n'
            if i % 5 == 0 and i != 0:
                await ctx.send(str_out)
                str_out = ''
        if str_out != '':
            await ctx.send(str_out)
        await ctx.send('=====Триггеры закончились=====')

    @commands.command()
    @d_is_admin
    @logger.catch
    @in_channel(is_admin=True, is_command=True)
    async def set_trigger(self, ctx: commands.context.Context, text_request: str, text_response: str):
        text_request = text_request.lower()
        text_response = text_response.lower()
        try:
            gv.DataBaseClass.set_trigger(text_request, text_response)
            await ctx.send('Добавлено')
        except:
            await ctx.send('Произошла ошибка, обратитесь к Sayary')

    @commands.command()
    @d_is_admin
    @logger.catch
    @in_channel(is_admin=True, is_command=True)
    async def del_trigger(self, ctx: commands.context.Context, id_trigger: int):
        try:
            gv.DataBaseClass.del_trigger(id_trigger)
            await ctx.send('Удалено')
        except:
            await ctx.send('Произошла ошибка, обратитесь к Sayary')


def setup(bot):
    bot.add_cog(AdminCommand(bot))
