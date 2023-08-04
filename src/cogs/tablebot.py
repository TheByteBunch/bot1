import discord
from discord.ext import commands
from discord import app_commands
from table2ascii import table2ascii as t2a, PresetStyle
from configparser import ConfigParser


def get_guild_id():
    config = ConfigParser()
    config.read("../config.ini")
    return int(config["DEV"]["Guild_id"])


class Tablebot(commands.Cog):
    # Config
    guild_id = get_guild_id()

    # Variables
    table_info = {
        "headers": [],
        "body": []
    }

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Tablebot cog is ready")

    @app_commands.command(name="add_header", description="Add header to table")
    @app_commands.guilds(guild_id)
    async def add_header(self, interaction: discord.Interaction, header: str):
        """
        Add a header to the table
        :param interaction:
        :param header:
        :return:
        """
        # Add header
        self.table_info["headers"].append(header)

        # Send response
        await interaction.response.send_message(f"Added header {header}", ephemeral=True)

    @app_commands.command(name="add_body", description="Add body to table")
    @app_commands.guilds(guild_id)
    async def add_body(self, interaction: discord.Interaction, body: str):
        """
        Add a body to the table
        :param interaction:
        :param body:
        :return:
        """
        # Parse body items
        body_items = body.split(",")

        # Check that the body items are the same length as the headers
        if len(body_items) != len(self.table_info["headers"]):
            await interaction.response.send_message("Body items must be the same length as the headers", ephemeral=True)
            return

        # Add body
        for item in body_items:
            self.table_info["body"].append(item)

        # Send response
        await interaction.response.send_message(f"Added body {body}", ephemeral=True)

    @app_commands.command(name="create_member_table", description="Creates a new member table")
    @app_commands.guilds(guild_id)
    async def create_member_table(self, interaction: discord.Interaction):
        """
        Creates a new member table
        :param interaction:
        :return:
        """
        # Make Header and body
        header = ["Name", "Local Time(24h)", "Projects"]
        body = [
            ["Alibaba", "13:00", "Project 1, Project 2"],
            ["Erik", "07:00", "Project 1, Project 2, Project 3"],
        ]

        # Make table
        output = t2a(header, body, style=PresetStyle.ascii_compact)

        # Send response
        await interaction.response.send_message(f"```\n{output}\n```")


async def setup(client):
    await client.add_cog(Tablebot(client))
