import discord
from discord import channel
from discord.ext import commands,tasks
from discord.ext.commands import Bot
from discord.ext.commands.core import command
from discord.gateway import DiscordClientWebSocketResponse
from discord.guild import Guild
from discord.utils import get

import json
import re
import os
import collections
import sys
import asyncio
import datetime
import traceback

from datetime import datetime
from discord.flags import Intents

intents=discord.Intents.default()
intents.members=True
intents.reactions=True
member=discord.Member
guild=discord.Guild.name

bot=Bot(command_prefix='x!',intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=" x!help"))

    print(f"Logged in as {bot.user.name}")
    print(bot.user.id)
    print(bot.user.name)

@bot.event
async def on_member_join(ctx,member):
    await ctx.send(f"{member} has joined!!Everyone welcome {member}!!")
    print("Welcome "+member.name+". They just joined the server!! Make sure to check out all our channels")
    await member.send(f"Welcome to the server!!our server is a lot of fun")

@bot.command(name='ping')
async def ping(ctx):
    await ctx.message.channel.send(f"Yo!!The ping is {round(bot.latency*100)}ms")

@bot.group(invoke_without_command=True)
async def help(ctx):
    helpEmbed=discord.Embed(title="Xenobot is here to help!",description="Use x!help <command> to see more info on a command",color=discord.Colour.green())
    helpEmbed.add_field(name="x!",value="x! is the prefix for Xenobot!!Run any command with x!<command> to get the command working..Have fun!!")
    helpEmbed.add_field(name="ping",value="Checks your ping")
    helpEmbed.add_field(name="description",value="Displays info on Xeno")
    helpEmbed.add_field(name="avatar",value="Displays the specified user's avatar")
    helpEmbed.add_field(name="purge",value="Purges specified number of messages")
    helpEmbed.add_field(name="kick",value="Kicks a member and sends to their dms the reason they were kicked")
    helpEmbed.add_field(name="ban",value="bans a member and sends to their dms the reason they were banned")
    helpEmbed.add_field(name="unban",value="unbans a member and sends to their dms that they were unbanned")
    helpEmbed.add_field(name=".",value="The Bot will now catch and delete messages that contain blacklisted words, by users in the server and send them a warning")
    helpEmbed.add_field(name="roles",value="Puts up the roles message")
    helpEmbed.add_field(name="mute",value="Mutes the member for a specific reason")
    helpEmbed.add_field(name="unmute",value="Unmutes the member that was previously muted")
    helpEmbed.set_footer(text="Built by Eth")
    await ctx.send(embed=helpEmbed)

@help.command()
async def ping(ctx):
    pingEmbed=discord.Embed(title="Ping",description="Checks ur ping")
    pingEmbed.add_field(name="**Syntax**",value="x!ping")
    await ctx.send(embed=pingEmbed)

@help.command()
async def description(ctx):
    descEmbed=discord.Embed(title="Description",description="A description of Xeno",color=discord.Colour.blurple())
    descEmbed.add_field(name="**Syntax**",value="x!description")
    descEmbed.add_field(name="Aliases",value="desc,d")
    await ctx.send(embed=descEmbed)

@help.command()
async def avatar(ctx):
    avatarEmbed=discord.Embed(title="Avatar",description="Provides the avatar of the mentioned user")
    avatarEmbed.add_field(name="**Syntax**",value="x!avatar <@Member Tag>")
    avatarEmbed.set_footer(text="Do not include the <> while mentionining the tag1")
    await ctx.send(embed=avatarEmbed)

@help.command()
async def purge(ctx):
    prgEmbed=discord.Embed(title="Purge",description="Purges Messages")
    prgEmbed.add_field(name="**Syntax**",value="x!purge <Number of Messages>")
    prgEmbed.add_field(name="Aliases",value="pg,p,del")
    prgEmbed.set_footer(text="NOTE: Only Fr Moderators, Admins and Owners")
    await ctx.send(embed=prgEmbed)

@help.command()
async def kick(ctx):
    kEmbed=discord.Embed(title="Kick",description="Kicks a User from the server")
    kEmbed.add_field(name="**Syntax**",value="x!kick <@Member> <Reason>")
    kEmbed.set_footer(text="NOTE: Only Fr Moderators, Admins and Owners")
    await ctx.send(embed=kEmbed)

@help.command()
async def ban(ctx):
    bEmbed=discord.Embed(title="Ban",description="Bans a User from the server")
    bEmbed.add_field(name="**Syntax**",value="x!ban <@Member> <Reason>")
    bEmbed.set_footer(text="NOTE: Only Fr Moderators, Admins and Owners")
    await ctx.send(embed=bEmbed)

@help.command()
async def unban(ctx):
    ubEmbed=discord.Embed(title="Unban",description="Unbans a previously banned user from the server")
    ubEmbed.add_field(name="**Syntax**",value="x!unban Member#id (Since they arent in the server anymore u cant tag them)")
    ubEmbed.set_footer(text="NOTE: Only Fr Moderators, Admins and Owners")
    await ctx.send(embed=ubEmbed)

@help.command()
async def roles(ctx):
    hlEmbed=discord.Embed(title="Roles",description="Summons a message containing reaction roles")
    hlEmbed.add_field(name="**Syntax**",value="x!roles")
    hlEmbed.set_footer(text="NOTE: Only Fr Admins and Owners")
    await ctx.send(embed=hlEmbed)

@help.command()
async def mute(ctx):
    mtEmbed=discord.Embed(title="Mute",description="Mutes a member as well as dms them the reason they were muted, also mentioning the name of the server they were muted in")
    mtEmbed.add_field(name="**Syntax**",value="x!mute <@Member> Reason")
    mtEmbed.set_footer(text="NOTE: Only Fr Admins and Owners")
    await ctx.send(embed=mtEmbed)

@help.command()
async def unmute(ctx):
    umtEmbed=discord.Embed(title="Unmute",description="Unmutes a member as well as dms them that they were successfully unmuted, also mentioning them not to repeat the same mistake again")
    umtEmbed.add_field(name="**Syntax**",value="x!unmute <@Member>")
    umtEmbed.set_footer(text="NOTE: Only Fr Admins and Owners")
    await ctx.send(embed=umtEmbed)

blacklisted_words=["fuck","sex","ntr","gay","lesbian","terrorist","bitch","slut","gore","bdsm","penis","vagina","cock","dick","pussy","ass"]

@bot.event
async def on_message(message):
    if message.content=="Im a new member":
        myEmbed=discord.Embed(title="Xeno",description="This is Xeno for you!!",color=discord.Colour.blue())
        myEmbed.set_thumbnail(url=bot.user.avatar_url)
        myEmbed.add_field(name="About Xeno",value="This is a server friendly moderation and entertainment bot that is user friendly and staff friendly. Run x!help to know more",inline=False)
        myEmbed.add_field(name="Date of Release",value="5th September 21",inline=False)
        myEmbed.set_footer(text="Built by Eth")
        myEmbed.set_author(name="universalXeno")

        await message.channel.send(embed=myEmbed)
    
    elif message.content.lower().startswith("imagine"):
        await message.channel.send(f"I cant even {message.content}")

    elif message.content.lower() in blacklisted_words:
        await message.delete()
        await message.channel.send("Please refrain from saying things like that in the future. This might invoke a tempmute or ban from the admins and owners")

    elif any(words in blacklisted_words for words in message.content.lower().split()):
        await message.delete()
        await message.channel.send("Please refrain from saying things like that in the future. This might invoke a tempmute or ban from the admins and owners")

    await bot.process_commands(message)  

@bot.command(name='description',aliases=["desc","d"])
async def description(ctx,member: discord.Member=None):
    dscEmbed=discord.Embed(title="Xeno",description="This is Xeno for you!!",color=discord.Colour.blue())
    dscEmbed.set_thumbnail(url=bot.user.avatar_url)
    dscEmbed.add_field(name="About Xeno",value="This is a server friendly moderation and entertainment bot that is user friendly and staff friendly. Run x!help to know more",inline=False)
    dscEmbed.add_field(name="Date of Release",value="5th September 21",inline=False)
    dscEmbed.set_footer(text="Built by Eth")
    dscEmbed.set_author(name="universalXeno")

    await ctx.message.channel.send(embed=dscEmbed)

@bot.command(aliases=["av"])
async def avatar(ctx,*,member: discord.Member=None):
    member=ctx.author if not member else member
    avEmbed=discord.Embed(title=f"Avatar of {member.name}",color=member.color,timestamp=ctx.message.created_at)
    avEmbed.set_image(url=member.avatar_url)
    avEmbed.set_footer(text=f"Command run by {ctx.author}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=avEmbed)

@bot.command(aliases=["pg","p","del"])
@commands.has_permissions(manage_messages=True)
async def purge(ctx,amount=35):
    if amount>500:
        await ctx.send("Whoa!! Chill out..delete only 500 at once")
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount} messages")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member: discord.Member=None,*,reason="No reason provided"):
    await member.send(f"You have been kicked!!. Reason being: {reason}")
    await member.kick(reason=reason)
    await ctx.send(f"User {member} was successfully kicked!!")

@kick.error
async def kick_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("Sorry u dont have the permissions to kick people! Why u trying to kick bro?")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,member: discord.Member=None,*,reason="No reason provided"):
    await member.send(f"You have been banned!!. Reason being: {reason}")
    await member.ban(reason=reason)
    await ctx.send(f"User {member.mention} was successfully banned!!")

@ban.error
async def ban_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("Sorry u dont have the permissions to ban people! Why u trying to ban bro?")

@bot.command()
async def unban(ctx,*,member):
    banned_users=await ctx.guild.bans()
    member_name,member_discriminator=member.split('#')

    for ban_entry in banned_users:
        user=ban_entry.user

        if(user.name,user.discriminator)==(member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f" Unbanned {user.name}#{user.discriminator}")
            return


@bot.command()
@commands.has_role("ADMIN")
async def roles(ctx):
    reactEmbed=discord.Embed(
        title="Welcome to Dank on ARRIVAL!!\n🏛️ Heist Ping\n🎉 Giveaway Ping\n📢 Announcements Ping\n🙌 Events Ping\n❓ Poll Ping",
        description="React with respective emojis to get roles",
        color=discord.Colour.red(),
        timestamp=datetime.now()
    )

    message=await ctx.send(embed=reactEmbed)
    await message.add_reaction('🏛️')
    await message.add_reaction('🎉')
    await message.add_reaction('📢')
    await message.add_reaction('🙌')
    await message.add_reaction('❓')

    await ctx.message.add_reaction('💖')

@bot.event
async def on_raw_reaction_add(payload):
    messageId=884752218731999312

    if messageId==payload.message_id:
        member=payload.member
        guild=member.guild
        emoji=payload.emoji.name

        if emoji=='🏛️':
            role=discord.utils.get(guild.roles,name="Heist Ping")
        elif emoji=='🎉':
            role=discord.utils.get(guild.roles,name="Giveaway Ping")
        elif emoji=='🙌':
            role=discord.utils.get(guild.roles,name="Event Ping")
        elif emoji=='📢':
            role=discord.utils.get(guild.roles,name="Announcement Ping")
        elif emoji=='❓':
            role=discord.utils.get(guild.roles,name="Poll Ping")

        await member.add_roles(role)

@bot.command()
async def on_raw_reaction_remove(payload):
    messageId=884752218731999312

    if messageId==payload.message_id:
        guild=await(bot.fetch_guild(payload.guild_id))
        emoji=payload.emoji.name
        if emoji=='🏛️':
            role=discord.utils.get(guild.roles,name="Heist Ping")
        elif emoji=='🎉':
            role=discord.utils.get(guild.roles,name="Giveaway Ping")
        elif emoji=='🙌':
            role=discord.utils.get(guild.roles,name="Event Ping")
        elif emoji=='📢':
            role=discord.utils.get(guild.roles,name="Announcement Ping")
        elif emoji=='❓':
            role=discord.utils.get(guild.roles,name="Poll Ping")
        member=await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print("Member not found")

@bot.command(aliases=["ui","info","user","uinfo"])
async def userinfo(ctx,member: discord.Member):

    auEmbed=discord.Embed(title="USER INFO", description=f"This is the userinfo of the requested user",color=member.color,timestamp=ctx.message.created_at)
    auEmbed.set_thumbnail(url=member.avatar_url)
    auEmbed.add_field(name="NAME",value=member.display_name,inline=False)
    auEmbed.add_field(name="NICKNAME",value=member.nick,inline=False)
    auEmbed.add_field(name="ID",value=member.id,inline=False)
    auEmbed.add_field(name="STATUS",value=member.status,inline=False)
    auEmbed.add_field(name="TOP ROLE",value=member.top_role.name,inline=False)
    await ctx.send(embed=auEmbed)

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")
    


bot.run("ODc0NTk4MDY0NTU4NjAwMjMy.YRJS6w.JbCKl65Znti-mB0GsX3UAFtnGo4")
