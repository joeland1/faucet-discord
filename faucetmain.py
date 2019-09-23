from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord

#import sqlite3
#from sqlite3 import Error
import os.path
import os
import time

import config

rpc_connection = 'http://{0}:{1}@{2}:{3}'.format(config.rpc_user, config.rpc_password, config.ip, config.rpc_port)

#by joe_land1


client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    #print(message)
    if message.author.bot == True:
        return

    wallet = AuthServiceProxy(rpc_connection)

    if message.content.startswith('//faucet'):

    #test to see if person has ever used faucet
        if os.path.isfile(str(message.author.id)+'.txt')==False:
            f= open(str(message.author.id)+".txt","w+")


            print(message.created_at.timestamp())
            print("message:current")
            print(time.time())
            print('------')

            f.write(str(time.time()))
            f.close

            #get address to send faucet
            toaddress = message.content.split(" ")[1]

            #validate address function
            validatestatus=wallet.validateaddress(toaddress)

            if validatestatus["isvalid"]==True:
                txid = wallet.sendfrom(config.FAUCET_SOURCE,toaddress, config.AMOUNT)
                if len(txid) == 64:
                    await sendmessage(message, txid)
                #await message.channel.send("sent")
            else:
                await message.channel.send("invalid")


        #if person has use faucet before
        else:
            contents = 0 # Initialize this as zero value - we'll add to it to ensure it stays an int
            file_name = "{0}.txt".format(message.author.id)
            with open(file_name, 'r') as f:
                for line in f:
                    try:
                        contents = float(line)
                    except:
                        raise

            print(time.time())
            print("current :minus: past")
            print(contents)
            print('------')

            if time.time()-float(contents)>=86400:
                                #validate address function
                toaddress = message.content.split(" ")[1]
                validatestatus=wallet.validateaddress(toaddress)

                if  validatestatus['isvalid']==True:
                    txid = wallet.sendfrom(config.FAUCET_SOURCE,toaddress, config.AMOUNT)

                    #rewrite file if time diff is greater than 1 day
                    os.remove(str(message.author.id)+".txt")
                    f=open(str(message.author.id)+".txt", "+a")
                    f.write(str(time.time()))
                    f.close()

                    if len(txid) == 64:
                        #await message.channel.send("sent")
                        await sendmessage(message, txid)

                else:
                    await message.channel.send("invalid")

            else:
                await message.channel.send("Too soon, you gotta wait a bit more")
                print("diff is "+str(time.time()-float(contents)))
                return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

async def sendmessage(ctx, txid):
    embed = discord.Embed(
        title="**Block explorer**",
        url='https://1explorer.sugarchain.org/tx/{0}'.format(txid), color=0x0043ff)
    embed.add_field(
        value="Amount sent: "+str(config.AMOUNT),
        name=ctx.content.split(" ")[1])

    await ctx.channel.send(embed=embed)

client.run(config.TOKEN)
