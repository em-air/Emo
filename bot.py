import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import aiohttp
import json

intents = Intents.all()
intents.members = True

# bot = commands.Bot(command_prefix=["e.", "E.", "emo ", "Emo "], case_insensitive=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("e.", "E.", "emo ", "Emo "))
bot.remove_command('help')


with open("config.json", "r") as f:
    configData = json.load(f)

token = configData["Token"]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="e.help"))


@bot.event
async def on_connect():
    bot.session = aiohttp.ClientSession()


@bot.event
async def on_guild_join(guild):
    guild_name = guild.name
    guild_id = str(guild.id)
    guild_region = guild.region
    data = None
    with open("guilds.json", "r") as f:
        data = json.load(f)
    data[guild_id] = {"name": guild_name, "region": guild_region}
    with open("guilds.json", "w") as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_guild_remove(guild):      
    try:
        guild_id = str(guild.id)
        data = None
        with open("guilds.json", "r") as f:
            data = json.load(f)
        del data[guild_id]
        with open("guilds.json", "w") as f:
            json.dump(data, f, indent=4)
    except KeyError:
        print("This server does not exist.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return


@bot.command(aliases=["info"])
async def help(ctx):
    embed = discord.Embed(title="Info", description="Prefix aliases: 'e.', 'emo' or just ping the bot.",
        color=discord.Color.green()

    )
    embed.add_field(name='e.ping', value='Returns PONG!', inline=False)
    embed.add_field(
        name='e.gif <search query>', value='Returns gif!', inline=False)
    embed.add_field(
        name="e.advice", value="A piece of advice.", inline=False)
    embed.add_field(
        name="e.meme", value="Posts a meme from reddit.", inline=False)
    embed.add_field(
        name="e.def <word>", value="Returns funny definition of given word.", inline=False)
    embed.add_field(
        name="e.insult <ping someone here>", value="Roast someone.", inline=False)
    embed.add_field(
        name="e.compliment <ping someone here>", value="Compliment someone!", inline=False)
    embed.add_field(
        name="e.invite", value="Invite Emo to your sever!", inline=False)


    await ctx.send(embed=embed)


bot.load_extension('gifs_cog')
bot.load_extension('misc_cog')
bot.load_extension('meme_cog')
bot.load_extension('dictionary_cog')
bot.run(token)
