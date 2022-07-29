import discord
from utils import global_variables


def user_is_admin(user: discord.Member):
    flag = False
    for item in user.roles:
        flag |= item.permissions.administrator
    return flag


def user_is_owner(user: discord.Member):
    return user.id == global_variables.OwnerID


def get_help_from_class(cls):
    out_str = ''
    ignor_list = set()
    for base in cls.__bases__:
        for func_name in dir(base):
            ignor_list.add(func_name)
    i = 0
    for func_name in dir(cls):
        func = getattr(cls, func_name)
        if not callable(func) or func_name.startswith('_') or func_name in ignor_list:
            continue

        i += 1
        out_str += f'{i}: {func_name} '
        for par_name, par_type in func.__dict__['params'].items():
            if par_name == 'self' or par_name == 'ctx':
                continue
            if par_type.default is None:
                out_str += f'<{par_name}> '
            else:
                out_str += f'[{par_name}] '

        out_str += '\n'
    return out_str[:-1]
