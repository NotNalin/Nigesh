import os
import discord
from discord.ext import commands
from rtadubai import Nol
from discord.commands import slash_command
from discord.ui import View

client = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Game("the fool with Nigesh"))


@client.command(aliases=['latency'])
async def ping(ctx):
    await ctx.reply(f'{round(client.latency * 1000)}ms', mention_author=False)


@client.slash_command(name="ping", description="Returns the bot's latency")
async def ping(ctx):
    await ctx.respond(f'{round(client.latency * 1000)}ms', ephemeral=True)


@client.command(aliases=["bal"])
async def balance(ctx, card):
    nolbal = Nol.details(card)
    if nolbal['Error'] is False:
        await ctx.reply(f"Your Nol card balance is : {nolbal['Card Balance']} AED", mention_author=False)
    else:
        await ctx.reply(f"{card} is not a valid NOL Card", mention_author=False)


@client.slash_command(name="balance", description="Check your NOL Card balance")
async def bal(ctx, card: discord.Option(str, "NOL Card Number", requied=True)):
    nolbal = Nol.details(card)
    if nolbal['Error'] is False:
        await ctx.respond(f"Your Nol card balance is : {nolbal['Card Balance']} AED")
    else:
        await ctx.respond(f"{card} is not a valid NOL Card")


@client.command()
async def nol(ctx, card):
    try:
        card = Nol.Card(card)
    except ValueError:
        await ctx.reply(f"{card} is not a valid NOL Card", mention_author=False)
        return

    embed = discord.Embed(title=f"NOL Details", description=f"{card.id}", color=0x00ff00)
    embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
    embed.add_field(name="Card Balance", value=f"{card.balance} AED", inline=True)
    embed.add_field(name="Pending Balance", value=f"{card.pending} AED", inline=True)
    embed.add_field(name="Expiry Date", value=f"{card.expiry}", inline=True)
    embed.set_footer(text=f"Please note that the shown balance may not include transactions occurred in the past 48 hours")
    await ctx.reply(embed=embed, mention_author=False)


@client.slash_command(name="nol", description="Returns the Nol card's Details")
async def nol(ctx, card):
    try:
        card = Nol.Card(card)
    except ValueError:
        await ctx.respond(f"{card} is not a valid NOL Card")
        return

    embed = discord.Embed(title=f"NOL Details", description=f"{card.id}", color=0x00ff00)
    embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
    embed.add_field(name="Card Balance", value=f"{card.balance} AED", inline=True)
    embed.add_field(name="Pending Balance", value=f"{card.pending} AED", inline=True)
    embed.add_field(name="Expiry Date", value=f"{card.expiry}", inline=True)
    embed.set_footer(text=f"Please note that the shown balance may not include transactions occurred in the past 48 hours")
    await ctx.respond(embed=embed)


@client.command()
async def recent(ctx, card, transaction_no=1):
    recent = Nol.recent(card, transaction_no)
    if recent['Error'] is False:
        transaction = recent['Transaction']
        if transaction_no == 1:
            embed = discord.Embed(title=f"Last NOL Transaction", description=f"{transaction['NolID']}")
        else:
            embed = discord.Embed(title=f"Recent NOL Transaction Number {transaction}", description=f"{transaction['NolID']}")
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Date", value=f"{transaction['Date']}")
        embed.add_field(name="Time", value=f"{transaction['Time']}")
        embed.add_field(name="Transaction Type", value=f"{transaction['Type']}")
        embed.add_field(name="Amount", value=f"{transaction['Amount']} AED")
        embed.set_footer(text=f"Please note that the bot only shows transactions occurred in the past month")
        await ctx.reply(embed=embed, mention_author=False)
    else:
        await ctx.reply(recent['ErrorMsg'], mention_author=False)


@client.slash_command(name="recent", description="Check your NOL Card recent transactions")
async def recent(ctx, card: discord.Option(str, "NOL Card Number", requied=True), transaction_no: discord.Option(int, name="transaction", description="Number of recent transaction to show", min_value=1, default=1)):
    recent = Nol.recent(card, transaction_no)
    if recent['Error'] is False:
        transaction = recent['Transaction']
        if transaction_no == 1:
            embed = discord.Embed(title=f"Last NOL Transaction", description=f"{transaction['NolID']}")
        else:
            embed = discord.Embed(title=f"Recent NOL Transaction Number {transaction}", description=f"{transaction['NolID']}")
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Date", value=f"{transaction['Date']}")
        embed.add_field(name="Time", value=f"{transaction['Time']}")
        embed.add_field(name="Transaction Type", value=f"{transaction['Type']}")
        embed.add_field(name="Amount", value=f"{transaction['Amount']} AED")
        embed.set_footer(text=f"Please note that the bot only shows transactions occurred in the past month")
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(recent['ErrorMsg'])


def transaction_embed(transactions, no):
    transaction = transactions[no]
    embed = discord.Embed(title=f"Transaction {no + 1}/{len(transactions)}", description=f"{transaction['NolID']}")
    embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
    embed.add_field(name="Date", value=f"{transaction['Date']}")
    embed.add_field(name="Time", value=f"{transaction['Time']}")
    embed.add_field(name="Transaction Type", value=f"{transaction['Type']}")
    embed.add_field(name="Amount", value=f"{transaction['Amount']} AED")
    embed.set_footer(text=f"Please note that the bot only shows transactions occurred in the past month")
    return embed


class TransactionsView(View):
    def __init__(self, transactions):
        self.transactions = transactions
        self.index = 0
        super().__init__()
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[2].label = f"{self.index + 1}/{len(self.transactions)}"

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        try:
            await self.message.edit_original_message(view=self)
        except AttributeError:
            await self.message.edit(view=self)

    @discord.ui.button(label="⏪", style=discord.ButtonStyle.blurple)
    async def rewind(self, button, interaction):
        self.index = 0
        button.disabled = True
        self.children[1].disabled = True
        self.children[2].label = f"{self.index + 1}/{len(self.transactions)}"
        self.children[3].disabled = False
        self.children[4].disabled = False
        await interaction.response.edit_message(embed=transaction_embed(self.transactions, self.index), view=self)

    @discord.ui.button(label="◀", style=discord.ButtonStyle.blurple)
    async def previous_callback(self, button, interaction):
        self.index -= 1
        if self.index == 0:
            self.children[0].disabled = True
            button.disabled = True
        if self.index < len(self.transactions) - 1:
            self.children[3].disabled = False
            self.children[4].disabled = False
        self.children[2].label = f"{self.index + 1}/{len(self.transactions)}"
        await interaction.response.edit_message(embed=transaction_embed(self.transactions, self.index), view=self)

    @discord.ui.button(label=f"1/0", style=discord.ButtonStyle.secondary, disabled=True)
    async def no_callback(self):
        pass

    @discord.ui.button(label="▶", style=discord.ButtonStyle.blurple)
    async def next_callback(self, button, interaction):
        self.index += 1
        if self.index == len(self.transactions) - 1:
            button.disabled = True
            self.children[4].disabled = True
        if self.index != 0:
            self.children[0].disabled = False
            self.children[1].disabled = False
        self.children[2].label = f"{self.index + 1}/{len(self.transactions)}"
        await interaction.response.edit_message(embed=transaction_embed(self.transactions, self.index), view=self)

    @discord.ui.button(label="⏩", style=discord.ButtonStyle.blurple)
    async def fast_forward(self, button, interaction):
        self.index = len(self.transactions) - 1
        self.children[0].disabled = False
        self.children[1].disabled = False
        self.children[2].label = f"{self.index + 1}/{len(self.transactions)}"
        self.children[3].disabled = True
        button.disabled = True
        await interaction.response.edit_message(embed=transaction_embed(self.transactions, self.index), view=self)


@client.command()
async def transactions(ctx, card):
    transactions = Nol.transactions(card)
    if transactions['Error'] is False:
        Transactions = transactions['Transactions']
        if len(Transactions) == 0:
            await ctx.reply("No transactions found")
        else:
            view = TransactionsView(Transactions)
            view.message = await ctx.reply(embed=transaction_embed(Transactions, 0), view=view)


@client.slash_command()
async def transactions(ctx, card):
    transactions = Nol.transactions(card)
    if transactions['Error'] is False:
        Transactions = transactions['Transactions']
        if len(Transactions) == 0:
            await ctx.respond("No transactions found")
        else:
            view = TransactionsView(Transactions)
            view.message = await ctx.respond(embed=transaction_embed(Transactions, 0), view=view)


client.run(os.environ['NIGESH_TOKEN'])
