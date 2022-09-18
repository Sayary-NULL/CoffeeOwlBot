import discord
from utils import global_variables
from datetime import datetime


def user_is_admin(user: discord.Member):
    flag = False
    for item in user.roles:
        flag |= item.permissions.administrator
    return flag


def user_is_owner(user: discord.Member):
    return user.id == global_variables.OwnerID


def generate_parameter_from_trigger(ctx: discord.message.Message) -> dict:
    return {
        "{time}": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "{user_name}": ctx.author.name,
        "{user_mention}": ctx.author.mention,
        "{channel_name}": ctx.channel.name,
        "{channel_mention}": ctx.channel.mention
    }


def get_param_on_func(func):
    out_str = '```'
    out_str += str(func) + ' '
    for par_name, par_type in func.__dict__['params'].items():
        if par_name == 'self' or par_name == 'ctx':
            continue
        if par_type.default is None:
            out_str += f'<{par_name}> '
        else:
            out_str += f'[{par_name}] '
    return out_str[:-1] + '```'


def get_help_from_class(cls):
    out_str = '```'
    ignor_list = set()
    for base in cls.__bases__:
        for func_name in dir(base):
            ignor_list.add(func_name)
    i = 0
    for func_name in dir(cls):
        func = getattr(cls, func_name)
        if not callable(func) or func_name.startswith('_') or func_name in ignor_list:
            continue

        if func.__dict__['parent'] is not None:
            continue
        out_str += f'> {func_name} '
        if 'description' in dir(func):
            if func.description is not None:
                if func.description.strip() != '':
                    out_str += f'- {func.description}'
        out_str += '\n'

    return out_str[:-1] + '```'


def get_funcs_on_name_or_aliases(func_name, cls):
    for cls_func_name in dir(cls):
        func = getattr(cls, cls_func_name)
        if not callable(func) or cls_func_name.startswith('_'):
            continue
        if func_name == cls_func_name:
            return func
        if 'aliases' in dir(func):
            if func_name in func.aliases:
                return func
    return None


def get_all_group(group_name, cls):
    out_lst = []
    for cls_func_name in dir(cls):
        func = getattr(cls, cls_func_name)
        if not callable(func) or cls_func_name.startswith('_'):
            continue

        param = func.__dict__

        if '__original_kwargs__' in param:
            kwargs = param['__original_kwargs__']
            if 'parent' in kwargs:
                if str(kwargs['parent']) == group_name:
                    out_lst.append(cls_func_name)

    return out_lst if len(out_lst) != 0 else None
