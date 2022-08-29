import json
import os
import asyncio
from discord.ext import commands
import argparse
from loguru import logger
from DataBase.DB import DB
import utils.global_variables as gv
from utils.create_tabels import create_tables

bot = commands.Bot(command_prefix='>')
bot.remove_command('help')


@bot.command()
async def reload(ctx: commands.context.Context):
    if ctx.author.id != gv.OwnerID:
        return
    logger.info('Start reload functions')
    for item in os.listdir(path):
        if not item.startswith('_'):
            logger.debug(item)
            await bot.reload_extension(f'script.{item[:-3]}')
    logger.info('End reload functions')
    await ctx.send(f'{ctx.author.mention}, перезагрузка модулей завершена')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_const', const=True)
    parser.add_argument('-d', '--debug', action='store_const', const=True)
    arg = parser.parse_args()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script')

    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    logger_level = 'INFO'

    create_tables(config['file_db'])

    gv.DataBaseClass = DB(config['file_db'])
    token = config['token_owl']

    if arg.debug or arg.test:
        logger.debug('Mode BEBUG on')
        logger_level = 'DEBUG'
        gv.ISDebug = True

    if arg.test:
        token = config['token_test']
        logger_level = 'DEBUG'
        gv.TestBot = True

    logger.add('logs/logs_{time:YY_M_D}.log', format='[{time:YY.M.D HH:m:s}] - {level}: {message}', level=logger_level,
               rotation='1 MB', compression='zip')

    logger.info('Start load functions')
    for item in os.listdir(path):
        if not item.startswith('_'):
            logger.debug(item)
            bot.load_extension(f'script.{item[:-3]}')
    logger.info('End load functions')

    with open('version.json', 'r') as f:
        ver = json.load(f)['ver']

    logger.info(f'Запуск бота версии: {ver}')

    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(asyncio.wait([ioloop.create_task(bot.start(token))]))
    ioloop.close()

    logger.info('Бот выключен')
