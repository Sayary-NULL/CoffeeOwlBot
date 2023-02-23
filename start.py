import argparse
import os
import sys
from DataBase.DB import DB
import utils.global_variables as gv
import discord
import json
import asyncio
from discord.ext import commands
from loguru import logger
from utils.create_tabels import create_tables

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)
bot.remove_command('help')


@bot.command()
async def reload(ctx: commands.context.Context):
    if ctx.author.id != gv.OwnerID:
        return
    logger.info('Start reload functions')
    for item in os.listdir('./script'):
        if not item.startswith('_'):
            logger.debug(item)
            await bot.reload_extension(f'script.{item[:-3]}')
    logger.info('End reload functions')
    await ctx.send(f'{ctx.author.mention}, перезагрузка модулей завершена')


async def start_bot(token: str):
    async with bot:
        logger.info('Start load functions')
        for item in os.listdir('./script'):
            if item.startswith('_'):
                continue
            logger.debug(f'загрузка модуля: {item[:-3]}')
            await bot.load_extension(f'script.{item[:-3]}')
        logger.info('End load functions')

        await bot.start(token)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_const', const=True)
    parser.add_argument('-d', '--debug', action='store_const', const=True)
    arg = parser.parse_args()

    logger_level = 'INFO'

    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    create_tables(config['file_db'])
    gv.DataBaseClass = DB(config['file_db'])
    token = config['token_owl']
    gv.options = config.get('options', dict())

    if arg.debug or arg.test:
        logger_level = 'DEBUG'
        gv.ISDebug = True

    if arg.test:
        token = config['token_test']
        logger_level = 'DEBUG'
        gv.TestBot = True

    logger.add('logs/logs_{time:YY_MM_DD}.log', level=logger_level, rotation='1 MB', compression='zip')

    with open('version.json', 'r') as f:
        ver = json.load(f)['ver']

    logger.info(f'Запуск бота версии: {ver}')

    asyncio.run(start_bot(token))

    logger.info('Бот выключен')


if __name__ == '__main__':
    main()
