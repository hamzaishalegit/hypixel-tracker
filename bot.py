import discord
import asyncio
from mcstatus import JavaServer
import os

# Discord / server settings
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Players to track
USERNAMES = os.getenv("USERNAMES").split(",")  # e.g., "zonqued,SimpDePyke"

# Minecraft server
SERVER_ADDRESS = "mc.hypixel.net"  # Hypixel main server

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Keep track of online state
online_status = {player.strip(): False for player in USERNAMES}

async def check_players():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    server = JavaServer.lookup(SERVER_ADDRESS)

    while True:
        try:
            status = server.status()
            online_sample = []
            if status.players.sample:
                online_sample = [p.name for p in status.players.sample]

            for player in USERNAMES:
                player = player.strip()
                currently_online = player in online_sample

                # Player just came online
                if currently_online and not online_status[player]:
                    online_status[player] = True
                    await channel.send(f"🚨 {player} is ONLINE on Hypixel!")

                # Player just went offline
                elif not currently_online and online_status[player]:
                    online_status[player] = False
                    await channel.send(f"⚡ {player} went OFFLINE on Hypixel!")

        except Exception as e:
            print(f"Error checking server: {e}")

        await asyncio.sleep(60)  # check every 60 seconds

@client.event
async def on_ready():
    print("Bot is online!")

client.loop.create_task(check_players())
client.run(DISCORD_TOKEN)
