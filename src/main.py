import os
import asyncio
import discord
from discord.ext import commands
from configparser import ConfigParser

# Importing utils
import utils.basic as basic

# Define intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

# Define client
client = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready():
    print("Bot is ready")


def parse_feature_flags():
    """
    Parse feature flags from the config.ini file
    :return:
    """
    # Create config parser
    config = ConfigParser()
    # Read the config file
    config.read("../config.ini")
    # Get the feature flags
    feature_flags = config["FEATURE_FLAGS"]

    # Return the feature flags
    return feature_flags


async def load() -> None:
    """
    Loads all the cogs in the cogs folder
    :return: None
    """
    # Getting feature flags
    feature_flags = parse_feature_flags()

    print("#" * 50)
    print(f"[INFO] Loading cogs")
    # Looping through all the files in the cogs folder
    for filename in os.listdir("cogs"):
        # Check if the file is a python file
        if filename.endswith(".py"):
            # Get the name of the file
            feature_file_name = filename[:-3]
            # Check if the feature flag is set to 0 if so skip the file
            if feature_file_name in feature_flags and feature_flags[feature_file_name] == "0":
                print(f"Skipping {filename}")
                continue
            # Load the cog
            await client.load_extension(f"cogs.{feature_file_name}")
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
