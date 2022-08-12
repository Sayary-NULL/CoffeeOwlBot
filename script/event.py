import discord
import random
from discord.ext import commands
from loguru import logger
from utils.global_variables import DataBaseClass
from utils.utils_methods import generate_parameter_from_trigger


class Events(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    @logger.catch
    async def on_message(self, message: discord.message.Message):
        if message.author == self.bot.user:
            return

        mess = message.content.lower()

        response_db = DataBaseClass.get_trigger_form_text(mess)
        if not response_db:
            return
        id_random_response = random.randint(0, len(response_db) - 1)
        text_response: str = response_db[id_random_response][0]

        for k, v in generate_parameter_from_trigger(message).items():
            if text_response.find(k) != -1:
                text_response = text_response.replace(k, v)

        await message.channel.send(text_response)

    @commands.Cog.listener()
    @logger.catch
    async def on_ready(self):
        logger.info('Bot ready!')


def setup(bot):
    bot.add_cog(Events(bot))
