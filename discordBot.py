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

# ================ LIBRARIES ================
import asyncio
import random
import time
import discord
from discord.ext import tasks, commands

# ================ VARIABLES ================
TOKEN = ""
console = [482934173032775683] #Kisakot
quoteBookID = 0 #quote-book
logsID = 0 #asb-logs
ultralogsID = 0 #asb-ultralogs (Bot Testing server)
modsID = 0 #mods role
guildID = 0 #server/guild ID
bdaysPath = r""
dataPath = r""
quotesPath = r""

# ================ INITIALISING ================

intents = discord.Intents.default()
intents.message_content = True

async def main():
    async with bot:
        bot.loop.create_task(checkForNewQuotes())
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

async def checkForNewQuotes():
    await bot.wait_until_ready()
    quoteBook = bot.get_channel(quoteBookID)
    newestMsgID = quoteBook.last_message_id
    with open (dataPath,"r",encoding="utf-8") as dataFileR:
        prevMsgID = int(dataFileR.readline())
        if prevMsgID != newestMsgID:
            msgCount = 0
            async for msg in quoteBook.history():
                msgID = msg.id
                if msgID == prevMsgID:
                    break
                msgCount += 1
            newQuotes = [msg async for msg in quoteBook.history(limit=msgCount)]
            with open(quotesPath,"r",encoding="utf-8") as quoteFileR:
                oldQuoteCount = len(quoteFileR.readlines())
            newQuoteCount = addQuotesToFile(newQuotes)
            logs = bot.get_channel(logsID)
            await logs.send(f"{msgCount} new messages detected in <#{quoteBookID}>.")
            await logs.send(f"Added {newQuoteCount-oldQuoteCount} quotes to discordQuotes.txt. New length = {len(newQuoteCount)}")

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
async def addquotes(ctx,*args):
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
            quotesAdded = addQuotesToFile(quotes) #adding to file in def addQuotesToFile(quotes)
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

# ================ OWNER COMMANDS ================

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
            print(channel)
            channelsListed.append(channel)
    await ctx.send(f"{', '.join(channelsListed)}")

@bot.command(pass_context=True)
@commands.is_owner()
async def getguild(ctx):
    guildid = ctx.message.guild.id
    ctx.send(guildid)
    
@bot.command(pass_context=True)
@commands.is_owner()
async def shutdown(ctx):
    quoteBook = bot.get_channel(quoteBookID)
    newestMsg = quoteBook.last_message_id
    with open (dataPath,"w",encoding="utf-8") as dataFileW:
        dataFileW.write(str(newestMsg))
    await ctx.channel.send("Bot shutting down. Cya!")
    time.sleep(3)
    await bot.get_channel(logsID).send("Alphabet Soup Bot now shut down.")
    await bot.close()

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
async def testquotes(ctx):
    with open (quotesPath,"r",encoding="utf-8") as quoteFileR:
        lines = quoteFileR.readlines()
        print(len(lines))
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
