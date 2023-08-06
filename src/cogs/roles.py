import discord
from discord.ext import commands
from discord import app_commands

from utils import basic_utils

import logging


class Roles(commands.Cog):
    # Config
    guild_id = (
        basic_utils.get_guild_id()
    )  # this doesn't generalize to multiple servers #todo maybe

    def __init__(self, client: commands.Bot):
        self.client = client
        self.dict_of_role_to_emoji = dict()
        self.role_message_id = None

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Roles cog is ready")
        print("Roles cog is ready")

    @app_commands.command(name="add_role", description="Add role for auto role message")
    @app_commands.guilds(guild_id)
    async def add_role(
        self, interaction: discord.Interaction, role_name: str, role_emoji: str
    ):
        """
        Add a role to the auto role message
        :param interaction:
        :param role_name:
        :param role_emoji:
        :return:
        """
        if interaction.guild.id != self.guild_id:
            return
        # Get guild
        guild = self.client.get_guild(self.guild_id)

        # Get role
        role = discord.utils.get(guild.roles, name=role_name).name

        # Get message
        emoji = role_emoji

        # Check if role and emoji exist
        if role and emoji:
            self.dict_of_role_to_emoji[role] = emoji
        else:
            await interaction.response.send_message(
                "Role or emoji not found", ephemeral=True
            )
            return

        # Send response
        await interaction.response.send_message(
            f"Added role {role_name} with emoji {role_emoji}", ephemeral=True
        )

    @app_commands.command(
        name="remove_role", description="Remove role for auto role message"
    )
    @app_commands.guilds(guild_id)
    async def remove_role(self, interaction: discord.Interaction, role_name: str):
        """
        Remove a role from the auto role message
        :param interaction:
        :param role_name:
        :return:
        """
        if interaction.guild.id != self.guild_id:
            return
        # Get guild
        guild = self.client.get_guild(self.guild_id)

        # Get role
        role = discord.utils.get(guild.roles, name=role_name)

        # Check if role exists
        if role:
            del self.dict_of_role_to_emoji[role_name]
        else:
            await interaction.response.send_message("Role not found", ephemeral=True)
            return

        # Send response
        await interaction.response.send_message(
            f"Removed role {role_name}", ephemeral=True
        )

    @app_commands.command(
        name="create_role_message", description="Creates a role message"
    )
    @app_commands.guilds(guild_id)
    async def create_roles_message(self, interaction: discord.Interaction):
        """
        Creates a role message based on roles given by the user
        :param interaction:
        :return:
        """
        if interaction.guild.id != self.guild_id:
            return
        # Create message
        await interaction.response.send_message(
            "React to this message to get your roles!"
        )

        # Get latest message ID
        # todo: is there a more reliable way to do this?
        message = await interaction.channel.fetch_message(
            interaction.channel.last_message_id
        )

        # Create embed
        embed = discord.Embed(title="React to this message to get your roles!")

        # Add emojis to the embed
        for role_name, emoji in self.dict_of_role_to_emoji.items():
            embed.add_field(name=role_name, value=emoji)

        # Add embed to the message
        await message.edit(embed=embed)

        # Add emojis to the message
        for emoji in self.dict_of_role_to_emoji.values():
            await message.add_reaction(emoji)

        # Save message ID
        self.role_message_id = message.id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Give a role based on a reaction emoji
        :param payload:
        :return:
        """
        # Make sure that the bot is not reacting to itself
        if payload.member.bot:
            return

        # Check that role message has been created
        if self.role_message_id is None:
            logging.warning("No role message ID")
            return

        # Check if the message is the target message
        if payload.message_id != self.role_message_id:
            logging.warning("Not the target message")
            return

        # Check the guild is equal to the target guild
        guild = self.client.get_guild(payload.guild_id)
        if guild.id != self.guild_id:
            logging.warning("Not the target guild")
            return

        # Check that emoji is within allowed
        allowed_emojis = self.dict_of_role_to_emoji.values()
        # name: The custom emoji name, if applicable, or the unicode codepoint of the non-custom emoji.
        if payload.emoji.name not in allowed_emojis:
            logging.warning("Emoji not allowed")
            return

        logging.info(f"Adding role {payload.emoji.name}")

        # Get role name
        # role_name = None
        role_name_to_apply = ""
        for role_name, emoji in self.dict_of_role_to_emoji.items():
            if payload.emoji.name == emoji:
                role_name_to_apply = role_name
                break  # note to Al1: at least this is on average n/2 (still O(n) though)
        assert (
            role_name_to_apply != ""
        ), "role_name_to_apply should have a non-empty string value"
        # Adding the role
        role = discord.utils.get(guild.roles, name=role_name_to_apply)
        member = guild.get_member(payload.user_id)

        await member.add_roles(role, reason="Reaction role")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """
        Remove a role based on a reaction emoji
        :param payload:
        :return:
        """

        # Check that role message has been created
        if self.role_message_id is None:
            return

        # Check if the message is the target message
        if payload.message_id != self.role_message_id:
            return

        # Check the guild
        guild = self.client.get_guild(payload.guild_id)
        if guild.id != self.guild_id:
            return

        # Check that emoji is within allowed

        allowed_emojis = self.dict_of_role_to_emoji.values()
        if payload.emoji.name not in allowed_emojis:
            return

        logging.info(f"Removing role {payload.emoji.name}")

        # Get role name
        role_name = None
        for role_name, emoji in self.dict_of_role_to_emoji.items():
            if payload.emoji.name == emoji:
                role_name_to_apply = role_name
                break

        # Removing a role
        role = discord.utils.get(guild.roles, name=role_name_to_apply)
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)


async def setup(client):
    await client.add_cog(Roles(client))
