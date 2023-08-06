"""
Script that will create new python file with default cog structure
"""

import os
import sys


def create_cog_file(cog_name: str) -> None:
    """
    Creates a new cog file with the default structure
    :param cog_name: Name of the cog
    :return: None
    """
    # Create the cog file
    with open(f"../cogs/{cog_name}.py", "w") as cog_file:
        # Write the default structure
        cog_file.write(
            f"""import discord
from discord.ext import commands
from discord import app_commands

import logging

from utils import basic_utils

class {cog_name.capitalize()}(commands.Cog):

    # Configs
    guild_id = basic_utils.get_guild_id()

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("{cog_name.capitalize()} cog is ready")


async def setup(client):
    await client.add_cog({cog_name.capitalize()}(client))"""
        )


def verify_name(cog_name: str) -> bool:
    """
    Verifies that the cog name is valid
    :param cog_name: Name of the cog
    :return: True if the name is valid, False otherwise
    """
    # Check if the cog name is valid
    if cog_name.isidentifier():
        # Check if the cog already exists
        if os.path.isfile(f"../cogs/{cog_name}.py"):
            # Print error message
            print(f"Error: {cog_name}.py already exists")
            # Return False
            return False
        # Return True
        return True
    # Print error message
    print(f"Error: {cog_name} is not a valid name")
    # Return False
    return False


def main():
    # Get the cog name
    cog_name = input("Enter the name of the cog: ")

    # Parse result
    if verify_name(cog_name):
        # Make cog_name lowercase
        cog_name = cog_name.lower()
        # Create the cog file
        create_cog_file(cog_name)


if __name__ == "__main__":
    main()
