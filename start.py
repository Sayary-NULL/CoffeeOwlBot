import json
import os
from discord.ext import commands
import argparse

bot = commands.Bot(command_prefix='>')
bot.remove_command('help')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_const', const=True)
    parser.add_argument('-d', '--debug', action='store_const', const=False)
    arg = parser.parse_args()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script')

    with open('config.json', 'r') as file:
        config = json.load(file)

    token = config['token_owl']
    if arg.test:
        token = config['token_test']

    for item in os.listdir(path):
        if not item.startswith('_'):
            bot.load_extension(f'script.{item[:-3]}')

    print('run bot')
    bot.run(token)
