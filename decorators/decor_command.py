import discord.ext.commands
import functools
import utils.global_variables as gv


def in_channel(is_base: bool = False, is_command: bool = False, is_admin: bool = False, is_test: bool = False):
    def decor(fn):
        @functools.wraps(fn)
        async def decor2(self, ctx: discord.ext.commands.context.Context, *args, **kwargs):
            channel_id = ctx.channel.id
            rez = gv.DataBaseClass.get_channel_status(channel_id)
            if rez is not None:
                if rez[1] == is_admin or rez[2] == is_base or rez[3] == is_test or rez[4] == is_command:
                    await fn(self, ctx, *args, **kwargs)
            else:
                await ctx.send('канал не подходит под условия')
        return decor2
    return decor


# raspberry
def is_admin(fn):
    @functools.wraps(fn)
    async def decor(self, ctx: discord.ext.commands.context.Context, *args, **kwargs):
        perm: discord.permissions.Permissions = ctx.author.guild_permissions
        if perm.administrator:
            await fn(self, ctx, *args, **kwargs)
        else:
            await ctx.send('Недостаточно прав')
    return decor


def is_owner(fn):
    @functools.wraps(fn)
    async def decor(self, ctx: discord.ext.commands.context.Context, *args, **kwargs):
        if ctx.author.id == gv.OwnerID:
            await fn(self, ctx, *args, **kwargs)
        else:
            await ctx.send('Доступно только создателю бота')
    return decor


def add_description(description: str = None):
    def decorator(fn):
        fn.description = description
        return fn
    return decorator
