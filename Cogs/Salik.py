import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from rtadubai import Salik



class salik_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    salik = SlashCommandGroup("salik", description="Salik commands")

    @salik.command()
    async def balance(self, ctx, plate, mobile):
        await ctx.defer()
        balance = Salik.balance_plate(plate, mobile)
        try:
            int(balance)
            await ctx.respond(f"{balance} AED")
        except:
            await ctx.respond(balance)

    @salik.command()
    async def expiry(self, ctx, plate):
        await ctx.defer()
        expiry = Salik.expiry(plate)
        await ctx.respond(expiry)


def setup(bot):
    bot.add_cog(salik_cog(bot))
    print("Salik cog loaded")