# bot.py
import os
from datetime import datetime
import discord
from dotenv import load_dotenv
from time import sleep

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(guild.channels, name='general')

    while True:
        time = datetime.now()
        await channel.send(f'{time.hour} : {time.minute}')
        sleep(60)


client.run(TOKEN)