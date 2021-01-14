# bot.py
import os
import time
import discord
import random
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents = intents)
bot.remove_command('help')
hassave = 0
saveVoice = []
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    #os.system('cls')
    await bot.change_presence(activity=discord.Game(name="!info for help"))
    print(
        '[-------------Connection success-------------] \n'
        f'{bot.user} Is connected to {guild.name}'
    )

@bot.command(name = 'info',)
async def info(ctx):
    print('Info commanded')
    embed=discord.Embed(title="Commands", description="Useful information about the bots commands", color=0xffffff)
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1305379416772620290/C8r6a81q_400x400.jpg")
    embed.add_field(name="!info", value="Brings up this window.", inline=False)
    embed.add_field(name="!onlinerole", value="Checks how many of the specified role are online", inline=False)
    embed.add_field(name="!contactinfo", value="Direct messages you contact info about TAI staff", inline=True)
    embed.set_footer(text="TAIBot - Information window.")
    await ctx.send(embed=embed)

@bot.command()
async def contactinfo(ctx):
    print('Contact info commanded')
    await ctx.author.create_dm()
    await ctx.send("Direct messaging you the contact info!")
    embed=discord.Embed(title="Here is your information!", description="Contact information for the TAI staff", color=0xff0000)
    embed.add_field(name="Rainer", value="+3584458128", inline=True)
    embed.add_field(name="Thomas", value="+381884719", inline=True)
    embed.set_footer(text="TAIBot - Contact Information.")
    await ctx.author.dm_channel.send(embed=embed)

@bot.command()
async def onlinerole(ctx, role: discord.Role):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    rolemems = 0
    onlinemems = 0
    await ctx.send(role.mention)
    for member in guild.members:
        for _role in member.roles:
            if _role.id == role.id:
                print(
                    f'{member.name} has role {role.name}'
                )
                rolemems = rolemems + 1
                if str(member.status) != 'offline':
                    onlinemems = onlinemems + 1
    embed=discord.Embed()
    embed.add_field(name=role.name, value=f'{role.mention} has {onlinemems} out of {rolemems} online', inline=False)
    await ctx.send(embed=embed)

async def changestatus():
    await bot.wait_until_ready()
    statuses = ["Minecraft in class", "!info for help", "CS:GO in class", "Roblox in class", "Valorant in class"]
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(5)

async def checkvoice():
    await bot.wait_until_ready()
    global hassave
    global saveVoice
    while not bot.is_closed():
        await asyncio.sleep(5)
        guild = discord.utils.get(bot.guilds, name=GUILD)
        if hassave == 0:
            for voicechanel in guild.voice_channels:
                saveVoice.append(voicechanel)

        hassave = 1
        
        for voicechanel in guild.voice_channels:
            print(len(voicechanel.members))
            stringformat = f'({len(voicechanel.members)})'
            indexof = guild.voice_channels.index(voicechanel)
            line = saveVoice[indexof].name + stringformat
            print(saveVoice[indexof].name)
            #await voicechanel.edit(reasone=None, name=line)
            await asyncio.sleep(1)

bot.loop.create_task(changestatus())
bot.loop.create_task(checkvoice())
bot.run(TOKEN)
#for voicechanel in guild.voice_channels:
#   print(voicechanel.name)
#   if voicechanel.name == 'DATA19':
#       await voicechanel.edit(reasone=None, name='Cheese')