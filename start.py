import json
import os
from discord.ext import commands
import argparse
from loguru import logger
from DataBase.DB import DB
import utils.global_variables as gv

bot = commands.Bot(command_prefix='>')
bot.remove_command('help')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_const', const=True)
    parser.add_argument('-d', '--debug', action='store_const', const=False)
    arg = parser.parse_args()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script')

    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    logger_level = 'INFO'

    gv.DataBaseClass = DB(config['file_db'])

    if arg.debug:
        logger_level = 'DEBUG'

    token = config['token_owl']
    if arg.test:
        token = config['token_test']
        logger_level = 'DEBUG'

    logger.add('logs/logs_{time:YY_M_D}.log', format='[{time:YY.M.D HH:m:s}] - {level}: {message}', level=logger_level,
              rotation='1 MB', compression='zip')

    logger.info('Start load functions')
    for item in os.listdir(path):
        if not item.startswith('_'):
            logger.debug(item)
            bot.load_extension(f'script.{item[:-3]}')
    logger.info('End load functions')

    logger.info('Запуск')
    bot.run(token)
