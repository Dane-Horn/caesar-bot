import random
from discord.ext.commands import Command
from tokenParser import parse #pylint: disable=import-error
from bot import bot  # pylint: disable=no-name-in-module

@bot.command('r')
async def roll(ctx, *roll):
    print(''.join(roll))
    result = ''
    try:
        result = parse(''.join(roll))
    except:
        result = 'Alea iacta est - non'
    await ctx.send(f'{ctx.author.mention} {result}')