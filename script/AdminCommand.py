import discord
from loguru import logger
from discord.ext import commands
import utils.global_variables as gv
from decorators.decor_command import in_channel, is_admin as d_is_admin
from utils.class_for_help_command import InitialClass


class AdminCommand(commands.Cog, InitialClass):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.set_help_str(AdminCommand)

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


def setup(bot):
    bot.add_cog(AdminCommand(bot))
