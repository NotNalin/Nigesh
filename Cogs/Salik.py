import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from rtadubai import Salik


async def plate_code(ctx: discord.AutocompleteContext):
    area = ctx.options["area"]
    if area:
        return Salik.plates(int(area))
    return []


class salik_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    salik = SlashCommandGroup("salik", description="Salik commands")

    @salik.command()
    @discord.option("area", str, description="plate area", choices=[discord.OptionChoice(j, str(i)) for i, j in Salik.AREAS.items()])
    @discord.option("code", str, description="plate code", autocomplete=plate_code)
    @discord.option("plate", str, description="plate number", max_length=5)
    @discord.option("mobile", str, description="Mobile number")
    async def balance(self, ctx, area, code, plate, mobile):
        await ctx.defer()
        try:
            balance = Salik.balance(code, plate, mobile, area=area)
            await ctx.respond(f"{balance} AED")
        except Exception as e:
            await ctx.respond(e)
            raise e

    @salik.command()
    async def expiry(self, ctx, plate):
        await ctx.defer()
        try:
            expiry = Salik.expiry(plate)
            await ctx.respond(expiry)
        except Exception as e:
            await ctx.respond(e)
            raise e


def setup(bot):
    bot.add_cog(salik_cog(bot))
    print("Salik cog loaded")
