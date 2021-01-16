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
async def groupselector(ctx, groups, memgroups, *people):
    print('[Commands] Group selector called')
    groupam = int(groups)
    memberg = int(memgroups)
    people = list(people)
    groupstring = ''
    embed=discord.Embed(title="Group selector", description=f'Groups selected', color=0xff0000)
    for group in range(groupam):
        peopleing = ''
        groupstring = groupstring + f' Group {group + 1}:'
        for personum in range(memberg):
            person = random.choice(people)
            peopleing = peopleing + person + ", "
            people.remove(person)
        embed.add_field(name=f' Group {group + 1}:', value=f'{peopleing[:-2]}', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, polltitle, amanswers, length, *answers):
    print('[Commands] Poll called') #1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣
    emojilist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    embed=discord.Embed(title=polltitle, description=f'Poll created by {ctx.author.mention} \nReact with the corresponding emoji to answer.', color=0xff0000)
    answerslist = ''
    amanswersl = min(int(amanswers), 9, len(answers))
    answerstrue = answers[0 : amanswersl]
    for answer in answerstrue:
        answerslist = answerslist + f'{answer} '
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
    for currreact in messagereacts[:amanswersl]:
        if currreact.count == highest.count:
            tied = f'{tied} {answerstrue[messagereacts.index(currreact)]}'
        if currreact.count > highest.count:
            highest = currreact
            tied = ' '
    winner = answerstrue[messagereacts.index(highest)]
    if not tied == ' ':
        print('[Poll] Score tied, printing multiple winners')
        winner = tied
    donembed=discord.Embed(color=0xff0000)
    donembed.add_field(name='Poll ended', value=f'Poll ended winner: {winner}', inline=False)
    donembed.set_footer(text="TAIBot - Poll ended")
    await timemsg.edit(embed = donembed)

@bot.command(name = 'info',)
async def info(ctx):
    print('[Commands] Info called')
    embed=discord.Embed(title="Commands", description="Useful information about the bots commands", color=0xff0000)
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1305379416772620290/C8r6a81q_400x400.jpg")
    embed.add_field(name="!info", value="Brings up this help window. \n !info", inline=False)
    embed.add_field(name="!onlinerole", value="Checks how many members of the role are online. \n !onlinerole {@Role} ", inline=False)
    embed.add_field(name="!contactinfo", value="Direct messages you contact info about TAI staff. \n !contactinfo", inline=False)
    embed.add_field(name="!poll", value="Creates a poll with reactions. \n !poll {Poll title} {amount of answers} {time (minutes)} {answers separated by spaces, surrounded by quotes}", inline=False)
    embed.add_field(name="!timer", value="Sets up a countdown timer. \n !timer {s = seconds, m = minutes} {length}", inline=False)
    embed.add_field(name="!dice", value="Rolls dice. \n !dice {amount of dice} {sides of dice}", inline=False)
    embed.add_field(name="!groupselector", value="Randomly chooses groups out of a list of people. \n !groupselector {amount of groups} {people per group} {people to select from, separated by spaces surronded by quotes}", inline=False)
    embed.add_field(name="!helpme", value="Gives more information on a specified command and gives an example. \n !helpme {command without !}", inline=False)
    embed.set_footer(text="TAIBot - Information window.")
    await ctx.send(embed=embed)

@bot.command(name = 'helpme')
async def helpme(ctx, command):
    print('[Commands] Helpme called')
    embed=discord.Embed(title="Command help", description=f'Information and example of the command {command}', color=0xff0000)
    if command == "info":
            embed.add_field(name="Info", value="Brings up a help window with all commands and information about them.", inline=False)
            embed.add_field(name="Example", value="!info", inline=False)
    elif command == "onlinerole":
            embed.add_field(name="Info", value="Checks and tells you how many of the specified role are online.", inline=False)
            embed.add_field(name="Example", value="!onlinerole @DATA20", inline=False)
    elif command == "contactinfo":
            embed.add_field(name="Info", value="Direct messages you contact information about some of the TAI data staff.", inline=False)
            embed.add_field(name="Example", value="!contactinfo", inline=False)
    elif command == "poll":
            embed.add_field(name="Info", value="Makes a poll that users can vote on, lasts a specified time before giving the winner.", inline=False)
            embed.add_field(name="Example", value="!poll \"Hur lång ska klassen va\" 3 1 \"2h\" \"1h\" \"15h\"", inline=False)
    elif command == "timer":
            embed.add_field(name="Info", value="Sets up a live countdown timer that counts down from the specified time.", inline=False)
            embed.add_field(name="Example", value="!timer m 10", inline=False)
    elif command == "dice":
            embed.add_field(name="Info", value="Rolls the specified dice and amount of dice and gives you the answer.", inline=False)
            embed.add_field(name="Example", value="!dice 2 6", inline=False)
    elif command == "groupselector":
            embed.add_field(name="Info", value="Automatically splits up the listed people in to specified groups.", inline=False)
            embed.add_field(name="Example", value="!groupselector 3 2 \"Mikael\" \"Emil\" \"Elias\" \"Jon\" \"Karl\" \"Amos\"", inline=False)
    elif command == "helpme":
            embed.add_field(name="Info", value="Gives you information and an example about a specified command.", inline=False)
            embed.add_field(name="Example", value="!helpme poll", inline=False)
    else:
        embed=discord.Embed(title='Unkown command', description=f'You typed: {command}, please make sure you are only typing the command without the ! and all lowercase.', color=0xff0000)
    await ctx.send(embed = embed)

        

@bot.command(name = 'timer')
async def timer(ctx, sorm, length):
    print('[Commands] Timer called')
    lengint = int(length)
    if sorm == 's':
        print('[Timer] Seconds selected')
        embed = discord.Embed(title="Timer", description=f'Time left: {lengint} second(s).', color=0xff0000)
        timermsg = await ctx.send(embed=embed)
        for sec in range(lengint)[1:]:
            await asyncio.sleep(1)
            newembed = discord.Embed(title="Timer", description=f'Time left: {lengint - sec} second(s).', color=0xff0000)
            await timermsg.edit(embed=newembed)
        await asyncio.sleep(1)
        finishedembed = discord.Embed(title="Timer", description=f'Time is up!.', color=0xff0000)
        await timermsg.edit(embed=finishedembed)
        print('[Timer] Finished')
    elif sorm == 'm':
        print('[Timer] Minutes selected')
        embed = discord.Embed(title="Timer", description=f'Time left: {lengint} minute(s).', color=0xff0000)
        timermsg = await ctx.send(embed=embed)
        for minl in range(lengint)[1:]:
            await asyncio.sleep(60)
            newembed = discord.Embed(title="Timer", description=f'Time left: {lengint - minl} minute(s).', color=0xff0000)
            await timermsg.edit(embed=newembed)
        await asyncio.sleep(60)
        finishedembed = discord.Embed(title="Timer", description=f'Time is up!.', color=0xff0000)
        await timermsg.edit(embed=finishedembed)
        print('[Timer] Finished')

@bot.command(name='dice')
async def dice(ctx, adice, sdice):
    print('[Commands] Dice called')
    amountdice = int(adice)
    sidedice = int(sdice) + 1
    dicestring = ''
    for die in range(amountdice):
        diceresult = random.randrange(1, sidedice)
        dicestring = dicestring + str(diceresult) + " "
    print('[Dice] Result: ' + dicestring)
    embed = discord.Embed(title="Dice", description=f'Dice result(s): {dicestring}', color=0xff0000)
    await ctx.send(embed=embed)

@bot.command()
async def contactinfo(ctx):
    print('[Commands] Contact info called')
    await ctx.author.create_dm()
    await ctx.send("Direct messaging you the contact info!")
    embed=discord.Embed(title="Here is your information!", description="Contact information for the TAI staff", color=0xff0000)
    embed.add_field(name="Rainer", value="+3584458128", inline=True)
    embed.add_field(name="Thomas", value="+381884719", inline=True)
    embed.set_footer(text="TAIBot - Contact Information.")
    await ctx.author.dm_channel.send(embed=embed)

@bot.command()
async def onlinerole(ctx, role: discord.Role):
    print('[Commands] Online role called')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    rolemems = 0
    onlinemems = 0
    for member in guild.members:
        for _role in member.roles:
            if _role.id == role.id:
                print(
                    f'[Onlinerole] {member.name} has role {role.name} and is {member.status}'
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