import os

import discord
from github import Github
from github import Auth

from discord.ext import commands
import random

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_random_line():
    auth = Auth.Token(os.getenv("GITHUB_TOKEN"))

    g = Github(auth=auth)

    content_files = []

    for repo in g.get_user('thebytebunch').get_repos():
        contents = repo.get_contents('')
        while len(contents) > 0:
            file_content = contents.pop(0)
            if file_content.type == 'dir':
                contents.extend(repo.get_contents(file_content.path))
            else:
                content_files.append(file_content)

    lines = []
    for content_file in content_files:
        lines.extend(content_file.decoded_content.decode('ASCII').split('\n'))
    chosen_line = ''
    while not chosen_line.strip():
        chosen_line = random.choice(lines)
    return chosen_line


if __name__ == '__main__':
    print(get_random_line())


class CodeQuoteCog(commands.Cog, name='CodeQuoteCog'):

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.content.startswith('$code'):
            await message.channel.send(f"I'm going to fetch a random line of code from one of our repositories. "
                                       f"Will you be able to guess what it is?")
            await message.channel.send(f"Code: \n{get_random_line()}")


async def setup(bot):
    await bot.add_cog(CodeQuoteCog(bot))
