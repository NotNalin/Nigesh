import os
import json
import discord
from discord.ext import commands, pages
import rtadubai
from discord.commands import SlashCommandGroup
from rtadubai import Nol, Salik, Shail
from discord.ui import View


async def stop_searcher(ctx: discord.AutocompleteContext):
    try:
        stops = [stop['name'] for stop in Shail.findstop(ctx.value)]
    except:
        stops = []
    return stops
        
class journey_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # @commands.slash_command()
    # @discord.option(name='from_stop', type=str, description="From stop", autocomplete=stop_searcher)
    # @discord.option(name='to_stop', type=str, description="To stop", autocomplete=stop_searcher)
    # async def journey(self, ctx, from_stop, to_stop):
    #     from_stop = Stop(name=from_stop)
    #     to_stop = Stop(name=to_stop)
    #     journey = JourneyPlanner.findroute(from_stop, to_stop)
    #     await ctx.respond(json.dumps(journey, indent=4))

    @commands.slash_command()
    @discord.option(name='stop', type=str, description="Stop to check departures", autocomplete=stop_searcher)
    async def departures(self, ctx, stop):
        stop = Shail.Stop(name=stop)
        departures = Shail.departures(stop)
        paginator = pages.Paginator(pages=departure_embeds(departures, stop))
        await paginator.respond(ctx.interaction)
        

def departure_embeds(departures, stop):
    embeds = []
    for departure in departures:
        embed = discord.Embed(title=f"{stop.name}", description=f"Departures at {stop.name}", color=0x00ff00)
        embed.add_field(name="Mode", value=departure["mode"])
        embed.add_field(name="Type", value=departure["type"])
        embed.add_field(name="Direction", value=departure["direction"])
        embed.add_field(name="Scheduled Time", value=departure["scheduled_time"])
        embed.add_field(name="Estimated Time", value=departure["estimated_time"])
        embed.add_field(name="Status", value=departure["status"])
        embeds.append(embed)
    return embeds

def setup(bot):
    bot.add_cog(journey_cog(bot))
    print("Journey cog loaded")

