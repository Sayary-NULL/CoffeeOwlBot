import re
import discord
import requests
import utils.global_variables as gv
from loguru import logger
from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext.commands import Bot
from discord.ext import tasks, commands


class ThreadTasks(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot: Bot = bot
        self.news_nasa.start()
        self.old_date = None

    def cog_unload(self):
        self.news_nasa.cancel()

    @tasks.loop(minutes=1.0)
    async def news_nasa(self):
        guild_id = 484402073744703498
        channel_id = 687285704849489935

        if gv.TestBot:
            guild_id = 435485527156981770
            channel_id = 531541696995917844

        date = datetime.now().date()
        time = datetime.now().time()

        logger.info('Start task news_nasa')

        if gv.ISDebug:
            logger.debug(f'nasa_news: guild_id - {guild_id}, channel_id - {channel_id}, '
                         f'status - {"on" if gv.ISPostNasaNews else "off" }, '
                         f'data - {date} '
                         f'time - {time} '
                         f'old_date - {self.old_date}')

        if not gv.ISPostNasaNews:
            logger.info('skip task news_nasa')
            return

        if self.old_date is not None and date > self.old_date and time.hour != 8:
            logger.debug('skip nasa_news')
            return

        self.old_date = date

        guild: discord.Guild = self.bot.get_guild(guild_id)
        channel: discord.TextChannel = guild.get_channel(channel_id)

        response = requests.get('https://apod.nasa.gov/apod/')
        if response.status_code == 200:
            text = response.text

            soup = BeautifulSoup(text, "lxml")
            body = soup.body
            href = body.find_all('a', href=re.compile(r'image/\d{4}'))[0]
            min_src = href.img['src']

            description = str(body.find_all('p')[2])[26:-5]
            description = description.replace('\n', '')
            description = re.sub(r'<a href=".+?">(.+?)</a>', r'\1', description)

            replaces = [
                (' .', '. '),
                (' ,', ', '),
                ('.', '. '),
                (',', ', '),
                ('  ', ' ')
            ]

            for repl_item in replaces:
                description = description.replace(*repl_item)

            emd = discord.Embed(color=gv.AdminColor)
            emd.add_field(name='**Описание**', value=description)
            emd.add_field(name='**Ссылка на большую версию**', value=f'https://apod.nasa.gov/apod/{href["href"]}',
                          inline=False)
            emd.set_image(url=f'https://apod.nasa.gov/apod/{min_src}')
            emd.set_footer(text=guild.name, icon_url=guild.icon_url)
            await channel.send(embed=emd)

    @news_nasa.before_loop
    async def before_news_nasa(self):
        logger.info('await connect bot')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(ThreadTasks(bot))
