import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        if message.author == self.bot.user:
            return

        mess = message.content.lower()

        if mess == '<:say_paw:982188705068503090>':
            await message.channel.send(f'{message.author.mention}, <:say_paw:982188705068503090>')


def setup(bot):
    bot.add_cog(Events(bot))
