import discord
import asyncio
import random
import time
import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
token = 'your bot token'
ROLE = "Member"
UNVERIFIED = "Unverified"

def is_channel(ctx):
    return ctx.channel.id == channel_id

@bot.event
async def on_ready():
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)
    print('Servers connected to:')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!help'))

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=ROLE)
    role2 = discord.utils.get(member.guild.roles, name=UNVERIFIED)
    await member.add_roles(role, role2)

@bot.command(name='verify')
@commands.check(is_channel)
async def verify(ctx):
    unverified = discord.utils.get(ctx.guild.roles, name="Unverified") 
    if unverified in ctx.author.roles: 
        verify = discord.utils.get(ctx.guild.roles, name="Verified") 
        msg = await ctx.send('Verification has been sent in DMs')
        await msg.add_reaction('✅')
        e = discord.Embed(title='Please rewrite the code below to access the server.',description='**NOTE:** This is **Case and Space Sensitive**',color=0xfcf8f8)
        e.add_field(name='Code:',
                    value='xM863w2vQI',inline=False)
        await ctx.author.send(embed=e)

        def check(m):
            return m.content == 'xM863w2vQI'

        msg = await bot.wait_for('message', check=check)
        e = discord.Embed(color=0xfcf8f8)
        await ctx.author.remove_roles(unverified)
        e.add_field(name='Thank you for verifying!', value='You now have access to the server.')
        print(f'{ctx.author} has been successfully verified!')
        await ctx.author.send(embed=e)
        await ctx.author.add_roles(verify) 
    else:
        await ctx.send('You are already verified!')

bot.run(token)
