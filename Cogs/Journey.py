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
        return Shail.stopnames(ctx.value)
    except Exception as e:
        print(e)
        return []
        
class journey_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        embed = discord.Embed(title=f"{stop.name}", description=f"Departures at {stop.name}")
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

