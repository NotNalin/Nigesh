import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned_or('$'), intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Game("the fool with Sura"))


@client.command(aliases=['latency'])
async def ping(ctx):
    await ctx.reply(f'{round(client.latency * 1000)}ms', mention_author=False)


@client.slash_command(name="ping", description="Returns the bot's latency")
async def ping(ctx):
    await ctx.respond(f'{round(client.latency * 1000)}ms', ephemeral=True)


for i in os.listdir('./Cogs'):
    if i.endswith('.py'):
        client.load_extension(f'Cogs.{i[:-3]}', store = False)

client.load_extension('jishaku')

client.run(os.environ['NIGESH_TOKEN'])
