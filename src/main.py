import os
import asyncio
import discord
from discord.ext import commands

# Importing utils
import utils.basic as basic

# Define intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

# Define client
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready():
    print("Bot is ready")


async def load() -> None:
    """
    Loads all the cogs in the cogs folder
    :return: None
    """
    print("#" * 50)
    print(f"[INFO] Loading cogs")
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename}")
    print("#" * 50)


async def main():
    async with client:
        # Load all the cogs
        await load()
        # Start the bot
        await client.start(basic.get_secret_token())


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exiting")
except RuntimeError as e:
    print(e)
    print("Bot did not start properly")
