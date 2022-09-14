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

    @commands.slash_command()
    @discord.option(name='fromstop', type=str, description="From stop", autocomplete=stop_searcher)
    @discord.option(name='tostop', type=str, description="To stop", autocomplete=stop_searcher)
    async def journey(self, ctx, fromstop, tostop):
        await ctx.defer()
        fromstop = Shail.Stop(name=fromstop)
        tostop = Shail.Stop(name=tostop)
        journey = Shail.journey_planner(fromstop, tostop)
        paginator = pages.Paginator(pages=journey_embeds(journey), show_menu=True, menu_placeholder="Select a Journey")
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

def journey_embeds(journeys):
    menus = []
    for journey in journeys:
        embeds = []
        embed = discord.Embed()
        embed.add_field(name="Staring From", value=journey["startstop"])
        embed.add_field(name="Starting time", value=journey["starttime"])
        embed.add_field(name="Ending Time", value=journey["endtime"])
        embed.add_field(name="Duration", value=journey["duration"])
        embed.add_field(name="Amount", value=journey["amount"])
        embeds.append(embed)
        for i in journey['journeys']:
            embed = discord.Embed()
            embed.add_field(name="Time", value=i["time"])
            embed.add_field(name="Stop", value=i["stop"])
            embed.add_field(name="Method", value=i["method"])
            embed.add_field(name="Mode", value=i["mode"])
            embed.add_field(name="Duration", value=i["duration"])
            embeds.append(embed)
        menus.append(
            pages.PageGroup(
                pages=embeds,
                label=f"Starting time : {journey['starttime']}, Ending Time: {journey['endtime']}",
                description=f"Duration: {journey['duration']}, Amount: {journey['amount']}",
            )
        )
    return menus

def setup(bot):
    bot.add_cog(journey_cog(bot))
    print("Journey cog loaded")

