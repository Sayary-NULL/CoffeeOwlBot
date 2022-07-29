import discord
from discord.ext import commands
import utils.global_variables as gv
from loguru import logger
from decorators.decor_command import in_channel, is_owner


class OwnerCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    @in_channel(is_test=True)
    @logger.catch
    @is_owner
    async def test(self, ctx: commands.context.Context, mess: str):
        message: discord.Message = ctx.message
        for item in gv.DataBaseClass.get_trigger_form_text(mess.lower()):
            await ctx.send(item)


def setup(bot):
    bot.add_cog(OwnerCommand(bot))
