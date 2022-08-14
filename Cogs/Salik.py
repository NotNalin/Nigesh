import os
import json
import discord
from discord.ext import commands
import rtadubai
from discord.commands import SlashCommandGroup
from rtadubai import Nol, Salik, Stop, JourneyPlanner
from discord.ui import View



class salik_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    salik = SlashCommandGroup("salik")

    @salik.command()
    async def balance(self, ctx, plate, mobile):
        balance = Salik.balance_plate(plate, mobile)
        try:
            int(balance)
            await ctx.respond(f"{balance} AED")
        except:
            await ctx.respond(balance)

    @salik.command()
    async def expiry(self, ctx, plate):
        expiry = Salik.expiry(plate)
        await ctx.respond(expiry)


def setup(bot):
    bot.add_cog(salik_cog(bot))
    print("Salik cog loaded")