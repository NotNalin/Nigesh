import discord
from discord.ext import commands, pages
from discord.commands import SlashCommandGroup
from rtadubai import Nol


class nol_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, card):
        nolbal = Nol.details(card)
        if nolbal['Error'] is False:
            await ctx.reply(f"Your Nol card balance is : {nolbal['Card Balance']} AED", mention_author=False)
        else:
            await ctx.reply(f"{card} is not a valid NOL Card", mention_author=False)

    @commands.command(name='nol', aliases=['details'])
    async def _nol(self, ctx, card):
        try:
            card = Nol.Card(card)
        except ValueError:
            await ctx.reply(f"{card} is not a valid Nol Card", mention_author=False)
            return

        embed = discord.Embed(title=f"Nol Details", description=f"{card.id}", color=0x00ff00)
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Card Balance", value=f"{card.balance} AED", inline=True)
        embed.add_field(name="Pending Balance", value=f"{card.pending} AED", inline=True)
        embed.add_field(name="Expiry Date", value=f"{card.expiry}", inline=True)
        embed.set_footer(text=f"Please note that the shown balance may not include transactions occurred in the past 48 hours")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def recent(self, ctx, card, transaction_no=1):
        recent = Nol.recent(card, transaction_no)
        if recent['Error'] is False:
            transaction = recent['Transaction']
            if transaction_no == 1:
                embed = discord.Embed(title=f"Last Nol Transaction", description=f"{transaction['NolID']}")
            else:
                embed = discord.Embed(title=f"Recent Nol Transaction Number {transaction}", description=f"{transaction['NolID']}")
            embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
            embed.add_field(name="Date", value=f"{transaction['Date']}")
            embed.add_field(name="Time", value=f"{transaction['Time']}")
            embed.add_field(name="Transaction Type", value=f"{transaction['Type']}")
            embed.add_field(name="Amount", value=f"{transaction['Amount']} AED")
            embed.set_footer(text=f"Please note that the bot only shows transactions occurred in the past month")
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply(recent['ErrorMsg'], mention_author=False)

    @commands.command()
    async def transactions(self, ctx, card):
        transactions = Nol.transactions(card)
        if transactions['Error'] is False:
            Transactions = transactions['Transactions']
            if len(Transactions) == 0:
                await ctx.reply("No transactions found")
            else:
                paginator = pages.Paginator(pages=transaction_embeds(Transactions))
                await paginator.send(ctx, reference=ctx.message, mention_author=False)

    nol = SlashCommandGroup("nol", description="Nol commands")

    @nol.command(name="balance", description="Check your Nol Card balance")
    @discord.option(name='card', type=str, required=True, description='Nol Card Number', max_length=10, min_length=10)
    async def bal(self, ctx, card):
        await ctx.defer(ephemeral=True)
        nolbal = Nol.details(card)
        if nolbal['Error'] is False:
            await ctx.respond(f"Your Nol card balance is : {nolbal['Card Balance']} AED", ephemeral=False)
        else:
            await ctx.respond(f"{card} is not a valid Nol Card")

    @nol.command(name="details", description="Returns the Nol card's Details")
    @discord.option(name='card', type=str, required=True, description='Nol Card Number', max_length=10, min_length=10)
    async def details(self, ctx, card):
        await ctx.defer(ephemeral=True)
        try:
            card = Nol.Card(card)
        except ValueError:
            await ctx.respond(f"{card} is not a valid Nol Card")
            return

        embed = discord.Embed(title=f"NOL Details", description=f"{card.id}", color=0x00ff00)
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Card Balance", value=f"{card.balance} AED", inline=True)
        embed.add_field(name="Pending Balance", value=f"{card.pending} AED", inline=True)
        embed.add_field(name="Expiry Date", value=f"{card.expiry}", inline=True)
        embed.set_footer(text=f"Please note that the shown balance may not include transactions occurred in the past 48 hours")
        await ctx.respond(embed=embed, ephemeral=False)

    @nol.command(name="recent", description="Check your Nol Card recent transactions")
    @discord.option(name='card', type=str, required=True, description='Nol Card Number', max_length=10, min_length=10)
    @discord.option(name='transaction_no', type=int, default=1, description='Number of recent transaction to show')
    async def recent_slash(self, ctx, card, transaction_no):
        await ctx.defer(ephemeral=True)
        recent = Nol.recent(card, transaction_no)
        if recent['Error'] is False:
            transaction = recent['Transaction']
            if transaction_no == 1:
                embed = discord.Embed(title=f"Last Nol Transaction", description=f"{transaction['NolID']}")
            else:
                embed = discord.Embed(title=f"Recent Nol Transaction Number {transaction}", description=f"{transaction['NolID']}")
            embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
            embed.add_field(name="Date", value=f"{transaction['Date']}")
            embed.add_field(name="Time", value=f"{transaction['Time']}")
            embed.add_field(name="Transaction Type", value=f"{transaction['Type']}")
            embed.add_field(name="Amount", value=f"{transaction['Amount']} AED")
            embed.set_footer(text=f"Please note that the bot only shows transactions occurred in the past month")
            await ctx.respond(embed=embed, ephemeral=False)
        else:
            await ctx.respond(recent['ErrorMsg'], ephemeral=False)

    @nol.command(name="transactions", description="Check your Nol Card transactions")
    @discord.option(name='card', type=str, required=True, description='Nol Card Number', max_length=10, min_length=10)
    async def transactions_slash(self, ctx, card):
        await ctx.defer(ephemeral=True)
        transactions = Nol.transactions(card)
        if transactions['Error'] is False:
            Transactions = transactions['Transactions']
            if len(Transactions) == 0:
                await ctx.respond("No transactions found")
            else:
                paginator = pages.Paginator(pages=transaction_embeds(Transactions))
                await paginator.respond(ctx.interaction, ephemeral=False)


def transaction_embeds(transactions):
    embeds = []
    for transaction in transactions:
        embed = discord.Embed(title=f"Nol Transaction {len(embeds) + 1}/{len(transactions)}", description=f"{transaction['NolID']}")
        embed.set_thumbnail(url="https://www.rta.ae/wps/wcm/connect/rta/3ae021ee-ea75-4c10-a579-35ab58bcf20d/apps.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_N004G041LOBR60AUHP2NT32000-3ae021ee-ea75-4c10-a579-35ab58bcf20d-nUKFITN")
        embed.add_field(name="Date", value=f"{transaction['Date']}")
        embed.add_field(name="Time", value=f"{transaction['Time']}")
        embed.add_field(name="Transaction Type", value=f"{transaction['Type']}")
        embed.add_field(name="Amount", value=f"{transaction['Amount']} AED")
        embed.set_footer(text=f"Please note that the bot only shows transactions occurred in the past month")
        embeds.append(embed)
    return embeds


def setup(bot):
    bot.add_cog(nol_cog(bot))
    print("Nol cog loaded")
