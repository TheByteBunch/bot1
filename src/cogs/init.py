import discord
from discord.ext import commands
from discord import app_commands


class Init(commands.Cog):

    def __init__(self, client:commands.Bot):
        self.client = client
        self.guild = 1136642484697583667
        self.user_id = 207813174588604418

    @commands.Cog.listener()
    async def on_ready(self):
        print("Init cog ready")

    @commands.command()
    async def sync(self, ctx:commands.Context):
        print("Syncing commands")
        if ctx.author.id == self.user_id:
            synced_commands = await self.client.tree.sync(guild=discord.Object(id=self.guild))
            await ctx.send(f"Synced {len(synced_commands)} commands")
        else:
            await ctx.send("You must be the owner to use this command!")


async def setup(client):
    await client.add_cog(Init(client))
