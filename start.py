import json
from discord.ext import commands
import argparse

bot = commands.Bot(command_prefix='>')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_const', const=True)
    parser.add_argument('-d', '--debug', action='store_const', const=False)
    arg = parser.parse_args()

    with open('config.json', 'r') as file:
        config = json.load(file)

    token = config['token_owl']
    if arg.test:
        token = config['token_test']

    bot.run(token)
