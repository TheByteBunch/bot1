import discord
from discord.ext import commands
from discord import app_commands


class Ping(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping cog is ready")

    @app_commands.command(name="ping", description="Returns the latency of the bot")
    @app_commands.guilds(1136642484697583667)
    async def ping(self, interactions: discord.Interaction):
        await interactions.response.send_message(f"Pong! {round(self.client.latency * 1000)}ms")


async def setup(client):
    await client.add_cog(Ping(client))
