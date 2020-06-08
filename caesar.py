import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
from customParser import Parser
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')
@bot.event
async def on_ready():
    print(f'{bot.user.name} has come online!')

@bot.command(name='r')
async def roll(ctx, *roll):
    print(''.join(roll))
    response = f'{ctx.author.mention} Rolling 1d6 = {random.randint(1, 6)}'
    result = ''
    try:
        result = Parser().parse(''.join(roll))
    except:
        result = 'Hell naw'
    await ctx.send(f'{ctx.author.mention} {result}')
bot.run('NzE4OTQxNzY4NDA5ODA4OTk3.XtwM7g.YlTMDA3zIQmAaMnR344DDqB1Auk')