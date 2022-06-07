import os
import discord
from discord.ext import commands
from rtadubai import Nol
from discord.commands import slash_command

client = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Game("the fool with Nigesh"))


@client.command(aliases=['latency'])
async def ping(ctx):
    await ctx.reply(f'{round(client.latency * 1000)}ms')


@client.slash_command(name="ping", description="Returns the bot's latency")
async def ping(ctx):
    await ctx.respond(f'{round(client.latency * 1000)}ms', ephemeral=True)


@client.command(aliases=["bal"])
async def balance(ctx, card):
    nolbal = Nol.Details(card)
    if nolbal['Error'] is False:
        await ctx.reply(f"Your Nol card balance is : {nolbal['Balance']}")
    else:
        await ctx.reply(f"{card} is not a valid NOL Card")


@client.slash_command(name="nol", description="Returns the Nol card's Details")
async def nol(ctx, card):
    nol_details = Nol.Details(card)
    if nol_details['Error'] is False:
        embed = discord.Embed(title=f"NOL Details", description=f"{nol_details['NolID']}")
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Card Balance", value=f"{nol_details['Card Balance']}")
        embed.add_field(name="Pending Balance", value=f"{nol_details['Pending Balance']}")
        embed.add_field(name="Expiry Date", value=f"{nol_details['Expiry Date']}")
        embed.set_footer(text=f"Please note that the shown balance may not include transactions occurred in the past 48 hours")
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(nol_details['ErrorMsg'])


@client.command()
async def nol(ctx, card):
    nol_details = Nol.Details(card)
    if nol_details['Error'] is False:
        embed = discord.Embed(title=f"NOL Details", description=f"{nol_details['NolID']}")
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Card Balance", value=f"{nol_details['Card Balance']}")
        embed.add_field(name="Pending Balance", value=f"{nol_details['Pending Balance']}")
        embed.add_field(name="Expiry Date", value=f"{nol_details['Expiry Date']}")
        embed.set_footer(text=f"Please note that the shown balance may not include transactions occurred in the past 48 hours")
        await ctx.reply(embed=embed)
    else:
        await ctx.reply(nol_details['ErrorMsg'])


@client.command()
async def recent(ctx, card, transaction=1):
    recent = Nol.Recent(card, transaction)
    if recent['Error'] is False:
        if transaction == 1:
            embed = discord.Embed(title=f"Last NOL Transaction", description=f"{recent['NolID']}")
        else:
            embed = discord.Embed(title=f"Recent NOL Transaction Number {transaction}", description=f"{recent['NolID']}")
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Date", value=f"{recent['Date']}")
        embed.add_field(name="Time", value=f"{recent['Time']}")
        embed.add_field(name="Transaction Type", value=f"{recent['Type']}")
        embed.add_field(name="Amount", value=f"{recent['Amount']} AED")
        embed.set_footer(text=f"Please note that the bot only shows transactions occurred in the past month")
        await ctx.reply(embed=embed)
    else:
        await ctx.reply(recent['ErrorMsg'])


@client.slash_command(name="balance", description="Check your NOL Card balance")
async def bal(ctx, card: discord.Option(str, "NOL Card Number", requied=True)):
    nolbal = Nol.Details(card)
    if nolbal['Error'] is False:
        await ctx.respond(f"Your Nol card balance is : {nolbal['Balance']}")
    else:
        await ctx.respond(f"{card} is not a valid NOL Card")


@client.slash_command(name="recent", description="Check your NOL Card recent transactions")
async def recent(ctx, card: discord.Option(str, "NOL Card Number", requied=True), transaction: discord.Option(int, description="Number of recent transaction to show", min_value=1, default=1)):
    recent = Nol.Recent(card, transaction)
    if recent['Error'] is False:
        if transaction == 1:
            embed = discord.Embed(title=f"Last NOL Transaction", description=f"{recent['NolID']}")
        else:
            embed = discord.Embed(title=f"Recent NOL Transaction Number {transaction}", description=f"{recent['NolID']}")
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Date", value=f"{recent['Date']}")
        embed.add_field(name="Time", value=f"{recent['Time']}")
        embed.add_field(name="Transaction Type", value=f"{recent['Type']}")
        embed.add_field(name="Amount", value=f"{recent['Amount']} AED")
        embed.set_footer(text=f"Please note that the bot only shows transactions occurred in the past month")
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(recent['ErrorMsg'])


client.run(os.environ['TOKEN'])
