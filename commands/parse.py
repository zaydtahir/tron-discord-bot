import discord

from ._util import parse_message


async def parse_command(ctx: discord.Message, client: discord.Client):
    args = parse_message(ctx.content)
    msg = ""
    num = 0
    for arg in args:
        msg += "arg " + str(num) + " : " + arg + "\n"
        num += 1
    await ctx.channel.send(msg)
