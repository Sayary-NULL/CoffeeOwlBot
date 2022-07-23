import discord
from discord.ext import commands


class UserCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx: commands.context.Context):
        await ctx.send(f'{ctx.author.mention}, hello!')

    @commands.command()
    async def help(self, ctx: commands.context.Context):
        await ctx.send(f'{ctx.author.mention}, у меня обед!')


def setup(bot):
    bot.add_cog(UserCommand(bot))
