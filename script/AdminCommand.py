import datetime

import discord
from loguru import logger
from discord import app_commands
from discord.ext import commands
import utils.global_variables as gv
from utils.utils_methods import generate_parameter_from_trigger
from decorators.decor_command import in_channel, write_log
from decorators.chekers import checks, is_admin, in_channel


class AdminCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.url = 'https://media.discordapp.net/attachments/462236317926031370/464447806887690240/news26052017.jpg' \
                   '?width=1193&height=671 '
        self.title = None
        self.desc = None

    # =======GROUP=======

    @commands.hybrid_group(description='Команды для админов')
    @logger.catch
    async def admin(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'{ctx.author.mention}, команды в группе не найдены')

    @commands.hybrid_group(description='Команды для работы с триггирами')
    @logger.catch
    async def trigger(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'{ctx.author.mention}, команды в группе не найдены')

    @commands.hybrid_group(description='Команды для работы с каналами')
    @logger.catch
    async def channel(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'{ctx.author.mention}, команды в группе не найдены')

    @commands.hybrid_group(description='команда для публикации новостей')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True))
    async def news(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'{ctx.author.mention}, команды в группе не найдены')

    # =======Command=======

    @channel.command(description='Возвращает параметры доступа канала')
    @write_log('get permissions')
    @logger.catch
    @checks(is_admin)
    async def getperm(self, ctx: commands.context.Context):
        if (per := gv.DataBaseClass.get_channel_status(ctx.channel.id)) is not None:
            await ctx.send(f'is_base = {per[1]}\nis_command = {per[2]}\nis_admin = {per[3]}\nis_test = {per[4]}')
        else:
            await ctx.send('Не установлено')

    @channel.command(description='Устанавливает параметры доступа для канала')
    @write_log('set permissions')
    @logger.catch
    @checks(is_admin)
    async def setperm(self, ctx: commands.context.Context,
                                      is_base: bool = False,
                                      is_command: bool = False,
                                      is_admin: bool = False,
                                      is_test: bool = False,
                                      channel_id: int = None):
        if channel_id is None:
            channel_id = ctx.channel.id
        if gv.DataBaseClass.get_channel_status(channel_id) is None:
            gv.DataBaseClass.set_channel_status(channel_id=channel_id,
                                                is_base=is_base,
                                                is_command=is_command,
                                                is_admin=is_admin,
                                                is_test=is_test)
            await ctx.send('Установлено')
        else:
            gv.DataBaseClass.update_channel_status(channel_id=channel_id,
                                                   is_base=is_base,
                                                   is_command=is_command,
                                                   is_admin=is_admin,
                                                   is_test=is_test)
            await ctx.send('Обновлено')

    @trigger.command(description='Возвращает активные триггеры')
    @write_log('select trigger')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True))
    async def select(self, ctx: commands.context.Context):
        str_out = ''
        for i, item in enumerate(gv.DataBaseClass.get_trigger_form_text()):
            str_out += f'{item[0]}) {item[1]} => {item[2]}\n'
            if i % 5 == 0 and i != 0:
                await ctx.send(str_out)
                str_out = ''
        if str_out != '':
            await ctx.send(str_out)
        await ctx.send('=====Триггеры закончились=====')

    @trigger.command(description='Устанавливает новый триггер')
    @app_commands.describe(
        text_request='Текст на который будет триггерится бот',
        text_response='Текст ответа на триггер'
    )
    @write_log('set trigger')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True))
    async def set(self, ctx: commands.context.Context, text_request: str, text_response: str):
        text_request = text_request.lower()
        text_response = text_response.lower()
        try:
            gv.DataBaseClass.set_trigger(text_request, text_response)
            await ctx.send('Добавлено')
        except:
            await ctx.send('Произошла ошибка, обратитесь к Sayary')

    @trigger.command(description='Возвращает строки которые будут заменены при вызове триггера')
    @write_log('trigger meta')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True))
    async def meta(self, ctx: commands.context.Context):
        param = generate_parameter_from_trigger(ctx.message)
        text = 'Параметры для замены в триггере\n'
        for k, v in param.items():
            text += f'{k} -> {v}\n'
        await ctx.send(text)

    @trigger.command(name='del', description='удаление триггера по id')
    @write_log('del trigger')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True))
    async def _del(self, ctx: commands.context.Context, id_trigger: int):
        try:
            gv.DataBaseClass.del_trigger(id_trigger)
            await ctx.send('Удалено')
        except:
            await ctx.send('Произошла ошибка, обратитесь к Sayary')

    @admin.command(name='ban', description='Реальный варн пользователей')
    @write_log('admin ban')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True))
    async def ban(self, ctx: commands.context.Context, user: discord.Member, del_message_days: int = None, *,
                  reason: str = None):
        if user.bot:
            return

        if del_message_days is None:
            del_message_days = 1

        url_image = 'https://steamuserimages-a.akamaihd.net/ugc/923666962148926254/1AEB8BA3672B07726AC719DFF9F270A604D43278/?imw=512&amp;imh=520&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true'

        if user.id == gv.OwnerID:
            await ctx.send(f"{ctx.author.mention}, я не пойду против своего создателя!")
            user = ctx.author
            text = "Не уважение к моему создателю!"
            url_image = 'https://media.discordapp.net/attachments/462236317926031370/1003226679403102248/1579887266_2020-01-24_19-57-45.gif'
        else:
            await user.ban(reason=reason, delete_message_days=del_message_days)

        emd = discord.Embed(color=gv.AdminColor)
        emd.add_field(name='**Бан**', value=f'К пользователю {user.mention} применена высшая мера наказания', inline=False)
        emd.add_field(name='**Причина**', value=f'{reason if reason is not None else "Не указанно"}', inline=False)
        emd.set_image(url=url_image)
        emd.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
        await ctx.send(embed=emd)

    @admin.command(description='Реальный варн пользователям')
    @write_log('admin warn')
    @logger.catch
    @checks(is_admin, in_channel(is_base=True))
    async def warn(self, ctx: commands.context.Context, user: discord.Member):
        if user.bot:
            await ctx.send(f'{ctx.author.mention}, с ботами не работаю')
            return

        count_warns = gv.DataBaseClass.get_warns(user.id)

        if count_warns is None:
            count_warns = 0

        count_warns = count_warns[0]

        if count_warns > 10:
            count_warns += int(count_warns / 5)*0.25

        count_warns += 1

        match round(count_warns) % 5:
            case 1:
                await ctx.send(f'{ctx.author.mention}, к {user.mention} применен первый уровень наказания')
                await user.timeout(datetime.timedelta(minutes=5))
            case 2:
                await ctx.send(f'{ctx.author.mention}, к {user.mention} применен второй уровень наказания')
                await user.timeout(datetime.timedelta(days=1))
            case 3:
                await ctx.send(f'{ctx.author.mention}, к {user.mention} применен третий уровень наказания')
                await user.timeout(datetime.timedelta(weeks=1))
            case 4:
                await ctx.send(f'{ctx.author.mention}, к {user.mention} применен четвертый уровень наказания')
                await user.timeout(datetime.timedelta(weeks=1))
            case 5:
                await ctx.send(f'{ctx.author.mention}, к {user.mention} применен пятый уровень наказания')
                await user.timeout(datetime.timedelta(weeks=2))

        gv.DataBaseClass.set_warns(user.id, count_warns)





    @admin.command(description='Переключает показ ежедневных постов NASA')
    @write_log('set nasa_news')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True))
    async def setnasanews(self, ctx: commands.context.Context, status: bool = False):
        gv.ISPostNasaNews = status
        await ctx.send(f'Новости {"включены" if status else "выключены"}')

    @news.command(description='Устанавливает текст новости')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True), err_message=False)
    @write_log('news desc')
    async def desc(self, ctx: commands.context.Context, *, desc: str):
        self.desc = desc
        await ctx.send('Описание установлено')

    @news.command(description='Устанавливает заголовок новости')
    @write_log('news title')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True), err_message=False)
    async def title(self, ctx: commands.context.Context, *, title: str):
        self.title = title
        await ctx.send('Заголовок установлен')

    @news.command(description='Устанавливает изображение новости')
    @write_log('news image')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True), err_message=False)
    async def image(self, ctx: commands.context.Context, url: str):
        self.url = url
        await ctx.send('Изображение установлено')

    @news.command(description='Публикует новость в переданный канал')
    @discord.app_commands.describe(channel='Ссылка или ID канала, если не передано публикует в этом же канале')
    @write_log('news post')
    @logger.catch
    @checks(is_admin, in_channel(is_admin=True, is_command=True), err_message=False)
    async def post(self, ctx: commands.context.Context, channel: discord.TextChannel = None):
        if self.desc is None:
            return
        if channel is None:
            channel = ctx.channel
        try:
            await channel.send(self.url)
            if self.title is not None:
                await channel.send(self.title)
            await channel.send(self.desc)
            await channel.send(f'Автор: {ctx.author.mention}')
        except Exception as e:
            await ctx.send("Ошибка отправки сообщения.")
            logger.error(e)


async def setup(bot):
    await bot.add_cog(AdminCommand(bot))
