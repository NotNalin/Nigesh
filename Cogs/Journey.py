import discord
from discord.ext import commands, pages
from rtadubai import Shail


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
        await ctx.defer()
        try:
            stop = Shail.Stop(name=stop)
            departures = Shail.departures(stop)
        except Exception as e:
            await ctx.respond(e)
            return
        if len(departures) == 0:
            await ctx.respond(f"No departures found for {stop.name}") 
        paginator = pages.Paginator(pages=departure_embeds(departures, stop))
        await paginator.respond(ctx.interaction)

    @commands.slash_command()
    @discord.option(name='fromstop', type=str, description="From stop", autocomplete=stop_searcher)
    @discord.option(name='tostop', type=str, description="To stop", autocomplete=stop_searcher)
    async def journey(self, ctx, fromstop, tostop):
        await ctx.defer()
        try:
            fromstop = Shail.Stop(name=fromstop)
            tostop = Shail.Stop(name=tostop)
            journey = Shail.journey_planner(fromstop, tostop)
        except Exception as e:
            await ctx.respond(e)
            return
        paginator = pages.Paginator(pages=journey_embeds(journey), show_menu=True, menu_placeholder="Select a Journey")
        await paginator.respond(ctx.interaction)
    
    @commands.Cog.listener()
    async def on_application_command_error(self, error):
        if isinstance(error, discord.errors.NotFound):
            pass
        else:
            raise error


def departure_embeds(departures, stop):
    embeds = []
    for departure in departures:
        embed = discord.Embed(title=f"{stop.name}", description=f"Departures at {stop.name}")
        embed.add_field(name="Mode", value=departure["mode"], inline=False)
        embed.add_field(name="Type", value=departure["type"], inline=False)
        embed.add_field(name="Direction", value=departure["direction"], inline=False)
        embed.add_field(name="Scheduled Time", value=departure["scheduled_time"], inline=False)
        embed.add_field(name="Estimated Time", value=departure["estimated_time"], inline=False)
        embed.add_field(name="Status", value=departure["status"], inline=False)
        embeds.append(embed)
    return embeds


def journey_embeds(journeys):
    menus = []
    for journey in journeys:
        embeds = []
        embed = discord.Embed()
        embed.title = "Journey Planner"
        embed.add_field(name="Staring From", value=journey["startstop"], inline=False)
        embed.add_field(name="Destination", value=journey["endstop"], inline=False)
        embed.add_field(name="Starting Time", value=journey["starttime"], inline=False)
        embed.add_field(name="Ending Time", value=journey["endtime"], inline=False)
        embed.add_field(name="Duration", value=journey["duration"], inline=False)
        embed.add_field(name="Amount", value=journey["amount"], inline=False)
        embeds.append(embed)
        for i in journey['journeys']:
            embed = discord.Embed()
            embed.add_field(name="Starting Time", value=i["starttime"], inline=False)
            embed.add_field(name="Ending Time", value=i["endtime"], inline=False)
            embed.add_field(name="From", value=i["from"], inline=False)
            embed.add_field(name="To", value=i["to"], inline=False)
            embed.add_field(name="Method", value=i["method"], inline=False)
            embed.add_field(name="Mode", value=i["mode"], inline=False)
            embed.add_field(name="Duration", value=i["duration"], inline=False)
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
