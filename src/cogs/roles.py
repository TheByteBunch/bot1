import discord
from discord.ext import commands
from discord import app_commands
from configparser import ConfigParser


def get_guild_id():
    config = ConfigParser()
    config.read("../config.ini")
    return int(config["DEV"]["Guild_id"])


class Roles(commands.Cog):
    # Config
    guild_id = get_guild_id()

    # Variables
    allowed_roles = {}
    role_message_id = None

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Roles cog is ready")

    @app_commands.command(name="add_role", description="Add role for auto role message")
    @app_commands.guilds(guild_id)
    async def add_role(self, interaction: discord.Interaction, role_name: str, role_emoji: str):
        """
        Add a role to the auto role message
        :param interaction:
        :param role_name:
        :param role_emoji:
        :return:
        """
        # Get guild
        guild = self.client.get_guild(self.guild_id)

        # Get role
        role = discord.utils.get(guild.roles, name=role_name)

        # Get message
        emoji = role_emoji

        # Check if role and emoji exist
        if role and emoji:
            self.allowed_roles[role_name] = {
                "emoji": emoji,
                "data": role
            }
        else:
            await interaction.response.send_message("Role or emoji not found", ephemeral=True)
            return

        # Send response
        await interaction.response.send_message(f"Added role {role_name} with emoji {role_emoji}", ephemeral=True)

    @app_commands.command(name="remove_role", description="Remove role for auto role message")
    @app_commands.guilds(guild_id)
    async def remove_role(self, interaction: discord.Interaction, role_name: str):
        """
        Remove a role from the auto role message
        :param interaction:
        :param role_name:
        :return:
        """
        # Get guild
        guild = self.client.get_guild(self.guild_id)

        # Get role
        role = discord.utils.get(guild.roles, name=role_name)

        # Check if role exists
        if role:
            del self.allowed_roles[role_name]
        else:
            await interaction.response.send_message("Role not found", ephemeral=True)
            return

        # Send response
        await interaction.response.send_message(f"Removed role {role_name}", ephemeral=True)

    @app_commands.command(name="create_role_message", description="Creates a role message")
    @app_commands.guilds(guild_id)
    async def roles_func(self, interaction: discord.Interaction):
        """
        Creates a role message based on roles given by the user
        :param interaction:
        :return:
        """
        # Create message
        await interaction.response.send_message("React to this message to get your roles!")

        # Get latest message ID
        message = await interaction.channel.fetch_message(interaction.channel.last_message_id)

        # Create embed
        embed = discord.Embed(title="React to this message to get your roles!")

        # Add emojis to the embed
        for emoji_name, data in self.allowed_roles.items():
            embed.add_field(name=emoji_name, value=data["emoji"])

        # Add embed to the message
        await message.edit(embed=embed)

        # Add emojis to the message
        for key, value in self.allowed_roles.items():
            emoji = value["emoji"]
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
            print("No role message ID")
            return

        # Check if the message is the target message
        if payload.message_id != self.role_message_id:
            print("Not the target message")
            return

        # Check the guild is equal to the target guild
        guild = self.client.get_guild(payload.guild_id)
        if guild.id != self.guild_id:
            print("Not the target guild")
            return

        # Check that emoji is within allowed
        allowed_emojis = [data["emoji"] for data in self.allowed_roles.values()]
        if payload.emoji.name not in allowed_emojis:
            print("Emoji not allowed")
            return

        print(f"Adding role {payload.emoji.name}")

        # Get role name
        role_name = None
        for k, v in self.allowed_roles.items():
            if v["emoji"] == payload.emoji.name:
                role_name = k

        # Adding the role
        role = discord.utils.get(guild.roles, name=role_name)
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
        allowed_emojis = [data["emoji"] for data in self.allowed_roles.values()]
        if payload.emoji.name not in allowed_emojis:
            return

        print(f"Removing role {payload.emoji.name}")

        # Get role name
        role_name = None
        for k, v in self.allowed_roles.items():
            if v["emoji"] == payload.emoji.name:
                role_name = k

        # Adding the role
        role = discord.utils.get(guild.roles, name=role_name)
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)


async def setup(client):
    await client.add_cog(Roles(client))
