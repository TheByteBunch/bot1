import discord
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser
import utils.basic_utils


class Init(commands.Cog):
    # Config
    guild = utils.basic_utils.get_guild_id()
    user_id = utils.basic_utils.get_user_id()

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
