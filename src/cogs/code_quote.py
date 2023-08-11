import os
import random

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv
from github import Auth, Github
from utils import basic_utils

load_dotenv(find_dotenv())


def get_random_line():
    auth = Auth.Token(os.getenv("GITHUB_TOKEN"))

    g = Github(auth=auth)

    repos = list(g.get_user("thebytebunch").get_repos())
    random.shuffle(repos)
    content_files = []
    while not content_files:
        repo = repos.pop()
        contents = repo.get_contents("")
        while len(contents) > 0:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                content_files.append(file_content)

        content_files = [
            content_file
            for content_file in content_files
            if content_file.path.endswith(".py")
        ]

    content_file = random.choice(content_files)
    lines = content_file.decoded_content.decode("ASCII").split("\n")
    chosen_line = ""
    while not chosen_line.strip():
        chosen_line = random.choice(lines)
    return chosen_line


class CodeQuoteCog(commands.Cog):
    guild_id = basic_utils.get_guild_id()

    @app_commands.command(name="code-quote", description="Quotes code")
    async def ping(self, interactions: discord.Interaction):
        await interactions.message.channel.send(
            "I'm going to fetch a random line of code from one of our repositories. "
            "Will you be able to guess what it is?"
        )
        await interactions.message.channel.send(f"Code: \n{get_random_line()}")


async def setup(bot):
    await bot.add_cog(CodeQuoteCog(bot))
