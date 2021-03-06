import os

import discord
from dotenv import load_dotenv

from commands import _mongoFunctions, _embedMessage, _email, _hashingFunctions
from commands import _util

load_dotenv()
os.environ['UW_API_KEY'] = os.getenv('UW_API_KEY')
from uwaterloodriver import UW_Driver

uw_driver = UW_Driver()


async def confirm(ctx: discord.Message, client: discord.Client):
    if not _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled']:
        replyEmbed = _embedMessage.create("Confirm Reply", "Verification is not enabled on this server!", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    # Verified users can't run $confirm. They are already verified (duh)
    if _mongoFunctions.is_user_id_linked_to_verified_user_in_guild(ctx.guild.id, ctx.author.id):
        replyEmbed = _embedMessage.create("Confirm Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    message_contents = _util.parse_message(ctx.content)

    if len(message_contents) != 2:
        await ctx.channel.send(embed = _embedMessage.create("Confirm Reply", "The syntax is invalid! Make sure it is in the format $confirm <confirmcode>", "red"))
        return

    uw_id = _mongoFunctions.get_uw_id_from_pending_user_id(ctx.guild.id, ctx.author.id)

    if uw_id is None:
        await ctx.channel.send(embed = _embedMessage.create("Confirm Reply", "You have not run $verify yet!", "red"))
        return

    unique_key = message_contents[1]
    if unique_key == _email.verificationCodes.get(ctx.author.id):
        # Removing this stuff since V2 API is deprecated

        # department = uw_driver.directory_people_search(uw_id)['department']

        # if department == "ENG/Mechanical & Mechatronics":
        #     await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name = "Tron"))
        # else:
        #     await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name = "Not Tron"))

        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name = _mongoFunctions.get_settings(ctx.guild.id)['verified_role']))
        _mongoFunctions.add_user_to_verified_users(ctx.guild.id, ctx.author.id, _hashingFunctions.hash_user_id(uw_id))
        _mongoFunctions.remove_user_from_pending_verification_users(ctx.guild.id, ctx.author.id)
        reply_embed = _embedMessage.create("Confirm reply", "You have been verified", "blue")
        await ctx.channel.send(embed = reply_embed)
        await ctx.author.send(embed = reply_embed)

    else:
        await ctx.channel.send(embed = _embedMessage.create("Confirm reply", "Invalid Code!", "red"))
