import discord
from discord.ext import commands
import urllib.parse, urllib.request
import requests
import googlesearch
import re
import json

bot = commands.Bot(description = "Im just a Kid", command_prefix ="@")

@bot.event
async def on_ready():
    print("IM READYYY")

@bot.command(pass_context=True)
async def search(ctx, *args):

    sites = [" Stadium Goods"]
    urllist = []
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"


    await ctx.send("working on your request")

    #SX
    keywords = ''
    for word in args:
        keywords += word + '%20'

    json_string = json.dumps({"params": f"query={keywords}&hitsPerPage=20&facets=*"})
    byte_payload = bytes(json_string, 'utf-8')
    algolia = {"x-algolia-agent": "Algolia for vanilla JavaScript 3.32.0", "x-algolia-application-id": "XW7SBCT9V6", "x-algolia-api-key": "6bfb5abee4dcd8cea8f0ca1ca085c2b3"}

    with requests.Session() as session:
        r = session.post("https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query", params=algolia, verify=False, data=byte_payload, timeout=30)
        results = r.json()["hits"][0]
        apiurl = f"https://stockx.com/api/products/{results['url']}?includes=market,360&currency=USD"

        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,la;q=0.6',
            'appos': 'web',
            'appversion': '0.1',
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

        response = requests.get(apiurl, verify=False, headers=header)
        prices = response.json()
        general = prices['Product']
        market = prices['Product']['market']
        sizes = prices['Product']['children']

        embed = discord.Embed(title='StockX', color=0x43dd36)
        embed.set_thumbnail(url=results['thumbnail_url'])

        embed.add_field(name=general['title'], value='https://stockx.com/' + general['urlKey'], inline=False)
        embed.add_field(name='SKU/PID:', value=general['styleId'], inline=True)
        embed.add_field(name='Colorway:', value=general['colorway'], inline=True)
        embed.add_field(name='Retail Price:', value=f"${general['retailPrice']}", inline=False)

        for size in sizes:
            if len(sizes[size]['market']) != 0:
                if (sizes[size]['market']['lowestAsk'] != 0 and sizes[size]['market']['highestBid'] != 0):
                    embed.add_field(name = f"Size: {sizes[size]['shoeSize']}", value=f"Low Ask: $ {sizes[size]['market']['lowestAsk']}\n High Bid: $ {sizes[size]['market']['highestBid']}", inline=True)

        embed.set_footer(text='GitHub: TestingYG', icon_url ="https://image.shutterstock.com/image-photo/cute-little-chicken-isolated-on-260nw-520818805.jpg")

    sku = general['styleId']

    for x in sites:
        for i in (googlesearch.search(sku+x ,tld='co.in',lang='en',num=10,stop=1,pause=2)):
            urllist.append(str(i))

    #SG
    req = urllib.request.Request(urllist[0], headers=headers)
    resp = urllib.request.urlopen(req)
    respdata = str(resp.read())

    find = re.findall('"sizeLabel":.*?."f', respdata)
    find = ''.join(find)

    size = re.findall('"sizeLabel".*?,', find)
    size = ''.join(size)
    size = re.sub('sizeLabel":"', "", size)
    size = re.sub('"', "", size)
    size = size[:-1]
    size = size.split(",")

    price = re.findall('"price":.*?"f', find)
    price = ''.join(price)
    price = re.sub('"f', "", price)
    price = re.sub('"price":', " ", price)
    price = re.sub(", ", " ", price)
    price = price[:-1]
    price = re.sub('"', "", price)
    price = re.sub('null', '0', price)
    price = price.split(" ")
    price = price[1:]

    StadiumGoods = dict(zip(size, price))

    embedSG = discord.Embed(title='Stadium Goods', color=0xd1d8d0)
    embedSG.set_thumbnail(url=results['thumbnail_url'])

    embedSG.add_field(name=general['title'], value= urllist[0], inline=False)
    embedSG.add_field(name='SKU/PID:', value=general['styleId'], inline=True)
    embedSG.add_field(name='Colorway:', value=general['colorway'], inline=True)
    embedSG.add_field(name='Retail Price:', value=f"${general['retailPrice']}", inline=False)

    for k,v in StadiumGoods.items():
        if v != '0':
            embedSG.add_field(name=f'Size: {k}', value= f"$ {v}", inline=True)

    embedSG.set_footer(text='GitHub: TestingYG', icon_url ="https://image.shutterstock.com/image-photo/cute-little-chicken-isolated-on-260nw-520818805.jpg")


    #GOAT

    keywords = f"{general['styleId']}%20"

    json_string = json.dumps({"params": f"facets=%2A&hitsPerPage=20&query={keywords}"})
    byte_payload = bytes(json_string, 'utf-8')
    algolia = {"x-algolia-agent": "Algolia for vanilla JavaScript 3.32.0", "x-algolia-application-id": "2FWOTDVM2O", "x-algolia-api-key": "ac96de6fef0e02bb95d433d8d5c7038a"}

    with requests.Session() as session:
        r = session.post("https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query", params=algolia, verify=False, data=byte_payload, timeout=30)
        results1 = r.json()["hits"][0]
        apiurl = f"https://www.goat.com/web-api/v1/product_variants?productTemplateId={results1['slug']}"
        url = f"https://www.goat.com/sneakers/{results1['slug']}/available-sizes"
        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,la;q=0.6',
            'appos': 'web',
            'appversion': '0.1',
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

        response = requests.get(apiurl, verify=False, headers=header)
        prices = response.json()

        dic = {}

        for x in range(len(prices)):
            if (prices[x]["shoeCondition"] == "new_no_defects" and prices[x]["boxCondition"] == "good_condition"):
                reduce = prices[x]["lowestPriceCents"]["amount"] / 100
                dic[prices[x]["size"]] = int(reduce)


        embedG = discord.Embed(title='Goat', color=0x000000)
        embedG.set_thumbnail(url=results['thumbnail_url'])

        embedG.add_field(name=general['title'], value= url, inline=False)
        embedG.add_field(name='SKU/PID:', value=general['styleId'], inline=True)
        embedG.add_field(name='Colorway:', value=general['colorway'], inline=True)
        embedG.add_field(name='Retail Price:', value=f"${general['retailPrice']}", inline=False)

        if len(dic) != 0:
            for k,v in dic.items():
                embedG.add_field(name = f"Size: {k}", value=f"$ {v}", inline=True)


        embedG.set_footer(text='GitHub: TestingYG', icon_url ="https://image.shutterstock.com/image-photo/cute-little-chicken-isolated-on-260nw-520818805.jpg")

    await ctx.send(embed=embed)
    await ctx.send(embed=embedSG)
    await ctx.send(embed=embedG)


bot.run("")
