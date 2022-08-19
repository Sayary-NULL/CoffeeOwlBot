import discord
from loguru import logger
from discord.ext import commands
import utils.global_variables as gv
from decorators.decor_command import in_channel, is_admin as d_is_admin, add_description


class AdminCommand(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.group()
    @logger.catch
    async def admin(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'{ctx.author.mention}, команды в группе не найдены')

    @commands.group()
    @logger.catch
    async def trigger(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'{ctx.author.mention}, команды в группе не найдены')

    @commands.group()
    @logger.catch
    async def channel(self, ctx: commands.context.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'{ctx.author.mention}, команды в группе не найдены')

    @channel.command()
    @d_is_admin
    @logger.catch
    async def getperm(self, ctx: commands.context.Context):
        if (per := gv.DataBaseClass.get_channel_status(ctx.channel.id)) is not None:
            await ctx.send(f'is_base = {per[1]}\nis_command = {per[2]}\nis_admin = {per[3]}\nis_test = {per[4]}')
        else:
            await ctx.send('Не установлено')

    @channel.command()
    @d_is_admin
    @logger.catch
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

    @trigger.command()
    @d_is_admin
    @logger.catch
    @in_channel(is_admin=True, is_command=True)
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

    @trigger.command()
    @d_is_admin
    @logger.catch
    @in_channel(is_admin=True, is_command=True)
    async def set(self, ctx: commands.context.Context, text_request: str, text_response: str):
        text_request = text_request.lower()
        text_response = text_response.lower()
        try:
            gv.DataBaseClass.set_trigger(text_request, text_response)
            await ctx.send('Добавлено')
        except:
            await ctx.send('Произошла ошибка, обратитесь к Sayary')

    @trigger.command()
    @d_is_admin
    @logger.catch
    @in_channel(is_admin=True, is_command=True)
    async def delt(self, ctx: commands.context.Context, id_trigger: int):
        try:
            gv.DataBaseClass.del_trigger(id_trigger)
            await ctx.send('Удалено')
        except:
            await ctx.send('Произошла ошибка, обратитесь к Sayary')

    @add_description('Реальный варн пользователей')
    @admin.command(name='ban')
    @logger.catch
    @d_is_admin
    @in_channel(is_admin=True, is_base=True)
    async def ban(self, ctx: commands.context.Context, user: discord.Member, reason: str = None,
                       del_message_days: int = None):
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
        """else:
            await user.ban(reason=reason, delete_message_days=del_message_days)"""

        emd = discord.Embed(color=gv.AdminColor)
        emd.add_field(name='**Бан**', value=f'К пользователю {user.mention} применена высшая мера наказания', inline=False)
        emd.add_field(name='**Причина**', value=f'{reason if reason is not None else "Не указанно"}', inline=False)
        emd.set_image(url=url_image)
        emd.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=emd)

    @admin.command()
    @d_is_admin
    @logger.catch
    async def warn(self, ctx: commands.context.Context, user: discord.Member, reason: str = None):
        pass


def setup(bot):
    bot.add_cog(AdminCommand(bot))
