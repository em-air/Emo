import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import asyncio
import random
import re
import json


class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['def'])
    async def define(self, ctx, *, query):
        url = f"https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": query}

        with open("./config.json", "r") as f:
            configData = json.load(f)

        ub_apikey = configData["UB_APIKEY"]
        headers = {
            'x-rapidapi-key': ub_apikey,
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }
        async with ctx.typing():
            await asyncio.sleep(0)
            async with self.bot.session.get(url, headers=headers, params=querystring) as r:
                try:
                    dic = await r.json()
                    list_of_definitions = dic["list"]
                    # done to prevent ValueError.
                    randomized_definitions_list = random.sample(
                        list_of_definitions, len(list_of_definitions))
                    def_choice = random.choice(
                        [x for x in range(len(randomized_definitions_list))])
                    defnText = list_of_definitions[def_choice]["definition"]
                    # removes "[" and "]" from the string.
                    defn = re.sub(r"[\([{})\]]", "", defnText)
                    exampleText = list_of_definitions[def_choice]["example"]
                    example = re.sub(r"[\[{}\]]", "", exampleText)
                    embed = discord.Embed(
                        title=query, color=discord.Color.green())
                    embed.add_field(name="Definition",
                                    value=defn, inline=False)
                    embed.add_field(
                        name="Example", value=example, inline=False)
                    embed.set_author(name=ctx.author.display_name,
                                     icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                except IndexError:
                    await ctx.send(f"Sorry, I couldn't find: {query}. There are no definitions for this word :/")
                    # try and except was used since it was an IndexError



# ---------------------------------------------------------------------------------ERROR HANDLING---------------------------------------------------------------

    @define.error
    async def define_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Provide a search query!")
        elif hasattr(error, "original"):
            if isinstance(error.original, IndexError):
                await ctx.send("Word not found.")
        else:
            raise error


def setup(bot):
    bot.add_cog(Dictionary(bot))
