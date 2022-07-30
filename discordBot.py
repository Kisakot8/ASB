# **************** NOTES ****************

# For emoji unicode characters, change + to 000 and place \ in front of it
# For the quotes file always add ,encoding="utf-8" in the brackets ie: ("discordQuotes.txt","r",encoding="utf-8")
# Character Ξ reserved for multi-line quote support (check quote functions)

# ================ LIBRARIES ================
import discord
from discord.ext import tasks, commands
import random
import os #unused (I think)

# ================ VARIABLES ================
TOKEN = ""
console = [482934173032775683] #Kisakot
quoteBookID = 123456789012345678 #quote-book


# ================ INITIALISING ================

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        print("this works")

bot = MyBot(intents = intents, command_prefix=".", owner_ids=set(console))

# ================ CODE ================

def addQuotesToFile(quotes): #needed for .addallquotes and .addquotes
    for qMsg in quotes: #checks if quote is already in the file
        quote = qMsg.content #content of quote
        sender = qMsg.author #person who sent quote
        with open ("discordQuotes.txt","r",encoding="utf-8") as quoteFileR:
            currentQuotes = quoteFileR.readlines()
            if (str(quote) + " - " + str(sender) + "\n") in currentQuotes:
                quotes.pop( quotes.index(qMsg) )

    for qMsg in quotes:
        quote = qMsg.content #content of quote
        sender = qMsg.author #person who sent quote
        if (quote.count("'") >= 2) or (quote.count('"') >= 2) or (("“" in quote) or ("‘" in quote)): #text quote
            if "\n" in quote: #multi-line support
                quote = quote.replace("\n","Ξ") #Ξ = new line symbol for multi-line quotes
            with open ("discordQuotes.txt","a",encoding="utf-8") as quoteFile:
                quoteFile.write(str(quote) + " - " + str(sender))
                quoteFile.write("\n")
            
        elif qMsg.attachments: #attachment (image) quote
            attachment = qMsg.attachments[0]
            attachmentUrl = attachment.url
            with open ("discordQuotes.txt","a",encoding="utf-8") as quoteFile:
                quoteFile.write(str(attachmentUrl) + " " + str(quote) + " - " + str(sender))
                quoteFile.write("\n")

    with open ("discordQuotes.txt","r",encoding="utf-8") as quoteFileR:
        lines = quoteFileR.readlines()
        return len(lines)

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    username = str(message.author).split("#")[0]
    user_tag = str(message.author).split("#")[1]
    user_message = str(message.content)
    channel = str(message.channel.name)

    if message.author == bot.user:
        return
    # HAVE ALL FUNCTIONS NOT INVOLVING THE BOT INTERACTING WITH ITSELF AFTER THIS POINT
    
    print(f"{username}: {user_message} ({channel})")
    
    if user_message.lower() == "cum": #cum message
        await message.channel.send("mmm cum")

    if user_message.lower() == "sneeze": #sneeze message
        await message.channel.send("Bless you!")

#     if user_message.lower() == ".calc": #broken calc function - need to get message ID's - USE CHANNEL HISTORY (but polls alr over :( )
#         print(countOne,countTwo,countThree,countFour)
    
    if user_message.lower() == "cool": #test reaction
        await message.add_reaction("\U0001F60E")
    
    if channel == "quote-book":
        quote = user_message
        sender = message.author
        if (user_message.count("'") >= 2) or (user_message.count('"') >= 2) or ("“" in user_message):
            with open ("discordQuotes.txt","a",encoding="utf-8") as quoteFile: #put utf-8 otherwise it dies
                if "\n" in quote: #multi-line support
                    quote = quote.replace("\n","Ξ") #Ξ = new line symbol for multi-line quotes
                quoteFile.write(str(quote) + " - " + str(sender))
                quoteFile.write("\n")
        elif message.attachments: #attachment (image) quote
            attachment = message.attachments[0]
            attachmentUrl = attachment.url
            with open ("discordQuotes.txt","a",encoding="utf-8") as quoteFile: #put utf-8 otherwise it dies
                quoteFile.write(str(attachmentUrl) + " - " + str(sender))
                quoteFile.write("\n")
    
#     if channel == "birthdays":
#         if user_message.count("/") == 2 and user_message.count(" ") == 1:
#             authorID = message.author.id
#             msgLst = user_message.split(" ")
#             name = msgLst[0]
#             date = msgLst[1]
#             dateLst = date.split("/")
#             day = dateLst[0]
#             month = dateLst[1]
#             year = dateLst[2]
#             if len(day) == 2 and day.isnumeric() and len(month) == 2 and month.isnumeric() and len(year) == 4 and year.isnumeric() and name.isalpha():
#                 with open("discordBdays.txt","a",encoding="utf-8") as bdayFileA:
#                     bdayFileA.write(str(name) + " <@" + str(authorID) + "> " + str(year) + "-" + str(month) + "-" + str(day) + "\n")
#                 
#             else:
#                 await message.channel.send("Wrong format! Please use NAME DD/MM/YYYY")
#                 await message.delete()
#         else:
#             await message.channel.send("Wrong format! Please use NAME DD/MM/YYYY")
#             await message.delete()

# ================ COMMANDS ================

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(pass_context=True)
@commands.has_role("mods")
async def createq(ctx):
    if ctx.channel == "❗teacher-comp❗":
        await ctx.message.delete()
        with open("teacherListDone.txt","r") as doneFileR:
            with open ("teacherList.txt","r") as listFileR:
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
            new_msg = await message.channel.send("""`ROUND """ + str(roundNum+1) + """: """ + title + """ """ + name + """`

**Teaching Ability:** **WORST** :one: :two: :three: :four: **BEST**
**Personality:** **WORST** :red_circle: :orange_circle: :yellow_circle: :green_circle: **BEST**
:bangbang:__Reminder: Only vote if you have experience (either with teaching or personality)__ :bangbang:

<@&990316741093646376> • """ + emoji)
            await new_msg.add_reaction("1️⃣")
            await new_msg.add_reaction("2️⃣")
            await new_msg.add_reaction("3️⃣")
            await new_msg.add_reaction("4️⃣")
            new_msg = await message.channel.send("** **")
            await new_msg.add_reaction("\U0001F534")
            await new_msg.add_reaction("\U0001F7E0")
            await new_msg.add_reaction("\U0001F7E1")
            await new_msg.add_reaction("\U0001F7E2")
    with open("teacherListDone.txt","a") as doneFileA:
        doneFileA.write(teacher)

@bot.command()
async def quote(ctx):
    with open ("discordQuotes.txt","r",encoding="utf-8") as quoteFile: #always put utf-8 for the file
        quotes = quoteFile.readlines()
        quote = random.choice(quotes)
        if "Ξ" in quote:
            quote = quote.replace("Ξ","\n")
        await ctx.send(quote)

@bot.command(pass_context=True)
@commands.has_role("mods")
async def addquotes(ctx,*args):
    if len(args) != 1:
        await message.channel.send("Incorrect arguments! Syntax: .addquotes <number>")
    else:
        quoteAmount = args[0]
        if not quoteAmount.isnumeric():
            await message.channel.send("That's not a number! Syntax: .addquotes <number>")
# actual code for adding quotes beyond this point
        else:
            await message.channel.send("Command recieved, started reading " + str(quoteAmount) + " messages of <#" + str(quoteBookID) + ">. This could take a while.")
            quoteBook = bot.get_channel(quoteBookID)
            quotes = await quoteBook.history(limit=int(quoteAmount)).flatten() #reads quoteAmount number of messages in channel
            await message.channel.send("Message transfer of " + str(quoteAmount) + " messages started. This could take a while.")
            quotesAdded = addQuotesToFile(quotes) #adding to file in def addQuotesToFile(quotes)
            await message.channel.send("Message transfer of " + str(quotesAdded) + " complete. Check discordQuotes.txt")

@bot.command(pass_context=True)
@commands.has_role("mods")
async def addallquotes(ctx):
    await ctx.channel.send("Command recieved, started reading contents of <#" + str(quoteBookID) + ">. This could take a while.")
    quoteBook = bot.get_channel(quoteBookID)
    quotes = await quoteBook.history(limit=None).flatten() #reads everything in channel
    open("discordQuotes.txt","w",encoding="utf-8").close() #clears file
    await ctx.channel.send("Message transfer started. This could take a while.")
    quotesAdded = addQuotesToFile(quotes)
    #adding to file in def addQuotesToFile(quotes)
    await ctx.channel.send("Message transfer of " + str(quotesAdded) + " complete. Check discordQuotes.txt")
    
@bot.command(pass_context=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.channel.send("Bot shutting down. Cya!")
    await bot.close()

# ================ TESTING ================

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

#         if user_message.lower() == ".restart":
#             await message.channel.send("Bot restarting...")
#             await bot.close()
#             import discordBotRestart.py   # dies because "RuntimeError: Cannot close a running event loop"

# @bot.event
# async def on_reaction_add(reaction,user): #test message on reaction
#     await reaction.message.channel.send(f"{user} reacted with {reaction.emoji}")


bot.run(TOKEN)
