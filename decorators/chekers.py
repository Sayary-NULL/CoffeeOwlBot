import discord
import functools
import utils.global_variables as gv
from discord.ext.commands.context import Context


def checks(*args, err_message: bool = True):
    def decor(fn):
        @functools.wraps(fn)
        async def wrapper(self, ctx: Context, *args2, **kwargs2):
            for item in args:
                if not item(ctx):
                    if err_message:
                        await ctx.send('Доугукался... доступа нет!')
                    return
            await fn(self, ctx, *args2, **kwargs2)

        return wrapper

    return decor


def is_admin(ctx: Context):
    perm: discord.permissions.Permissions = ctx.author.guild_permissions
    return perm.administrator


def is_owner(ctx: Context):
    return ctx.author.id == gv.OwnerID


def only_false(ctx: Context):
    return False


def in_channel(is_base: bool = False, is_command: bool = False, is_admin: bool = False, is_test: bool = False):
    def decor(ctx: discord.ext.commands.context.Context):
        channel_id = ctx.channel.id
        rez = gv.DataBaseClass.get_channel_status(channel_id)
        if rez is None or (not rez[4] and is_test) or (not rez[3] and is_admin):
            return False

        if rez[4] or rez[3] or (rez[2] and is_command) or (rez[1] and is_base):
            return True
    return decor
