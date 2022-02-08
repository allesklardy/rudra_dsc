from logging import exception
import requests
import discord
import sqlite3

file = open("token.conf")
tokendisi = file.read()
api_url = "https://api.corona-zahlen.org/districts/"
heeelp = "I'm here to show you the current 7-day incidence of the specified city\n\nExample: '.corona München'. It's also possible to only write a part of the name.\nThe color coded map can be viewed via .map\n\ngithub @allesklardy"

def search(stadt):
    r = requests.get(api_url)
    json = r.json()
    ret = ""
    stadt = "%" + stadt + "%"
    con = sqlite3.connect("ags.sqlite")
    cur = con.cursor()
    suche = "SELECT ags FROM ags_name WHERE name like '" + stadt + "'"
    cur.execute(suche)
    limit = 1
    res = cur.fetchall()
    for i in res:
        for k in i:
            if limit <= 10:
                inzi = json["data"][str(k)]["weekIncidence"]
                stadtname = json["data"][str(k)]["county"]
                meta = json["meta"]["lastUpdate"]
                ausgabe = stadtname + " has a 7-day incidence of: " + str(round(inzi)) + " --- timestamp: " + str(meta)[:10]
                ret = ret + ausgabe + "\n"
                limit = limit + 1
    return(ret)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('--- Ready to receive commands ---')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.casefold().startswith('.map'):
        print("[EVENT] User entered " + message.content)
        await message.channel.send("https://api.corona-zahlen.org/map/districts")
        await message.channel.send("Color legend may differ from other maps.")

    if message.content.casefold().startswith('.help'):
        nachricht = heeelp
        print("[EVENT] User entered " + message.content + " output:" + nachricht)
        await message.channel.send(nachricht)

    if message.content.casefold().startswith('.corona'):
        inhalt = message.content[8:]
        if inhalt == "":
            await message.channel.send(heeelp)
        else: 
            try:
                nachricht = str(search(inhalt))
            except:
                nachricht = "The api seems to be not available... Try again later"
            print("[EVENT] User entered " + message.content + " output:" + nachricht)
            if nachricht != "":
                await message.channel.send(nachricht)
            else:
                await message.channel.send("Sry, nicht verfügbar.")


try:
    client.run(tokendisi)
except:
    print(exception)
    print("Discord hatte einen Fehler!!1")