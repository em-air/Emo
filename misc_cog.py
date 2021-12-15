import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import asyncio
import json
import country_converter as coco


class MiscCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
# ---------------------------------------------------------------------------PING COMMAND-----------------------------------------------------------------------

    @commands.command()
    async def ping(self, ctx):
        try:
            pingEmbed = discord.Embed(
                title='PONG!', description=f'{round(self.bot.latency * 1000)}ms')
            await ctx.send(embed=pingEmbed)
        except Exception as e:
            print(e)

# -------------------------------------------------------------------------INVITE COMMAND-------------------------------------------------------------------
    @commands.command()
    async def invite(self, ctx):
        try:

            bot_owner = await self.bot.fetch_user(799524443390738462)
            async with ctx.typing():
                await asyncio.sleep(0)
                embed = discord.Embed(
                    title="Invites and more!", color=discord.Color.random())
                embed.add_field(name="Invite me to your server!",
                                value="[Invite me!](https://discord.com/oauth2/authorize?client_id=844954629569773568&scope=bot&permissions=2147847232)", inline=False)
                embed.add_field(
                    name="Open source", value="[You can view my source code here](https://github.com/ShMoUm/Emo)!", inline=False)
                embed.set_footer(text=f"This bot was made by {bot_owner}")
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
# -------------------------------------------------------------------------ADVICE COMMAND------------------------------------------------------------------

    @commands.command()
    async def advice(self, ctx):
        try:
            async with ctx.typing():
                await asyncio.sleep(0)
                async with self.bot.session.get("https://api.adviceslip.com/advice") as r:
                    advice_dict = await r.json(content_type='text/html')
                    advice = advice_dict["slip"]["advice"]
                    embed = discord.Embed(description=advice)
                    embed.set_author(name=ctx.author.display_name,
                                     icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
        except Exception as e:
            print(e)
# -----------------------------------------------------------------------NAT COMMAND-------------------------------------------------------------------------

    @commands.command()
    async def nat(self, ctx, query):
        try:
            async with ctx.typing():
                await asyncio.sleep(0)
                async with self.bot.session.get("https://api.nationalize.io/?name=" + query) as r:
                    nat_dict = await r.json()

                    embed = discord.Embed(
                        title=f"{query.title()} is probably from...", description="", color=discord.Color.green())

                    for i in nat_dict.get("country"):
                        long_name = coco.convert(
                            names=f"{i['country_id']}", to='name_short')  # converts country code to the official name
                        embed.add_field(
                            name=f"{long_name}", value=f"Probability: {round(i['probability']*100, 2)}%", inline=False)
                    await ctx.send(embed=embed)
        except Exception as e:
            print(e)

# --------------------------------------------------------------------------LOVE COMMAND-------------------------------------------------------------------------------
    @commands.command()
    async def love(self, ctx):
        try:
            name, discrim = str(ctx.message.author).split('#')
            async with ctx.typing():
                await asyncio.sleep(0)
                await ctx.send(f"I love you, {name}.")
        except Exception as e:
            print(e)
# ------------------------------------------------------------------------INSULT COMMAND------------------------------------------------------------------------------------

    @commands.command()
    async def insult(self, ctx, member: commands.MemberConverter):
        try:
            async with ctx.typing():
                await asyncio.sleep(0)
                async with self.bot.session.get("https://evilinsult.com/generate_insult.php?lang=en&type=json") as r:
                    r = await r.json(content_type='application/json')
                    insult = r["insult"]
                    name, discrim = str(ctx.message.author).split('#')
                    if member == ctx.message.author:
                        await ctx.send("Ooh, self burn. Those are rare.")
                    else:
                        await ctx.send(f"{member.mention}, {insult}.\n\n   `Requested by {name}`")
        except Exception as e:
            print(e)

# ---------------------------------------------------------------------------------COMPLIMENT COMMAND-----------------------------------------------------------
    @commands.command()
    async def compliment(self, ctx, member: commands.MemberConverter):
        try:
            async with ctx.typing():
                await asyncio.sleep(0)
                async with self.bot.session.get("https://complimentr.com/api") as r:
                    r = await r.json()
                    compliment = r["compliment"]
                    compliment = compliment[0].upper() + compliment[1:]
                    await ctx.send(f"{compliment}, {member.mention}.")
        except Exception as e:
            print(e)
# ---------------------------------------------------------------------------------ERROR HANDLING---------------------------------------------------------------

    @nat.error
    async def nat_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Provide a search query!")
        elif isinstance(error, CommandInvokeError):
            print(error.original)
        else:
            raise error

    @advice.error
    async def advice_error(self, ctx, error):
        raise error

    @invite.error
    async def invite_error(self, ctx, error):
        raise error

    @insult.error
    async def insult_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):  
            await ctx.send("You need to ping someone!")
        elif isinstance(error, MemberNotFound):
            await ctx.send("User not found.")
        else:
            raise error

    @compliment.error
    async def compliment_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("You need to ping someone!")
        elif isinstance(error, MemberNotFound):
            await ctx.send("User not found.")
        else:
            raise error


def setup(bot):
    bot.add_cog(MiscCommands(bot))
