import discord

from commands import _mongoFunctions, _embedMessage, _checkrole, _util


async def admin_verify(ctx: discord.Message, client: discord.Client):
    # Checks if user is admin or bot owner
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("AdminVerify Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    if not _mongoFunctions.get_settings(ctx.guild.id)['verification_enabled']:
        replyEmbed = _embedMessage.create("AdminVerify Reply", "Verification is not enabled on this server!", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    message_contents = ctx.content.split(" ")

    if len(message_contents) != 2:
        await ctx.channel.send(embed = _embedMessage.create("AdminVerify Reply",
                                                            "The syntax is invalid! Make sure it is in the format $adminverify <User (Mention)>\nNote that this command does NOT assign a role, it only verifies them inside the database!",
                                                            "red"))
        return

    mention = message_contents[1]

    # Removes special characters from mention to end up with the user id
    user_id = mention.replace("<", "").replace(">", "").replace("@", "").replace("!", "")

    _mongoFunctions.admin_add_user_to_verified_users(ctx.guild.id, user_id)
    await ctx.guild.get_member(user_id).add_roles(discord.utils.get(ctx.guild.roles, name = _mongoFunctions.get_settings(ctx.guild.id)['verified_role']))
    await ctx.channel.send(embed = _embedMessage.create("AdminVerify reply", mention + "has been verified", "blue"))
