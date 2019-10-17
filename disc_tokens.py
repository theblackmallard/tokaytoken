# tokens
import discord
import token_rpc
import json

# connects to discord
client = discord.Client()

# connects to komodod
chain = "RICK"
rpc = token_rpc.def_credentials(chain)

# runs on startup
@client.event
async def on_ready():
    print("{0.user} has logged in!".format(client))  

# make sure bot doesn't respond to itself
@client.event
async def on_message(message):
    if message.author == client.user:  
        return

# Help message, shows available commands, not admin commands
    if message.content.startswith("!help"):
        await message.channel.send("""
```
THIS IS TESTING ONLY, PLEASE DON'T SEND KMD TO THESE ADDRESSES
!help returns this message
!topoff returns this wallet address, please send RICK to it if it runs low
!tokencreate,<Token Name>,<Supply>,<Data> creates a token
!tokeninfo <tokenID> shows information for that tokenID
!tokenlist shows all tokenIDs available for this chain
!getblockcount returns the current blockcount Komodod is synced to
```
""")

# creates a token. Probably a cleaner way to split this while allow data to be customized
    if message.content.startswith("!tokencreate,"):
        try:
            name = message.content.split(',')[1]
            supply = message.content.split(',')[2].strip()
            data = message.content.split(',')[3]
            supply = int(supply) / 100000000
            jname = json.dumps(name)
            jsupply =  json.dumps(supply)
            jdata = json.dumps(data)
            tokenid = token_rpc.tokenCreate(rpc, jname, jsupply, jdata)
            await message.channel.send("Your tokenID is {0}".format(tokenid))
        except:
            await message.channel.send("error with creating tokens... Sorry")

# Returns token list
    if message.content.startswith("!tokenlist"):
        result = token_rpc.tokenList(rpc)
        await message.channel.send("{0}".format(result))

# Returns wallet address (assuming you only have the one) this needs to account for different wallets
    if message.content.startswith("!topoff"):
        address, balance = token_rpc.listaddressgroupings(rpc)
        await message.channel.send("The Token pool address: {0}"
                                   " has a balance of {1}".format(address, balance))

# Returns information about a particular tokenID
    if message.content.startswith("!tokeninfo "):
        tokenid = message.content.split()[1]
        result = token_rpc.tokenInfo(rpc, tokenid)
        await message.channel.send("{0}".format(result))

# Returns current block count
    if message.content.startswith("!getblockcount"):
        blockcount = token_rpc.getblockcount(rpc)
        await message.channel.send("Current Block number is {}".format(blockcount))

# ADMIN STUFF #
# shutsdown the bot
    if message.content.startswith("!close"):
        if message.author.id == <Insert Your DiscordID>:
            await client.close()
        else:
            await message.channel.send("I'm sorry Dave, I'm afraid I can't do that.")
            return

# Returns your unique discordID
    if message.content.startswith("!author"):
        await message.channel.send(message.author.id)

# Sets pubkey, needed for CC's. Only use if you don't set pubkey on startup params
    if message.content.startswith("!setpubkey "):
        if message.author.id == <Insert Your DiscordID>:
            pubkey = message.content.split(' ')[1]
            result = token_rpc.setpubkey(rpc, pubkey)
            await message.channel.send(result)
        else:
            await message.channel.send("NO!")

# discord bot token
client.run("<Insert discord bot token here>")  
