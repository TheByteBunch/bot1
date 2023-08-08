import asyncio
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from utils import basic_utils

this_file_path = os.path.dirname(__file__)
repo_root_dir_path = str(Path(this_file_path).resolve().parents[0])

handler = logging.FileHandler(
    filename=os.sep.join([repo_root_dir_path, "discord.log"]),
    encoding="utf-8",
    mode="a",
)

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


async def load_cogs() -> None:
    """
    Loads all the cogs in the cogs folder
    :return: None
    """
    # Getting feature flags
    feature_flags = basic_utils.parse_feature_flags()

    print("#" * 50)
    print("[INFO] Loading cogs")
    # Looping through all the files in the cogs folder
    cogs_dir = os.sep.join([this_file_path, "cogs"])
    for filename in os.listdir(cogs_dir):
        if filename.startswith("__"):
            continue
        # Check if the file is a python file
        elif filename.endswith(".py"):
            # Get the name of the file
            feature_file_name = filename[:-3]
            # Check if the feature flag is set to 0 if so skip the file
            if (
                feature_file_name in feature_flags
                and feature_flags[feature_file_name] == "0"
            ):
                print(f"Skipping {filename}")
                continue
            # Load the cog
            await client.load_extension(f"cogs.{feature_file_name}")
            print(f"Loaded {filename}")
    print("#" * 50)


async def main():
    async with client:
        # Load all the cogs
        await load_cogs()
        # Start the bot
        discord.utils.setup_logging(handler=handler)
        await client.start(basic_utils.get_secret_token())


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Exiting")
except RuntimeError as e:
    print("Runtime Error:")
    print(e)
