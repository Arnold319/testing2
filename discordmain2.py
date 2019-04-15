import extralives, random, discord, pickle
import asyncio

TOKEN = 'NDYzNDIyNTA5MDE1MTA1NTU2.DhwMuA.Yh6KhbiMdeZ_TtF8UFZnt7qYlmY'

client = discord.Client()

@client.event
async def on_message(message):
    global auth
    # we do not want the bot to reply to itself

    if message.author == client.user:
        return
    
    
    limited = True
    for validrole in ("admin", "contributor", "donator"):
        if validrole in [y.name.lower() for y in message.author.roles]:
            limited = False
            break
        elif "lifepass " in [y.name.lower() for y in message.author.roles]:
            limited = False
    
    if message.content.startswith("+limit"):
        for validrole in ("admin", "contributor", "donator"):
            if validrole in [y.name.lower() for y in message.author.roles]:
                await client.send_message(message.channel, "You are a %s, you have infinite uses of this bot" % validrole)
                break
            elif "lifepass " in [y.name.lower() for y in message.author.roles]:
                await client.send_message(message.channel, "You have a %s, so you have infinite uses of this bot" % validrole)
        else:
            await client.send_message(message.channel, "You are not an admin, contributor or donator (or have a lifepass) so you have 1 use per day of this bot")

        
    if message.content.lower() == "+status":
        msg = 'The Bot Is Currently Active'
        await client.send_message(message.channel, msg)
    elif message.content.lower() == "+help":
        helpmsg = """
Bot made by @CaffieneAddict420 
-------------------------------
Usage:
-------------------------------
*+status* (Check if the bot is active)
*+help* (Show this message)
*+queue* (Shows how many lives are queued to be added)
-------------------------------
*+life [phone number]*
*+verify [code] [referal code]*
-------------------------------
        """
        await client.send_message(message.channel, helpmsg)
    
    elif message.content.lower() == "+queue":
        bearers = pickle.load(open("/root/bearers.p", "rb"))
        await client.send_message(message.channel, "There are %s lives queued to be added next US game" % str(len(bearers)))
    elif message.content.startswith('+life'):
        if limited == False:
            lifeargs = message.content.split(" ")
            if len(lifeargs) != 2:
                await client.send_message(message.channel, "Invalid no. of args\n See +help for usage")
            else:
                try:
                     auth = str(extralives.verify(lifeargs[1]))
                     await client.send_message(message.channel, "Code Sent. Check your messages")
                except:
                    await client.send_message(message.channel, "Invalid Phone Number. Example of valid phone number: +14242196850")
        else:
            await client.send_message(message.channel, "Unfortunately, we cannot create a life for you, as you don't have the correct perms yet\nYou need to be either an admin, contributor, donator, or have a lifepass currently\n\nIn the future, users of all roles will be able to use the bot once per day")
    elif message.content.startswith('+verify'):
        verifyargs = message.content.split(" ")
        if len(verifyargs) != 3:
            await client.send_message(message.channel, "Invalid no. of args\n See +help for usage")
        else:
            if auth == "":
                await client.send_message(message.channel, "You need to do +life [number] first")
            else:
                u = "False"
                while u == "False":
                    uname = str(random.randint(1000, 100000))
                    u = str(extralives.username_available(uname))
                try:
                    if str(extralives.submit_code(auth, int(verifyargs[1]))) == "True":
                        try:
                            auth = extralives.create_user(uname, auth, verifyargs[2], "US")['authToken']
                            bearers = pickle.load(open("/root/bearers.p", "rb"))
                            bearers.append(str(auth))
                            pickle.dump(bearers, open("/root/bearers.p", "wb"))
                            await client.send_message(message.channel, "Life is Queued For Creation During Next US Game")

                        except Exception as e:
                            await client.send_message(message.channel, "Uh oh. The an error has occured server-side " + str(e))
                    else:
                        await client.send_message(message.channel, "Invalid Code")
                except:
                    await client.send_message(message.channel, "Invalid Code -  It needs to be a number e.g. 1234")
     
@client.event
async def on_ready():
    global auth
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    auth = ""

client.run ('NTU5OTA5MjU2MDk5MjY2NTYw.XLSvMQ.XNylJKkwcav4fn-rLStDGZQG2hA')

