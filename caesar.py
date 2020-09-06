import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
from tokenParser import parse
from tokenizer import tokenize
import math
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has come online!')


@bot.command(name='r')
async def roll(ctx, *roll):
    print(''.join(roll))
    result = ''
    try:
        result = parse(''.join(roll))
    except:
        result = 'Alea iacta est - non'
    await ctx.send(f'{ctx.author.mention} {result}')


@bot.command(name='p')
async def poke(ctx, n):
    n = int(n)
    rolls = [random.randint(1, 6) for _ in range(n)]
    result = \
        f''' 
Rolls: {' '.join(map(str, rolls))}    
Successes: {len(list(filter(lambda r: r > 3, rolls)))}
Failures: {len(list(filter(lambda r: r <= 3, rolls)))}
'''[2:]
    await ctx.send(f'{ctx.author.mention}\n{result}')


@bot.command(name='g')
async def gurps(ctx, *args):
    goal = None
    mod = 0
    if len(args) >= 2:
        goal = int(args[0])
        mod = int(args[1])
    else:
        goal = int(args[0])
    rolls = [random.randint(1, 6) for _ in range(3)]
    roll = sum(rolls)
    if mod:
        roll += mod 
    result = f'Rolls: {{{", ".join(map(str, rolls))}}}'
    if mod:
        result += f' {"+" if mod >= 0 else "-"} {mod}'
    result += f' = {roll}'
    result += f'\n{"Beaten" if roll < goal else "Lost"} by: {abs(roll-goal)}'
    print(result)
    await ctx.send(f'{ctx.author.mention}\n{result}')


bot.run(token)
# comment
