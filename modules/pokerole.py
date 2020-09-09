import random
from discord.ext.commands import Command
from bot import bot  # pylint: disable=no-name-in-module


@bot.command('p')
async def pokerole(ctx, n):
    n = int(n)
    rolls = [random.randint(1, 6) for _ in range(n)]
    result = \
        f''' 
Rolls: {' '.join(map(str, rolls))}    
Successes: {len(list(filter(lambda r: r > 3, rolls)))}
Failures: {len(list(filter(lambda r: r <= 3, rolls)))}
'''[2:]
    await ctx.send(f'{ctx.author.mention}\n{result}')
