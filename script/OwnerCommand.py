import discord
from discord.ext import commands
import utils.global_variables as gv
from loguru import logger
from decorators.decor_command import in_channel, is_owner
from utils.class_for_help_command import InitialClass


class OwnerCommand(commands.Cog, InitialClass):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.set_help_str(OwnerCommand)
        logger.debug(f"owner: {OwnerCommand.help_str}")

    @commands.command()
    @in_channel(is_test=True)
    @logger.catch
    @is_owner
    async def test(self, ctx: commands.context.Context):
        await ctx.send(gv.DataBaseClass.get_channel_status(687290997453225984))


def setup(bot):
    bot.add_cog(OwnerCommand(bot))
