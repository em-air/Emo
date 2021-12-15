import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import asyncio
import asyncpraw
import random
import json


class Memes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        try:
            async with ctx.typing():
                await asyncio.sleep(0)
                with open("config.json", "r") as f:
                    configdata = json.load(f)
                client_id = configdata["CLIENT_ID"]
                client_secret = configdata["CLIENT_SECRET"]
                user_agent = configdata["USER_AGENT"]
                reddit = asyncpraw.Reddit(client_id=client_id,
                                        client_secret=client_secret,
                                        user_agent=user_agent)

                subreddits = random.choice(
                    ["okbuddyretard", "196", "comedyheaven", "antimeme", "blursedimages", "ComedyNecrophilia", "starterpacks"])
                subreddit = await reddit.subreddit(subreddits)
                hot = subreddit.hot(limit=50)
                memes = []
                async for submission in hot:
                    # iterates through hot memes and appends each value to the list meme
                    memes.append(submission)
                meme = random.choice(memes)  # chooses a random meme url
                embed = discord.Embed(
                    title=meme.title, description='', color=discord.Color.random())
                embed.set_image(url=meme.url)
                embed.set_footer(text=f"This post was taken from r/{subreddits}")
            await ctx.reply(embed=embed)
        except Exception as e:
            print(e)

# ------------------------------ERROR HANDLING--------------------------------------------
    @meme.error
    async def meme_error(self, ctx, error):
        raise error


def setup(bot):
    bot.add_cog(Memes(bot))
