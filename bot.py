# bot.py
import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} Is connected to {guild.name}'
    )
<<<<<<< HEAD
bot.event
async def def on_voice_state_update(member, before, after):
    for voicechanel in guild.voice_channels:
       print(voicechanel.name)
       if voicechanel.name == 'DATA19':
           await voicechanel.edit(reasone=None, name='Cheese')
    

@bot.command()
async def info(ctx):
    print('HelpMe commanded')
    response = '´´´TAIBot HELP \n Commands: \n info: Gives information regarding the server \n Onlinerole: Checks how many users of specified role are online \n Contact info: DMs you important contact info´´´'
    await ctx.send(response)

@bot.command()
async def contactinfo(ctx):
    print('Contact info commanded')
    await ctx.author.create_dm()
    await ctx.author.dm_channel.send(
        f'Hi {ctx.author.name}, here is the information you asked for'
    )
    

bot.run(TOKEN)