import discord
from utils import global_variables


def user_is_admin(user: discord.Member):
    flag = False
    for item in user.roles:
        flag |= item.permissions.administrator
    return flag


def user_is_owner(user: discord.Member):
    return user.id == global_variables.OwnerID
