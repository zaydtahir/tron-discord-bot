import os
import discord
from dotenv import load_dotenv
from commands import *
from commands import _setBotStatus, _scheduling, _mongoFunctions

command_prefix = "$"
emote_prefix = "!"
reaction_handler_prefix = "|"

prefixes = [command_prefix, emote_prefix]

commands = {
    command_prefix + "verify": verify,
    command_prefix + "confirm": confirm,
    command_prefix + "unverify": unverify,
    command_prefix + "setbirthday": set_birthday,
    command_prefix + "addduedate": add_due_date,
    command_prefix + "help": help_command,
    command_prefix + "setbedibotchannel": set_bedi_bot_channel,
    command_prefix + "ping": ping,
    command_prefix + "parse": parse_command,
    command_prefix + "addQuote": add_quote,
    command_prefix + "addquote": add_quote,
    command_prefix + "getQuotes": get_quotes,
    command_prefix + "getquotes": get_quotes,
    command_prefix + "getQuote": get_quotes,
    command_prefix + "getquote": get_quotes,
    command_prefix + "removequote": remove_quote,
    command_prefix + "adminverify": admin_verify,
    command_prefix + "removeduedate": remove_due_date,
    command_prefix + "forcebirthdays": force_birthdays,
    command_prefix + "say": say,
    command_prefix + "lockdown": lockdown,
    command_prefix + "unlock": unlock,
    command_prefix + "settings": settings,
    command_prefix + "getbirthdays": get_birthdays
}

reactionHandlers = {
    reaction_handler_prefix: quotes_reaction_handler,
}

intents = discord.Intents.all()
client = discord.Client(intents = intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await _mongoFunctions.init(client)
    await _setBotStatus.set_random_bot_status(client)
    await _scheduling.schedule_jobs(client)


@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    if ctx.content[0] in prefixes:
        if ctx.content.split(" ")[0] in commands:
            await commands[ctx.content.split(" ")[0]](ctx, client)


@client.event
async def on_raw_reaction_add(reaction_payload: discord.RawReactionActionEvent):
    if reaction_payload.member.bot:
        return

    message = await client.get_channel(reaction_payload.channel_id).fetch_message(reaction_payload.message_id)

    if message.author == client.user:
        if message.embeds[0].description.split(" ")[0] in reactionHandlers:
            await reactionHandlers[message.embeds[0].description.split(" ")[0]](reaction_payload, message)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    client.run(TOKEN)
