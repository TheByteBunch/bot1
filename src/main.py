import os
from dotenv import load_dotenv, find_dotenv

import asyncio

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
# from cogs.code_question import get_random_line

load_dotenv(find_dotenv())
discord_token = os.getenv('DISCORD_TOKEN')
assert discord_token != '', "DISCORD_TOKEN should be in the environment"


intents = discord.Intents.default()
intents.message_content = True
bot = Bot(
    command_prefix=commands.when_mentioned_or("$$$"),
    intents=intents,
    help_command=None,
)

#
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$code'):
#         await message.channel.send(f"I'm going to fetch a random line of code from one of our repositories. "
#                                    f"Will you be able to guess what it is?")
#         await message.channel.send(f"Code: \n{get_random_line()}")
#
#
# client.run(os. getenv('DISCORD_TOKEN'))


async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

asyncio.run(load_cogs())
bot.run(discord_token)
