import discord
from discord.ext import commands
import utils.global_variables as gv
from decorators.decor_command import in_channel, is_owner


class OwnerCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    @in_channel(is_test=True)
    @is_owner
    async def test(self, ctx: commands.context.Context):
        await ctx.send(gv.DataBaseClass.get_channel_status(687290997453225984))


def setup(bot):
    bot.add_cog(OwnerCommand(bot))
