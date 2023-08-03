import discord
from discord.ext import commands
from discord import app_commands
import asyncio


class Roles(commands.Cog):
    allowed_reactions = {
        "👍": "Thumbs up",
        "👎": "thumbs down",
        "😀": "smile face",
    }
    role_message_id = None
    guild_id = 1136642484697583667

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Roles cog is ready")

    @app_commands.command(name="create_role_message", description="Creates a role message")
    @app_commands.guilds(1136642484697583667)
    async def roles_func(self, interaction: discord.Interaction):
        # Create message
        await interaction.response.send_message("React to this message to get your roles!")

        # Get latest message ID
        message = await interaction.channel.fetch_message(interaction.channel.last_message_id)

        # Create embed
        embed = discord.Embed(title="React to this message to get your roles!")

        # Add emojis to the embed
        for emoji, emoji_name in self.allowed_reactions.items():
            embed.add_field(name=emoji_name, value=emoji)

        # Add embed to the message
        await message.edit(embed=embed)

        # Add emojis to the message
        for emoji in self.allowed_reactions:
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
        if payload.emoji.name not in self.allowed_reactions.keys():
            print("Emoji not allowed")
            return

        print(f"Adding role {payload.emoji.name}")

        # Adding the role
        role = discord.utils.get(guild.roles, name=self.allowed_reactions[payload.emoji.name])
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
        if payload.emoji.name not in self.allowed_reactions.keys():
            return

        print(f"Removing role {payload.emoji.name}")

        # Adding the role
        role = discord.utils.get(guild.roles, name=self.allowed_reactions[payload.emoji.name])
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)


async def setup(client):
    await client.add_cog(Roles(client))
