# ████████╗░█████╗░██████╗░
# ╚══██╔══╝██╔══██╗██╔══██╗
# ░░░██║░░░██║░░██║██████╔╝
# ░░░██║░░░██║░░██║██╔═══╝░
# ░░░██║░░░╚█████╔╝██║░░░░░
# ░░░╚═╝░░░░╚════╝░╚═╝░░░░░

# **************** NOTES ****************

# For emoji unicode characters, change + to 000 and place \ in front of it
# For the quotes file always add ,encoding="utf-8" in the brackets ie: (quotesPath,"r",encoding="utf-8")
# Character Ξ reserved for multi-line quote support (check quote functions)
# Retired commands (probably) won't have any new functionality added!

# ================ LIBRARIES ================
import asyncio
import datetime
import random
import time
import discord
from discord.ext import tasks, commands

# ================ VARIABLES ================

with open("discordSecrets.txt","r",encoding="utf-8") as secrets:
    lines = secrets.readlines()
    for i in range(len(lines)):
        line = lines[i]
        lines[i] = line.strip("\n")
        lines[i] = line.split("_")
    TOKEN = str(lines[0][0])
    console = [int(lines[1][0])]
    quoteBookID = int(lines[2][0])
    logsID = int(lines[3][0])
    birthdaysID = int(lines[4][0])
    bdaysID = int(lines[5][0])
    ultralogsID = int(lines[6][0])
    modsID = int(lines[7][0])
    guildID = int(lines[8][0])
    bdaysPath = rf"{str(lines[9][0])}".strip("\n")
    dataPath = rf"{str(lines[10][0])}".strip("\n")
    quotesPath = rf"{str(lines[11][0])}".strip("\n")
    lockedPath = rf"{str(lines[12][0])}".strip("\n")

# ================ INITIALISING ================

intents = discord.Intents.default()
intents.message_content = True

async def main():
    async with bot:
        bot.loop.create_task(checkForNewQuotes())
        bot.loop.create_task(checkForBdays())
        bot.loop.create_task(sayHello())
        await bot.start(TOKEN)

bot = commands.Bot(intents = intents, command_prefix=".", owner_ids=set(console))



# ███████╗██╗░░░██╗███╗░░██╗░█████╗░████████╗██╗░█████╗░███╗░░██╗░██████╗
# ██╔════╝██║░░░██║████╗░██║██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔════╝
# █████╗░░██║░░░██║██╔██╗██║██║░░╚═╝░░░██║░░░██║██║░░██║██╔██╗██║╚█████╗░
# ██╔══╝░░██║░░░██║██║╚████║██║░░██╗░░░██║░░░██║██║░░██║██║╚████║░╚═══██╗
# ██║░░░░░╚██████╔╝██║░╚███║╚█████╔╝░░░██║░░░██║╚█████╔╝██║░╚███║██████╔╝
# ╚═╝░░░░░░╚═════╝░╚═╝░░╚══╝░╚════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░

def addQuotesToFile(quotes): #needed for .addallquotes and .addquotes
    quotes.reverse() #old quotes first, new quotes last (to keep order when appending)
    for qMsg in quotes:
        quote = qMsg.content #content of quote
        sender = qMsg.author #person who sent quote
        if (quote.count("'") >= 2) or (quote.count('"') >= 2) or (("“" in quote) or ("‘" in quote and "’" in quote)): #text quote
            if "\n" in quote: #multi-line support
                quote = quote.replace("\n","Ξ") #Ξ = new line symbol for multi-line quotes
            with open (quotesPath,"a+",encoding="utf-8") as quoteFileAP:
                if (str(quote) + " - " + str(sender) + "\n") not in quoteFileAP:
                    quoteFileAP.write(str(quote) + " - " + str(sender))
                    quoteFileAP.write("\n")

        elif qMsg.attachments: #attachment (image) quote
            attachment = qMsg.attachments[0]
            attachmentUrl = attachment.url
            with open (quotesPath,"a+",encoding="utf-8") as quoteFileAP:
                currentQuotes = quoteFileAP.readlines()
                if (str(attachmentUrl) + " " + str(quote) + " - " + str(sender) + "\n") not in currentQuotes:
                    quoteFileAP.write(str(attachmentUrl) + " " + str(quote) + " - " + str(sender))
                    quoteFileAP.write("\n")

    with open (quotesPath,"r",encoding="utf-8") as quoteFileR:
        lines = quoteFileR.readlines()
        return len(lines)

async def checkForBdays():
    await bot.wait_until_ready()
    today = datetime.date.today()
    with open(bdaysPath,"r",encoding="utf-8") as bdayFileR:
        lines = bdayFileR.readlines()
        for line in lines:
            line = line.rstrip("\n")
            user, mention, date = line.split(" ")
            year, month, day = date.split("-")
            if str(today.strftime("%m-%d")) == f"{month}-{day}":
                bdays = bot.get_channel(bdaysID)
                await bdays.send(f"Happy birthday to {mention}‼️ They are now {int(today.strftime('%Y')) - int(year)} 🎉🎉!")
                # msgs = [msg async for msg in bdays.history(limit=None)]
                # if len(msgs) > 0:
                #     lastMsg = await bdays.fetch_message(bdays.last_message_id)
                #     if str(mention) not in lastMsg.content:
                #         await bdays.send(f"Happy birthday to {mention}‼️ They are now {int(today.strftime('%Y')) - int(year)} 🎉🎉! @everyone")
                # else:
                #     await bot.get_channel(bdaysID).send(f"Happy birthday to {mention}‼️ They are now {int(today.strftime('%Y')) - int(year)} 🎉🎉! @everyone")

async def checkForNewQuotes():
    await bot.wait_until_ready()
    quoteBook = bot.get_channel(quoteBookID)
    newestMsgID = quoteBook.last_message_id
    print(newestMsgID) #debug message
    with open (dataPath,"r",encoding="utf-8") as dataFileR:
        prevMsgID = int(dataFileR.readline())
    try:
        await quoteBook.fetch_message(prevMsgID)
    except discord.NotFound:
        print("discord.NotFound error; message not found, leaving function.")
        return
    if prevMsgID != newestMsgID:
        msgCount = 0
        async for msg in quoteBook.history():
            msgID = int(msg.id)
            if msgID == prevMsgID:
                break
            if msgID != prevMsgID:
                msgCount += 1
        if msgCount > 0:
            print(f"msgCount = {msgCount}") #debug message
            newQuotes = [msg async for msg in quoteBook.history(limit=msgCount)]
            with open(quotesPath,"r",encoding="utf-8") as quoteFileR:
                oldQuoteCount = len(quoteFileR.readlines())
            newQuoteCount = addQuotesToFile(newQuotes)
            logs = bot.get_channel(logsID)
            await logs.send(f"{msgCount} new messages detected in <#{quoteBookID}>.")
            await logs.send(f"Added {newQuoteCount-oldQuoteCount} quotes to discordQuotes.txt. New length = {newQuoteCount}")

async def sayHello():
    await bot.wait_until_ready()
    await bot.get_channel(logsID).send("Alphabet Soup Bot now running.")



# ███████╗██╗░░░██╗███████╗███╗░░██╗████████╗░██████╗
# ██╔════╝██║░░░██║██╔════╝████╗░██║╚══██╔══╝██╔════╝
# █████╗░░╚██╗░██╔╝█████╗░░██╔██╗██║░░░██║░░░╚█████╗░
# ██╔══╝░░░╚████╔╝░██╔══╝░░██║╚████║░░░██║░░░░╚═══██╗
# ███████╗░░╚██╔╝░░███████╗██║░╚███║░░░██║░░░██████╔╝
# ╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚═════╝░

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message): # All on_message
    await bot.process_commands(message)
    
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    if message.author == bot.user:
        return
    # HAVE ALL FUNCTIONS NOT INVOLVING THE BOT INTERACTING WITH ITSELF AFTER THIS POINT
    
    loggedMsg = f"{username}: {user_message} ({channel})"
    print(loggedMsg)
    ultralogs = bot.get_channel(ultralogsID)
    if message.guild.id == guildID:
        await ultralogs.send(loggedMsg)

    if user_message.lower() == "cum": #cum message
        await message.channel.send("mmm cum")

    if user_message.lower() == "hi": #hi message
        await message.channel.send("Hi")

    if user_message.lower() == "sneeze": #sneeze message
        await message.channel.send("Bless you!")

    if user_message.lower() == "cool": #test reaction
        await message.add_reaction("\U0001F60E")

    if channel == "quote-book":
        quote = user_message
        sender = message.author
        if (quote.count("'") >= 2) or (quote.count('"') >= 2) or (("“" in quote) or ("‘" in quote and "’" in quote)): #text quote
            with open (quotesPath,"a",encoding="utf-8") as quoteFile: #put utf-8 otherwise it dies
                if "\n" in quote: #multi-line support
                    quote = quote.replace("\n","Ξ") #Ξ = new line symbol for multi-line quotes
                quoteFile.write(str(quote) + " - " + str(sender))
                quoteFile.write("\n")
        elif message.attachments: #attachment (image) quote
            attachment = message.attachments[0]
            attachmentUrl = attachment.url
            with open (quotesPath,"a",encoding="utf-8") as quoteFile: #put utf-8 otherwise it dies
                quoteFile.write(str(attachmentUrl) + " - " + str(sender))
                quoteFile.write("\n")



# ░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░█████╗░███╗░░██╗██████╗░░██████╗
# ██╔══██╗██╔══██╗████╗░████║████╗░████║██╔══██╗████╗░██║██╔══██╗██╔════╝
# ██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║███████║██╔██╗██║██║░░██║╚█████╗░
# ██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚████║██║░░██║░╚═══██╗
# ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██║░░██║██║░╚███║██████╔╝██████╔╝
# ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚═════╝░

# ================ USER COMMANDS ================

@bot.command()
async def setbday(ctx,name=None,day=None,month=None,year=None):
    if (name and day and month and year) != None:
        if name.isalpha() and day.isnumeric() and month.isnumeric() and year.isnumeric() and len(day) == 2 and len(month) == 2 and len(year) == 4 and str(ctx.channel == "birthdays") and int(day) in range(1,32) and int(month) in range(1,13) and int(year) in range(2000,int(datetime.date.today().strftime("%Y"))):
            user = ctx.author
            userMention = ctx.author.mention
            with open(bdaysPath,"r",encoding="utf-8") as bdayFileR:
                lines = bdayFileR.readlines()
                newLine = f"{user} {userMention} {year}-{month}-{day}\n"
                newUser = True
                for line in lines:
                    if str(user) in line:
                        lines.remove(line)
                        newUser = False
                        break
            if not newUser:
                with open(bdaysPath,"r+",encoding="utf-8") as bdayFileRP:
                    for line in lines:
                        bdayFileRP.write(line) 
                    bdayFileRP.write(newLine)
                await ctx.message.delete()
                await ctx.send(f"Birthday edited to {day}/{month}/{year} ✨", delete_after=10)
                await bot.get_channel(logsID).send(f"{ctx.author.mention} edited birthday to {day}/{month}/{year}")
            elif newUser:
                with open(bdaysPath,"a",encoding="utf-8") as bdayFileA:
                    bdayFileA.write(newLine)
                await ctx.message.delete()
                await ctx.send(f"Birthday added as {day}/{month}/{year} ✨", delete_after=10)
                await bot.get_channel(logsID).send(f"{ctx.author.mention} set birthday to {day}/{month}/{year}")
        else:
            await ctx.message.delete()
            await ctx.send(f"Syntax = in <#{birthdaysID}> .setbday <name> DD MM YYYY", delete_after=10)
    else:
        await ctx.message.delete()
        await ctx.send(f"Syntax = in <#{birthdaysID}> .setbday <name> DD MM YYYY", delete_after=10)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def quote(ctx):
    with open (quotesPath,"r",encoding="utf-8") as quoteFile: #always put utf-8 for the file
        quotes = quoteFile.readlines()
        chosenQuote = random.choice(quotes)
        if "Ξ" in chosenQuote:
            chosenQuote = chosenQuote.replace("Ξ","\n")
        await ctx.send(chosenQuote)

# ================ MOD COMMANDS ================

@bot.command(pass_context=True)
@commands.has_role("mods")
async def masslockdown(ctx):
    await ctx.send("Mass lockdown initiated...")
    for channel in ctx.guild.channels:
        perms = channel.overwrites_for(ctx.guild.default_role)
        if perms.read_messages == True:
            perms.read_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms, reason="Mass Lockdown")
            await channel.send(f"{channel.mention} ***is now in lockdown.***")

            with open (lockedPath,"a", encoding="utf-8") as channelsFile:
                channelsFile.write(channel.id)

    await ctx.send("Lockdown complete.")
    await bot.get_channel(logsID).send(f"{ctx.author.mention} executed .masslockdown")

@bot.command(pass_context=True)
@commands.is_owner()
async def massunlock(ctx): # ================= kinda doesnt work lol ===========================
    await ctx.send("Mass unlock initiated...")
    with open (lockedPath,"r", encoding="utf-8") as channelsFile:
        for line in channelsFile.readlines():
            line.rstrip("\n")
            channel = bot.get_channel(line)
            perms = channel.overwrites_for(ctx.guild.default_role)
            if perms.read_messages == False:
                perms.read_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms, reason="Mass Unlock")
    open(lockedPath,"w", encoding="utf-8").close()
    await ctx.send("Mass unlock successful.")
    await bot.get_channel(logsID).send(f"{ctx.author.mention} executed .massunlock")

@bot.command(pass_context=True)
@commands.has_role("mods")
async def lockdown(ctx):
    perms = ctx.channel.overwrites_for(ctx.guild.default_role)
    if perms.read_messages == True:
        perms.read_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms, reason="Lockdown")
        await ctx.send(f"{ctx.channel.mention} ***is now in lockdown.***")
        await bot.get_channel(logsID).send(f"{ctx.author.mention} executed .lockdown in {ctx.channel.mention}")
    else:
        await ctx.send(f"Error: {ctx.channel.mention} is already locked to \@everyone.")

@bot.command(pass_context=True)
@commands.has_role("mods")
async def unlock(ctx):
    perms = ctx.channel.overwrites_for(ctx.guild.default_role)
    if perms.read_messages == False:
        perms.read_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms, reason="Unlock")
        await ctx.send(f"{ctx.channel.mention} ***has been unlocked.***")
        await bot.get_channel(logsID).send(f"{ctx.author.mention} executed .unlock in {ctx.channel.mention}")
    else:
        await ctx.send(f"Error: {ctx.channel.mention} is already unlocked to \@everyone.")

@bot.command(pass_context=True)
@commands.has_role("mods")
async def createq(ctx): #retired
    if ctx.channel == "❗teacher-comp❗":
        await ctx.message.delete()
        with open("teacherList.txt","r",encoding="utf-8") as doneFileR:
            with open ("teacherList.txt","r",encoding="utf-8") as listFileR:
                lb = doneFileR.readlines()
                lst = listFileR.readlines()
            roundNum = len(lb)
            if roundNum > len(lst):
                print("Error: no teachers left.")
                return None
            teacher = lst[roundNum]
            teacherLst = teacher.split(" ")
            title = str(teacherLst[0])
            name = str(teacherLst[1])
            emoji = str(teacherLst[2])
            new_msg = await ctx.send(f"""`ROUND {roundNum+1}: {title} {name}`

**Teaching Ability:** **WORST** :one: :two: :three: :four: **BEST**
**Personality:** **WORST** :red_circle: :orange_circle: :yellow_circle: :green_circle: **BEST**
:bangbang:__Reminder: Only vote if you have experience (either with teaching or personality)__ :bangbang:

<@&990316741093646376> • {emoji}""")
            await new_msg.add_reaction("1️⃣")
            await new_msg.add_reaction("2️⃣")
            await new_msg.add_reaction("3️⃣")
            await new_msg.add_reaction("4️⃣")
            new_msg = await ctx.send("** **")
            await new_msg.add_reaction("\U0001F534")
            await new_msg.add_reaction("\U0001F7E0")
            await new_msg.add_reaction("\U0001F7E1")
            await new_msg.add_reaction("\U0001F7E2")
    with open("teacherListDone.txt","a",encoding="utf-8") as doneFileA:
        doneFileA.write(teacher)

@bot.command(pass_context=True)
@commands.has_role("mods")
async def addquotes(ctx,*args): #retired
    if len(args) != 1:
        await ctx.send("Incorrect arguments! Syntax: .addquotes <number>")
    else:
        quoteAmount = args[0]
        if not quoteAmount.isnumeric():
            await ctx.send("That's not a number! Syntax: .addquotes <number>")
# actual code for adding quotes beyond this point
        else:
            await ctx.send(f"Command received, started reading {quoteAmount} messages of <#{quoteBookID}>. This could take a while.")
            quoteBook = bot.get_channel(quoteBookID)
            quotes = [quote async for quote in quoteBook.history(limit=int(quoteAmount))] #reads quoteAmount number of messages in channel
            await ctx.send(f"Message transfer of {quoteAmount} messages started. This shouldn't take that long.")
            quotesAdded = addQuotesToFile(quotes) #adding to file in     def addQuotesToFile(quotes)
            await ctx.send(f"Message transfer of {quotesAdded} complete. Check discordQuotes.txt")
 
@bot.command(pass_context=True)
@commands.has_role("mods")
async def addallquotes(ctx):
    await ctx.channel.send(f"Command received, started reading contents of <#{quoteBookID}>. This could take a while.")
    quoteBook = bot.get_channel(quoteBookID)
    quotes = [quote async for quote in quoteBook.history(limit=None)] #reads everything in channel
    open(quotesPath,"w",encoding="utf-8").close() #clears file
    await ctx.channel.send("Message transfer started. This shouldn't take that long.")
    quotesAdded = addQuotesToFile(quotes)
    #adding to file in def addQuotesToFile(quotes)
    await ctx.channel.send(f"Message transfer of {quotesAdded} complete. Check discordQuotes.txt")
    await bot.get_channel(logsID).send(f"{ctx.author.mention} executed .addallquotes")

# ================ OWNER COMMANDS ================

@bot.command(pass_context=True)
@commands.is_owner()
async def setstatus(ctx,mode,msg,presence='online',link='',*args):
    if (len(args) != 0) or (mode.lower() not in ['playing','streaming','listening','watching','clear']) or (link == '' and mode.lower() == 'streaming') or (presence.lower() not in ['online','idle','dnd','offline']):
        await ctx.send('Wrong format! Use: .setstatus playing/streaming/listening/watching "message"/clear online/idle/dnd/offline [url if mode=streaming]')
        return
    clear_activity = False
    if mode.lower() == 'clear':
        clear_activity = True
        set_activity = None
    if not clear_activity:
        finalmsg = msg
        # Setting the activity:
        if mode.lower() == 'playing':
            set_activity = discord.Game(name=str(msg))
        elif mode.lower() == 'streaming':
            set_activity = discord.Streaming(name=str(msg), url=link.lower())
            finalmsg = f'{msg} {str(link)}'
        elif mode.lower() == 'listening':
            set_activity = discord.Activity(type=discord.ActivityType.listening, name=str(msg))
        elif mode.lower() == 'watching':
            set_activity = discord.Activity(type=discord.ActivityType.watching, name=str(msg))
    # Setting the presence:
    if presence.lower() == 'online':
        set_status = discord.Status.online
    elif presence.lower() == 'idle':
        set_status = discord.Status.idle
    elif presence.lower() == 'dnd':
        set_status = discord.Status.dnd
    elif presence.lower() == 'offline':
        set_status = discord.Status.offline

    await bot.change_presence(status=set_status,activity=set_activity)
    await ctx.send(f'Success! New status: {mode[0].upper()}{mode[1:].lower()} {finalmsg}')

@bot.command(pass_context=True)
@commands.is_owner()
async def send(ctx,msg,channelname,*args):
    if len(args) != 0:
        await ctx.send('Wrong format! Use: .send "message" channel_name')
    else:
        guild = bot.get_guild(guildID)
        channel = discord.utils.get(guild.channels, name=channelname)
        channel = guild.get_channel(channel.id)
        await channel.send(msg)

@bot.command(pass_context=True)
@commands.is_owner()
async def getchannels(ctx):
    guild = bot.get_guild(guildID)
    channelsListed = []
    allChannels = guild.channels
    for channel in allChannels:
        if str(channel.type) == "text":
            channelsListed.append(channel.name)
    allChannelsStr = ', '.join(channelsListed)
    await ctx.send(allChannelsStr)

@bot.command(pass_context=True)
@commands.is_owner()
async def getguild(ctx):
    guildid = ctx.message.guild.id
    await ctx.send(guildid)
    
@bot.command(pass_context=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.channel.send("Bot shutting down. Cya!")
    print("Shutdown initiated...")
    quoteBook = bot.get_channel(quoteBookID)
    newestMsg = quoteBook.last_message_id
    print(newestMsg)
    with open (dataPath,"w",encoding="utf-8") as dataFileW:
        dataFileW.write(str(newestMsg))
    time.sleep(2)
    await bot.get_channel(logsID).send("Alphabet Soup Bot now shut down.")
    await bot.close()

@bot.command(pass_context=True)
@commands.is_owner()
async def powershutdown(ctx):
    await bot.close()

@bot.command(pass_context=True)
@commands.is_owner()
async def checkformsg(ctx,channelid: int,msgid: int):
    channel = bot.get_channel(channelid)
    try:
        msg = await channel.fetch_message(msgid)
    except discord.NotFound:
        await ctx.send("Message not found")
    else:
        await ctx.send(f"Message found. Contents: {msg.contents}")

# @bot.command(pass_context=True)
# @commands.is_owner()
# async def mod(ctx,*args):
#     member = args[0]
#     role = bot.get_role(modsID)
#     await bot.add_roles(member,role)

# @bot.command(pass_context=True)
# @commands.is_owner()
# async def demod(ctx,*args):
#     member = args[0]
#     role = bot.get_role(modsID)
#     await bot.add_roles(member,role)



# ████████╗███████╗░██████╗████████╗██╗███╗░░██╗░██████╗░
# ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██║████╗░██║██╔════╝░
# ░░░██║░░░█████╗░░╚█████╗░░░░██║░░░██║██╔██╗██║██║░░██╗░
# ░░░██║░░░██╔══╝░░░╚═══██╗░░░██║░░░██║██║╚████║██║░░╚██╗
# ░░░██║░░░███████╗██████╔╝░░░██║░░░██║██║░╚███║╚██████╔╝
# ░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚═════╝░

@bot.command(pass_context=True)
@commands.is_owner()
async def startconsequences(ctx):
    await ctx.send(f"{ctx.author.mention}, please mention everyone who is playing (you do not have to mention yourself)")
    players = []

    def check(msg, user):
        nonlocal players
        players = msg.content.split(" ")
        allPlayersAreMentions = True
        players.insert(0, ctx.author.mention)
        for player in players:
            if "<@" not in player or ">" not in player:
                allPlayersAreMentions = False
            elif players.count(player) > 1:
                players.remove(player)
        return allPlayersAreMentions and msg.channel == ctx.channel and user == ctx.author
    
    try:
        msg, ctx.author = await bot.wait_for("message", check=check, timeout = 10.0)

    except asyncio.TimeoutError:
        await ctx.send(f"Command expired, {ctx.author.mention} didn't enter a number :(")
    
    else:
        ctx.send(f"Great! We're playing with {len(players)} players.")
        story = ""
        complete = False
        while not complete:
            ctx.send("Alright, let's start the story...")
            ctx.send(f"{players[0]}, begin with the first word. **The game ends when someone enters 'end'.")

            def storyCheck(msg, user):
                if len(msg.content.split(" ")) != 1:
                    ctx.send(f"{user.mention} entered multiple words :(")
                    return False
                return len(msg.content.split(" ")) == 1

            for player in players:
                try:
                    word = await bot.wait_for("message", check=storyCheck, timeout=15.0)
                    if word.lower() == "end":
                        ctx.send(f"Excellent! The final story was: {story}")
                        return
                    story += word
                except asyncio.TimeoutError:
                    ctx.send(f"{player} took too long (>15s) :(")

@bot.command(pass_context=True)
@commands.is_owner()
async def testquotes(ctx):
    with open (quotesPath,"r",encoding="utf-8") as quoteFileR:
        lines = quoteFileR.readlines()
        await ctx.send(f"Lines: {len(lines)}")
        await ctx.send(file=discord.File(quotesPath))

@bot.command(pass_context=True)
@commands.is_owner()
async def repeatmessage(ctx, enabled = "start", interval = 10, message = ""):
    if enabled.lower() == "stop":
        messageInterval.stop()
    elif enabled.lower() == "start":
        messageInterval.change_interval(seconds = int(interval))
        messageInterval.start(ctx,message)

@tasks.loop(seconds = 10)
async def messageInterval(ctx,message):
    await ctx.send(message)

# ================ RUNNING MAIN ================

if __name__ == "__main__":
    asyncio.run(main())
