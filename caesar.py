import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
from customParser import Parser
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
        result = Parser().parse(''.join(roll))
    except:
        result = 'Alea iacta est - non'
    await ctx.send(f'{ctx.author.mention} {result}')

@bot.command(name = 'p')
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

bot.run(token)
#comment