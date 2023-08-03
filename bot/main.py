from dotenv import load_dotenv, find_dotenv
import discord
import os
# from features import roles, tables
# from utils import my_util

# This example requires the 'message_content' intent.

load_dotenv(find_dotenv())


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os. getenv('DISCORD_TOKEN'))
