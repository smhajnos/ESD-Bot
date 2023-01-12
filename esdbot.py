# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 06:41:12 2023

@author: sam
"""


import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
import esdbotsecrets
from geopy import Nominatim
import requests
import datetime




admin_server = 756535565612220557
cassowary_server = 1062371995020435509
#cassowary_server = admin_server
logs_channel = 1014726103543324672
esd_color = 0xffe100
esd_channel = 1062371995989311489 #general
#esd_channel = logs_channel
staff_channel = logs_channel
phil_channel = esd_channel


intents = nextcord.Intents.all()
#intents.members = True

bot = commands.Bot(command_prefix='}', intents=intents)

async def staff_command(ctx):
    ctx.channel.id = staff_channel
    
@bot.slash_command(name="ping",description="Check if the bot is working", guild_ids=[cassowary_server, admin_server])
async def ping(ctx):
    await ctx.send("Pong!")
    
@bot.slash_command(name="force",description="Force an ESD report", guild_ids=[admin_server])
async def force(ctx):
    await esdcheck(True)
    await ctx.senx("Done!")
      

async def log(s):
    lc = bot.get_channel(logs_channel)
    await lc.send(s)
    
    
    

@tasks.loop(seconds=60)
async def timedevents():
    await esdcheck()
    await philcheck()
    
def esdrisk(query):
    gl = Nominatim(user_agent="ESDBot")
    location = gl.geocode(query)
    url = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&appid={}".format(location.latitude,location.longitude,esdbotsecrets.OWM_KEY)
    print(url)
    response = requests.get(url)
    print(response.json())
    hum = response.json()["current"]["humidity"]
    if hum >= 30:
        return "The humidity is {}%. The ESD risk is low. Go ahead and rub your feet on the carpet.".format(hum)
    else:
        return "The humidity is {}%. The ESD risk is high. Use ESD precautions!".format(hum)
    
    
async def esdcheck(forced=False):
    esdday = datetime.datetime(2023,1,9,7,0,0,0)
    today = datetime.datetime.now()
    delta = today - esdday
    esddays = delta.days
    print("Days since last esd: {}".format(esddays))
    with open("lastesdcheck.txt","r") as esdfile:
        try:
            lastesddays = int(esdfile.read())
        except:
            lastesddays = 0
    if (lastesddays < esddays) or forced:
        risk = esdrisk("Eldersburg, MD")
        chan = bot.get_channel(esd_channel)
        await chan.send(risk)
        with open("lastesdcheck.txt","w") as esdfile:
            esdfile.write(str(esddays))
            

async def philcheck():
    philday = datetime.datetime(2023,1,27,9,0,0,0)
    today = datetime.datetime.now()
    delta = today - philday
    phildays = delta.days
    print("Days since Phil left: {}".format(phildays))
    if phildays < 0 :
        s = "Phil leaves in {} days.".format(-phildays)
    elif phildays == 0:
        s = "Phil leaves today!"
    else:
        s = "Phil left {} days ago".format(phildays)
    
    with open("lastphilcheck.txt","r") as philfile:
        try:
            lastphildays = int(philfile.read())
        except:
            lastphildays = -99999
    if lastphildays < phildays:
        chan = bot.get_channel(phil_channel)
        await chan.send(s)
        with open("lastphilcheck.txt","w") as philfile:
            philfile.write(str(phildays))
            


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}') 
    main_channel = bot.get_channel(logs_channel)
    await main_channel.send("Starting")
    
    #start timers
    if not timedevents.is_running():
        timedevents.start()
        




print("Starting bot")
bot.run(esdbotsecrets.DISCORD_TOKEN)