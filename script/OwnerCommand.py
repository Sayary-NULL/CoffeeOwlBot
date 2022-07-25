import json
import discord
from discord.ext import commands
import utils.global_variables as gv
from decorators.decor_command import in_channel


class OwnerCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    @in_channel(is_test=True)
    async def test(self, ctx: commands.context.Context):
        if ctx.author.id != gv.OwnerID:
            print('NO')
        print(gv.DataBaseClass.get_channel_status(687290997453225984))


def setup(bot):
    bot.add_cog(OwnerCommand(bot))
