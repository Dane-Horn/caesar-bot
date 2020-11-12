import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from modules import roll, pokerole, gurps, summon
from bot import bot

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot.run(token)
