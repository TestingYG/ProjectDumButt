import discord
from discord.ext import commands
import urllib.parse, urllib.request
import re

bot = commands.Bot(description = "Im just a Kid", command_prefix="!")

headers = {}
urllist = []
tf = True

def productSearch(urllist, userinput):
    req1 = urllib.request.Request('https://' + urllist[userinput], headers=headers)
    resp1 = urllib.request.urlopen(req1)
    respdata1 = str(resp1.read())

    sizelist =re.findall('data-size=(.*?)data-stock',respdata1)

    for x in range(len(sizelist)):
        sizelist[x] = re.sub("data-price=", '', sizelist[x])

    return (sizelist)


@bot.event
async def on_ready():
    print("IM READYYY")

@bot.command(pass_context = True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=int(amount)+1):
        messages.append(message)

    await channel.delete_messages(messages)

@bot.command()
async def search(ctx, *, string):

    if string[-1] == ' ':
        string = string[:-1]

    new = re.sub('[\s]', "%20", string)

    url = 'https://www.stadiumgoods.com/catalogsearch/result/?q=' + new
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"

    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    respdata= str(resp.read())

    itemprop = re.findall('a (itemprop="url" .*?") title', respdata)

    for x in range(len(itemprop)):
        url = str(re.findall('https://(.*?")', itemprop[x]))
        urllist.append(url[2:-3])


    if len(itemprop)> 5 or len(itemprop) == 0:
        await ctx.send("{.mention} Be more specific with your search".format(ctx.author))
    else:
        if len(itemprop) > 1:
            for x in range(len(urllist)):
                new = urllist[x][21:-1]
                new = re.sub("-", " ", new)
                print("{}) {}".format(x, new))

            await ctx.author.send('''Please Choose One{} Please Enter a number'''.format(urllist))
            await ctx.send (productSearch(urllist, userinput))
            urllist.clear()

        else:
            await ctx.send (productSearch(urllist, 0))
            urllist.clear()

bot.run("Enter Discord BOT KEY HERE")
