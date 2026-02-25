import discord
import requests
import asyncio
import os

# Get API keys and variables from Railway environment
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Multiple players separated by commas in Railway variable USERNAMES
USERNAMES = os.getenv("USERNAMES").split(",")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Store last login for each player
last_login_saved = {}

async def check_players():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while True:
        for USERNAME in USERNAMES:
            USERNAME = USERNAME.strip()  # remove extra spaces

            # Get UUID from Mojang API
            uuid_req = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{USERNAME}")
            if uuid_req.status_code != 200:
                continue  # skip if username not found
            uuid = uuid_req.json()["id"]

            # Get Hypixel player data
            url = f"https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}"
            response = requests.get(url).json()

            if response.get("success") and "player" in response and response["player"]:
                last_login = response["player"].get("lastLogin")

                if USERNAME not in last_login_saved:
                    last_login_saved[USERNAME] = last_login

                elif last_login != last_login_saved[USERNAME]:
                    last_login_saved[USERNAME] = last_login
                    # Send message in Discord
                    await channel.send(f"🚨 {USERNAME} just logged in on Hypixel!")

        await asyncio.sleep(300)  # check every 5 minutes

@client.event
async def on_ready():
    print("Bot is online!")

client.loop.create_task(check_players())
client.run(DISCORD_TOKEN)
