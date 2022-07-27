import discord
from discord.ext import commands
import utils.global_variables as gv
from decorators.decor_command import in_channel, is_admin


class AdminCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    @is_admin
    @in_channel(is_base=True, is_command=True, is_admin=True, is_test=True)
    async def select_channel_permissions(self, ctx: commands.context.Context):
        if (per := gv.DataBaseClass.get_channel_status(ctx.channel.id)) is not None:
            await ctx.send(per)
        else:
            await ctx.send('Не установлено')

    @commands.command()
    @is_admin
    @in_channel(is_test=True)
    async def set_permissions_channel(self, ctx: commands.context.Context,
                                      is_base: bool = False,
                                      is_command: bool = False,
                                      is_admin: bool = False,
                                      is_test: bool = False):
        if gv.DataBaseClass.get_channel_status(ctx.channel.id) is None:
            gv.DataBaseClass.set_channel_status(channel_id=ctx.channel.id,
                                                is_base=is_base,
                                                is_command=is_command,
                                                is_admin=is_admin,
                                                is_test=is_test)
            await ctx.send('Установлено')
        else:
            gv.DataBaseClass.update_channel_status(channel_id=ctx.channel.id,
                                                   is_base=is_base,
                                                   is_command=is_command,
                                                   is_admin=is_admin,
                                                   is_test=is_test)
            await ctx.send('Обновлено')


def setup(bot):
    bot.add_cog(AdminCommand(bot))
