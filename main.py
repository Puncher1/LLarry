import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
# end imports

# Discord Bot setup
load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="-", case_insensitive=True, intents=intents)
client.activity = discord.Activity(name="on villages", type=discord.ActivityType.watching)


# Loading cogs
cog_count = 0
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cog_count += 1

if not os.listdir('./cogs'):
    print('Loaded 0 cogs')

else:
    print(f'Loaded {cog_count} cogs')

client.run(os.getenv("DISCORD_TOKEN"))