# bot.py
import os
import time
import discord
import random
import math
import asyncio
from asyncio import sleep
from dotenv import load_dotenv
from discord.ext import commands
from discord import reaction

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents = intents)
bot.remove_command('help')
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

@bot.command()
async def poll(ctx, polltitle, amanswers, length, *answers):
    print('Poll commanded') #1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣
    emojilist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    embed=discord.Embed(title="Poll", description=f'Poll created by {ctx.author.mention}', color=0xff0000)
    answerslist = ''
    amanswersl = min(int(amanswers), 9, len(answers))
    answerstrue = answers[0 : amanswersl]
    for answer in answerstrue:
        answerslist = answerslist + f'{answer} '
        print(answer)
        embed.add_field(name=str(answerstrue.index(answer) + 1), value=f'{answer}', inline=False)
    embed.set_footer(text="TAIBot - Poll")
    pollmessage = await ctx.send(embed=embed)
    if amanswersl > 5:
        amanswersl = amanswersl + 1
    for x in range(amanswersl):
        numberindex = x
        await pollmessage.add_reaction(emojilist[numberindex])
    timembed=discord.Embed(color=0xff0000)
    timembed.add_field(name='Poll time', value=f'Minutes left: {int(length)}', inline=False)
    timembed.set_footer(text="TAIBot - Poll time")
    timemsg = await ctx.send(embed=timembed)
    cache_msg = discord.utils.get(bot.cached_messages, id=pollmessage.id)
    for _minute in range(int(length)):
        await asyncio.sleep(60)
        _timembed=discord.Embed(color=0xff0000)
        _timembed.add_field(name='Poll time', value=f'Minutes left: {int(length) - _minute - 1}', inline=False)
        _timembed.set_footer(text="TAIBot - Poll time")
        await timemsg.edit(embed = _timembed)
    messagereacts = cache_msg.reactions
    highest = messagereacts[0]
    tied = ' '
    print(messagereacts)
    for currreact in messagereacts[:amanswersl]:
        print("Reaction: " + str(currreact.count))
        print("Highest:" + str(highest.count))
        if currreact.count == highest.count:
            tied = f'{tied} {answerstrue[messagereacts.index(currreact)]}'
        if currreact.count > highest.count:
            highest = currreact
            tied = ' '
    winner = answerstrue[messagereacts.index(highest)]
    if not tied == ' ':
        print('Score tied, printing multiple winners')
        winner = tied
    donembed=discord.Embed(color=0xff0000)
    donembed.add_field(name='Poll ended', value=f'Poll ended winner: {winner}', inline=False)
    donembed.set_footer(text="TAIBot - Poll ended")
    await timemsg.edit(embed = donembed)

@bot.command(name = 'info',)
async def info(ctx):
    print('Info commanded')
    embed=discord.Embed(title="Commands", description="Useful information about the bots commands", color=0xff0000)
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1305379416772620290/C8r6a81q_400x400.jpg")
    embed.add_field(name="!info", value="Brings up this window. \n !info", inline=False)
    embed.add_field(name="!onlinerole", value="Checks how many of the role are online. \n !onlinerole {@Role} ", inline=False)
    embed.add_field(name="!contactinfo", value="Direct messages you contact info about TAI staff \n !contactinfo", inline=False)
    embed.add_field(name="!poll", value="Creates a poll with reactions \n !poll {amount out answers} {time (minutes)} {answers separated by spaces, surrounded by quotes}", inline=False)
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
    for member in guild.members:
        for _role in member.roles:
            if _role.id == role.id:
                print(
                    f'{member.name} has role {role.name}'
                )
                rolemems = rolemems + 1
                if str(member.status) != 'offline':
                    onlinemems = onlinemems + 1
    embed=discord.Embed(color=0xff0000)
    embed.add_field(name=role.name, value=f'{role.mention} has {onlinemems} out of {rolemems} online', inline=False)
    embed.set_footer(text="TAIBot - Online role")
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
    hassave = 0
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
            voicechanel.edit(reasone=None, name=line)
            asyncio.sleep(1)

bot.loop.create_task(changestatus())
#bot.loop.create_task(checkvoice())
bot.run(TOKEN)
#for voicechanel in guild.voice_channels:
#   print(voicechanel.name)
#   if voicechanel.name == 'DATA19':
#       await voicechanel.edit(reasone=None, name='Cheese')