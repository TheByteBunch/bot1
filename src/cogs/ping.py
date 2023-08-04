import discord
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser


def get_guild_id():
    config = ConfigParser()
    config.read("../config.ini")
    return int(config["DEV"]["Guild_id"])


class Ping(commands.Cog):
    # Config
    guild_id = get_guild_id()

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping cog is ready")

    @app_commands.command(name="ping", description="Returns the latency of the bot")
    @app_commands.guilds(guild_id)
    async def ping(self, interactions: discord.Interaction):
        await interactions.response.send_message(f"Pong! {round(self.client.latency * 1000)}ms")


async def setup(client):
    await client.add_cog(Ping(client))
