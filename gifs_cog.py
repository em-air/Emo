import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import asyncio
import json
import random


class GifCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gif(self, ctx, *, search):
        try:
            async with ctx.typing():
                await asyncio.sleep(0)
                with open("./config.json", "r") as f:
                    configData = json.load(f)

                tenor_api_key = configData["TENOR_APIKEY"]
                limit = 8
                async with self.bot.session.get(f"https://g.tenor.com/v1/search?&key={tenor_api_key}&q={search}&limit={limit}") as resp:
                    gif_data = await resp.json()
                    gif_choice = random.randint(0, limit-1)
                    url = gif_data["results"][gif_choice]["media"][0]["gif"]["url"]
                    embed = discord.Embed(title=search.title())
                    embed.set_image(url=url)
                    embed.set_author(name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)

# ------------------------------------------------------------------------ERROR HANDLING-------------------------------------------------------------

    @gif.error
    async def gif_error(self, ctx, error):
        embed = discord.Embed(
            description="Provide a search query!")
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(embed=embed)
        else:
            raise error


def setup(bot):
    bot.add_cog(GifCommands(bot))
