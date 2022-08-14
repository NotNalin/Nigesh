import os
import json
import discord
from discord.ext import commands
import rtadubai
from discord.commands import SlashCommandGroup
from rtadubai import Nol, Salik, Stop, JourneyPlanner
from discord.ui import View


async def stop_searcher(ctx: discord.AutocompleteContext):
    try:
        stops = [stop['name'] for stop in rtadubai.StopFinder.findstop(ctx.value)]
    except:
        stops = []
    return stops
        
class journey_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command()
    @discord.option(name='from_stop', type=str, description="From stop", autocomplete=stop_searcher)
    @discord.option(name='to_stop', type=str, description="To stop", autocomplete=stop_searcher)
    async def journey(self, ctx, from_stop, to_stop):
        from_stop = Stop(name=from_stop)
        to_stop = Stop(name=to_stop)
        journey = JourneyPlanner.findroute(from_stop, to_stop)
        await ctx.respond(json.dumps(journey, indent=4))

    @commands.slash_command()
    @discord.option(name='stop', type=str, description="Stop to check departures", autocomplete=stop_searcher)
    async def departures(self, ctx, stop):
        stop = Stop(name=stop)
        departures = JourneyPlanner.departures(stop)
        await ctx.respond(json.dumps(departures, indent=4))

def setup(bot):
    bot.add_cog(journey_cog(bot))
    print("Journey cog loaded")

