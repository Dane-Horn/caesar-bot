import random
from discord.ext.commands import Command
from bot import bot  # pylint: disable=no-name-in-module


@bot.command('summon')
async def pokerole(ctx, n):
    await ctx.send(f'{ctx.author.mention} you have no power here!')
