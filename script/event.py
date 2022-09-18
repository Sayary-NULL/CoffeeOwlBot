import discord
import random
from discord.ext import commands
from loguru import logger
from utils.global_variables import DataBaseClass
from utils.utils_methods import generate_parameter_from_trigger


class Events(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.del_emoji = discord.PartialEmoji(name='💢')

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

        # не ждем пока дискорд сам, сами говорим серверам что мы умные
        guilds_id = [435485527156981770, 484402073744703498]
        for guild_id in guilds_id:
            server = discord.Object(id=guild_id)
            self.bot.tree.copy_global_to(guild=server)
            await self.bot.tree.sync(guild=server)

    @commands.Cog.listener()
    @logger.catch
    async def on_connect(self):
        logger.info('Bot connect!')

    @commands.Cog.listener()
    @logger.catch
    async def on_error(self, event):
        logger.error(event)

    @commands.Cog.listener()
    @logger.catch
    async def on_command_error(self, ctx: discord.ext.commands.context.Context, exception, *args, **kwargs):
        logger.error(f'user: "{ctx.author.name}"({ctx.author.id}), on channel: "{ctx.channel.name}"({ctx.channel.id}), '
                     f'error message: {exception}')
        await ctx.send(f'{ctx.author.mention}, произошла ошибка: {exception}')

    @commands.Cog.listener()
    @logger.catch
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        user: discord.Member = guild.get_member(payload.user_id)

        if user.bot:
            return

        channel: discord.TextChannel = guild.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)

        if user.guild_permissions.administrator and payload.emoji == self.del_emoji:
            await message.delete()


async def setup(bot):
    await bot.add_cog(Events(bot))
