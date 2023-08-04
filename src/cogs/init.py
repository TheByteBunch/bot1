import discord
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser

def get_guild_id():
    config = ConfigParser()
    config.read("../config.ini")
    return int(config["DEV"]["Guild_id"])

def get_user_id():
    config = ConfigParser()
    config.read("../config.ini")
    return int(config["DEV"]["User_id"])


class Init(commands.Cog):
    # Hardcoded values
    guild = get_guild_id()
    user_id = get_user_id()

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Init cog ready")

    @commands.command()
    async def sync(self, ctx: commands.Context):
        print("Syncing commands")
        if ctx.author.id == self.user_id:
            synced_commands = await self.client.tree.sync(guild=discord.Object(id=self.guild))
            await ctx.send(f"Synced {len(synced_commands)} commands", ephemeral=True)
        else:
            await ctx.send("You must be the owner to use this command!", ephemeral=True)


async def setup(client):
    await client.add_cog(Init(client))
