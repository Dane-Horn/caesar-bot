import random
from discord.ext.commands import Command
from bot import bot  # pylint: disable=no-name-in-module

@bot.command('g')
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
        result += f' {"+" if mod >= 0 else "-"} {abs(mod)}'
    result += f' = {roll}'
    result += f'\n{"Beaten" if roll < goal else "Lost"} by: {abs(roll-goal)}'
    print(result)
    await ctx.send(f'{ctx.author.mention}\n{result}')
