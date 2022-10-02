import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from rtadubai import Salik


class salik_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    salik = SlashCommandGroup("salik", description="Salik commands")

    @salik.command()
    async def balance(self, ctx, plate: discord.Option(str, description="Plate"), mobile: discord.Option(str, description="Mobile number")):
        await ctx.defer()
        try:
            balance = Salik.balance_plate(plate, mobile)
            int(balance)
            await ctx.respond(f"{balance} AED")
        except Exception as e:
            print(e)
            await ctx.respond(e.split(":")[-1])

    @salik.command()
    async def expiry(self, ctx, plate):
        await ctx.defer()
        expiry = Salik.expiry(plate)
        await ctx.respond(expiry)


def setup(bot):
    bot.add_cog(salik_cog(bot))
    print("Salik cog loaded")
