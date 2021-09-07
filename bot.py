import discord
from discord import channel
from discord.ext import commands,tasks
from discord.ext.commands import Bot
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
async def on_member_join(member):
    await bot.get_channel(852601007888531529).send(f"{member} has joined!!Everyone welcome {member}!!")
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
    helpEmbed.add_field(name="avatar",value="Displays the specified user's avatar")
    helpEmbed.add_field(name="purge",value="Purges specified number of messages")
    helpEmbed.add_field(name="kick",value="Kicks a member and sends to their dms the reason they were kicked")
    helpEmbed.add_field(name="ban",value="bans a member and sends to their dms the reason they were banned")
    helpEmbed.add_field(name=".",value="The Bot will now catch and delete messages that contain blacklisted words, by users in the server and send them a warning")
    helpEmbed.set_footer(text="Built by Eth")
    await ctx.send(embed=helpEmbed)

@help.command()
async def ping(ctx):
    pingEmbed=discord.Embed(title="Ping",description="Checks ur ping")
    pingEmbed.add_field(name="**Syntax**",value="x!ping")
    await ctx.send(embed=pingEmbed)

@help.command()
async def description(ctx):
    descEmbed=discord.Embed(title="Description",description="a description of the bot",color=discord.Colour.blurple())
    descEmbed.add_field(name="**Syntax**",value="x!description")
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

blacklisted_words=["fuck","sex","ntr","gay","lesbian","terrorist","bitch","slut","gore","bdsm","penis","vagina","cock","dick","pussy","ass"]

@bot.event
async def on_message(message):
    if message.content=="Im a new member":
        myEmbed=discord.Embed(title="XenoBot",description="This is a bot version 2.0",color=discord.Colour.blue())
        myEmbed.add_field(name="Major Changes",value="Version 2.0",inline=False)
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
    myEmbed=discord.Embed(title="XenoBot",description="This is a bot version 2.0",color=discord.Colour.blue())
    myEmbed.add_field(name="Major Changes",value="Version 2.0",inline=False)
    myEmbed.add_field(name="Date of Release",value="5th September 21",inline=False)
    myEmbed.set_footer(text=f"Command run by {ctx.author.name}")
    myEmbed.set_author(name="universalXeno")

    await ctx.message.channel.send(embed=myEmbed)

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


bot.run("ODc0NTk4MDY0NTU4NjAwMjMy.YRJS6w.JbCKl65Znti-mB0GsX3UAFtnGo4")