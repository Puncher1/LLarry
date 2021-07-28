import discord
from discord.ext import commands
import coc

import os
import time
from dotenv import load_dotenv
# end imports


# Discord Bot setup
load_dotenv()

intents = discord.Intents.all()
coc_client = coc.login(os.getenv("COC_MAIL"), os.getenv("COC_PW"))

class LLarry(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coc_client = coc_client


client = LLarry(command_prefix="-", case_insensitive=True, intents=intents)
client.activity = discord.Activity(name="lightnings ⚡️", type=discord.ActivityType.watching)

start = time.perf_counter()

# Event: OnReady
@client.event
async def on_ready():
    end = time.perf_counter()
    duration = round(end - start / 1000, 2)
    print(f"[MAIN] Ready! [Duration: {duration}s]")


# Event: OnConnect
@client.event
async def on_connect():
    print(f"[MAIN] Connected to Discord.")


# Loading cogs
cog_count = 0
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cog_count += 1

if not os.listdir('./cogs'):
    print(f'[MAIN] {cog_count} cogs loaded.')

else:
    print(f'[MAIN] {cog_count} cogs loaded.')


print("[MAIN] Boot up...")
print("[MAIN] Connecting to Discord...")
client.run(os.getenv("DISCORD_TOKEN"))