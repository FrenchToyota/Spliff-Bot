import asyncio
from this import d
import aiohttp
import psutil
import os
import sys
import time
import traceback
import random
import discord
from discord.ext import commands
import datetime
import time
import json
import sqlite3


bot = commands.Bot(command_prefix='!')

bot.remove_command('help')

os.system('cls' if os.name == 'nt' else 'clear')
    

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')




@bot.event
async def on_member_join(member):
    embed = discord.Embed(title="Welcome to the server, {}!".format(member.name), description="Thanks for joining {}!".format(member.server.name), color=0x00ff00)
    embed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(member, embed=embed)
    await bot.send_message(member.server.default_channel, "{} has joined the server!".format(member.name))

@bot.command()
async def avatar(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f'{member}', color=0x00ff00)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def time(ctx):
    embed = discord.Embed(title=f'Time', color=0x00ff00)
    embed.add_field(name='Time', value=datetime.datetime.now().strftime("%H:%M:%S"))
    await ctx.send(embed=embed)

@bot.command()
async def log(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel
    await channel.send('Logging started.')
    async for message in channel.history(limit=None):
        with open('log.txt', 'a') as f:
            f.write(f'{message.created_at} - {message.author.name}: {message.content}\n')
    await channel.send('Logging stopped.')


@bot.command()
async def ban(ctx, member: discord.Member, *, reason: str):
    embed = discord.Embed(title=f'{member}', color=0x00ff00)
    embed.add_field(name='Banned', value=f'Reason: {reason}')
    await ctx.send(embed=embed)
    with open('banned.txt', 'a') as f:
        f.write(f'{member.id} - {reason}\n')

@bot.command()
async def number(ctx):
    number = random.randint(1, 10)
    while True:
        await ctx.send(f'Guess a number between 1 and 10:')
        guess = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        guess = int(guess.content)
        if guess == number:
            await ctx.send('You guessed it!')
            break
        else:
            await ctx.send(f'You guessed {guess}, but the number was {number}')


@bot.command()
async def coinflip(ctx):
    await ctx.send('Flip a coin')
    await ctx.send('Choose: heads or tails')
    while True:
        await ctx.send('Choose: heads or tails')
        choice = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        choice = choice.content.lower()
        if choice == 'heads':
            await ctx.send('You chose heads')
            break
        elif choice == 'tails':
            await ctx.send('You chose tails')
            break
        else:
            await ctx.send('Invalid choice')
    await ctx.send('I choose tails')
    if choice == 'heads':
        await ctx.send('You win!')
    elif choice == 'tails':
        await ctx.send('I win!')
    else:
        await ctx.send('Invalid choice')


@bot.command()
async def coinflipgame(ctx, member: discord.Member):
    await ctx.send(f'{ctx.author.name} has challenged {member.name} to a game of heads or tails')
    await ctx.send('Choose: heads or tails')
    while True:
        await ctx.send('Choose: heads or tails')
        choice = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        choice = choice.content.lower()
        if choice == 'heads':
            await ctx.send('You chose heads')
            break
        elif choice == 'tails':
            await ctx.send('You chose tails')
            break
        else:
            await ctx.send('Invalid choice, select a user to challenge')

@bot.command()
async def rpsgame(ctx, member: discord.Member):
    await ctx.send(f'{ctx.author.name} has challenged {member.name} to a game of rock paper scissors')
    await ctx.send('Choose: rock, paper, scissors')
    while True:
        await ctx.send('Choose: rock, paper, scissors')
        choice = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        choice = choice.content.lower()
        if choice == 'rock':
            await ctx.send('You chose rock')
            break
        elif choice == 'paper':
            await ctx.send('You chose paper')
            break
        elif choice == 'scissors':
            await ctx.send('You chose scissors')
            break
        else:
            await ctx.send('Invalid choice, select a user to challenge')


@bot.command()
async def rps(ctx):
    await ctx.send('Rock, Paper, Scissors')
    await ctx.send('Choose: rock, paper, scissors')
    while True:
        await ctx.send('Choose: rock, paper, scissors')
        choice = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        choice = choice.content.lower()
        if choice == 'rock':
            await ctx.send('You chose rock')
            break
        elif choice == 'paper':
            await ctx.send('You chose paper')
            break
        elif choice == 'scissors':
            await ctx.send('You chose scissors')
            break
        else:
            await ctx.send('Invalid choice')
    await ctx.send('I choose rock')
    if choice == 'rock':
        await ctx.send('It\'s a tie!')
    elif choice == 'paper':
        await ctx.send('You win!')
    elif choice == 'scissors':
        await ctx.send('I win!')
    else:
        await ctx.send('Invalid choice')

@bot.command()
async def serverstats(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', color=0x00ff00)
    embed.add_field(name='Members', value=f'{ctx.guild.member_count}')
    embed.add_field(name='Channels', value=f'{len(ctx.guild.channels)}')
    embed.add_field(name='Roles', value=f'{len(ctx.guild.roles)}')
    embed.add_field(name='Emojis', value=f'{len(ctx.guild.emojis)}')
    await ctx.send(embed=embed)

@bot.command()
async def createticket(ctx, *, name: str):
    await ctx.guild.create_text_channel(name)
    await ctx.send(f'Channel {name} created')

@bot.command()
async def countmsgs(ctx):
    await ctx.send(f'There are {len(ctx.channel.history)} messages in this channel')


@bot.command()
async def countup(ctx, number: int):
    for i in range(number):
        await ctx.send(i)

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f'Connected to {channel}')


@bot.command()
async def countusers(ctx):
    await ctx.send(f'There are {len(ctx.guild.members)} users in this server')
    with open('users.txt', 'a') as f:
        f.write(f'{len(ctx.guild.members)}\n')

@bot.command()
async def createrole(ctx, *, name: str):
    await ctx.guild.create_role(name=name, color=discord.Color.blue())
    await ctx.send(f'Role {name} created')

@bot.command()
async def mostemoji(ctx):
    emoji_count = {}
    for emoji in ctx.guild.emojis:
        if emoji.name in emoji_count:
            emoji_count[emoji.name] += 1
        else:
            emoji_count[emoji.name] = 1
    emoji_count = sorted(emoji_count.items(), key=lambda x: x[1], reverse=True)
    await ctx.send(f'{emoji_count[0][0]} is the most popular emoji in this server')

@bot.command()
async def vote(ctx, member: discord.Member):
    await ctx.send(f'{ctx.author.name} has voted for {member.name}')
    with open('votes.txt', 'a') as f:
        f.write(f'{ctx.author.name} voted for {member.name}\n')

@bot.command()
async def countvotes(ctx, member: discord.Member):
    with open('votes.txt', 'r') as f:
        votes = f.readlines()
    votes = [vote.split(' ') for vote in votes]
    votes = [vote for vote in votes if vote[0] == member.name]
    await ctx.send(f'{member.name} has {len(votes)} votes')

# fetch info from the API and display it in a embed
@bot.command()
async def weather(ctx, *, city: str):
    api_key = 'bafd01b286c82f7894a1050cf0e8d326'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
    embed = discord.Embed(title=f'{data["name"]}', color=0x00ff00)
    embed.add_field(name='Temperature', value=f'{data["main"]["temp"]} K')
    embed.add_field(name='Humidity', value=f'{data["main"]["humidity"]} %')
    embed.add_field(name='Wind Speed', value=f'{data["wind"]["speed"]} m/s')
    embed.add_field(name='Weather', value=f'{data["weather"][0]["description"]}')
    await ctx.send(embed=embed)
 

@bot.command()
async def verify(ctx):
    await ctx.send('Verified')
    role = discord.utils.get(ctx.guild.roles, name='Verified')
    await ctx.author.add_roles(role)
    await ctx.send('You have been verified')
    with open('verify.txt', 'a') as f:
        f.write(f'{ctx.author.name}\n')

@bot.command()
async def wordcount(ctx, *, word: str):
    with open('wordcount.txt', 'r') as f:
        words = f.readlines()
    words = [word.split(' ') for word in words]
    words = [word for word in words if word[0] == word]
    await ctx.send(f'{word} has been said {len(words)} times')
    with open('count.txt', 'a') as f:
        f.write(f'{word}\n')

@bot.command()
async def usercount(ctx):
    with open('count.txt', 'r') as f:
        words = f.readlines()
    words = [word.split(' ') for word in words]
    words = [word for word in words if word[0] == word]
    await ctx.send(f'There are {len(words)} people in this server')
    with open('count.txt', 'a') as f:
        f.write(f'{ctx.author.name}\n')

@bot.command()
async def allverifiedusers(ctx):
    with open('verify.txt', 'r') as f:
        users = f.readlines()
    users = [user.split(' ') for user in users]
    users = [user for user in users if user[0] == user]
    await ctx.send(f'{len(users)} users have verified their account')
    for user in users:
        await ctx.send(user[0])

@bot.command()
async def stats(ctx):
    embed = discord.Embed(title='CPU Usage', color=0x00ff00)
    embed.add_field(name='CPU Usage', value=f'{psutil.cpu_percent()}%')
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    embed = discord.Embed(title=f'{ctx.guild.name}', color=0x00ff00)
    embed.add_field(name='Server ID', value=f'{ctx.guild.id}')
    embed.add_field(name='Owner', value=f'{ctx.guild.owner}')
    embed.add_field(name='Member Count', value=f'{len(ctx.guild.members)}')
    embed.add_field(name='Region', value=f'{ctx.guild.region}')
    embed.add_field(name='Verified', value=f'{ctx.guild.verification_level}')
    embed.add_field(name='Created At', value=f'{ctx.guild.created_at}')
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(title=f'{member.name}', color=0x00ff00)
    embed.add_field(name='User ID', value=f'{member.id}')
    embed.add_field(name='Joined At', value=f'{member.joined_at}')
    embed.add_field(name='Status', value=f'{member.status}')
    embed.add_field(name='Roles', value=f'{member.roles}')
    embed.add_field(name='Bot', value=f'{member.bot}')
    await ctx.send(embed=embed)

@bot.command()
async def commands(ctx):
    with open('commands.txt', 'r') as f:
        commands = f.readlines()
    commands = [command.split(' ') for command in commands]
    commands = [command for command in commands if command[0] == command]
    await ctx.send(f'{len(commands)} commands have been executed')
    with open('commands.txt', 'a') as f:
        f.write(f'{ctx.message.content}\n')

@bot.command()
async def uptime(ctx):
    await ctx.send(f'{bot.uptime}')
 
@bot.command()
async def sql(ctx, *, query: str):
    conn = sqlite3.connect('sql.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.commit()
    conn.close()
    embed = discord.Embed(title=f'{query}', color=0x00ff00)
    for row in result:
        embed.add_field(name=f'{row[0]}', value=f'{row[1]}')
    await ctx.send(embed=embed)
    with open('sql.txt', 'a') as f:
        f.write(f'{query}\n')


@bot.command()
async def createuser(ctx, *, user: str):
    conn = sqlite3.connect('sql.db')
    c = conn.cursor()
    c.execute(f'CREATE TABLE IF NOT EXISTS {user} (id TEXT, level INTEGER)')
    conn.commit()
    conn.close()
    with open('sql.txt', 'a') as f:
        f.write(f'CREATE TABLE IF NOT EXISTS {user}\n')
    await ctx.send(f'{user} has been created')

# input data into sql database
@bot.command()
async def inputsql(ctx, *, query: str):
    conn = sqlite3.connect('sql.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
    with open('sql.txt', 'a') as f:
        f.write(f'{query}\n')

# delete data from sql database
@bot.command()
async def deletesql(ctx, *, query: str):
    conn = sqlite3.connect('sql.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
    with open('sql.txt', 'a') as f:
        f.write(f'{query}\n')
    
@bot.command()
async def ping(ctx):
    await ctx.send(f'{bot.latency}')
    with open('ping.txt', 'a') as f:
        f.write(f'{bot.latency}\n')

@bot.command()
async def prices(ctx, *, cryptocurrencies: str):
    cryptocurrencies = cryptocurrencies.split(' ')
    embed = discord.Embed(title='Prices', color=0x00ff00)
    for cryptocurrency in cryptocurrencies:
        url = f'https://api.coinmarketcap.com/v1/ticker/{cryptocurrency}/'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        embed.add_field(name=f'{cryptocurrency}', value=f'{data[0]["price_usd"]}')
    await ctx.send(embed=embed)
    with open('prices.txt', 'a') as f:
        f.write(f'{cryptocurrencies}\n')

@bot.command()
async def level(ctx, *, member: discord.Member):
    with open('level.txt', 'r') as f:
        levels = f.readlines()
    levels = [level.split(' ') for level in levels]
    levels = [level for level in levels if level[0] == level]
    for level in levels:
        if level[0] == member.id:
            await ctx.send(f'{member.name} is level {level[1]}')
            return
    await ctx.send(f'{member.name} is level 0')
    with open('level.txt', 'a') as f:
        f.write(f'{member.id} 0\n')

@bot.command()
async def changelevel(ctx, *, member: discord.Member):
    with open('level.txt', 'r') as f:
        levels = f.readlines()
    levels = [level.split(' ') for level in levels]
    levels = [level for level in levels if level[0] == level]
    for level in levels:
        if level[0] == member.id:
            levels.remove(level)
            with open('level.txt', 'w') as f:
                for level in levels:
                    f.write(f'{level[0]} {level[1]}\n')
            await ctx.send(f'{member.name} is now level {level[1]}')
            return
    await ctx.send(f'{member.name} is level 0')
    with open('level.txt', 'a') as f:
        f.write(f'{member.id} 0\n')

@bot.command()
async def shutdown(ctx):
    await ctx.send('Shutting down')
    await bot.logout()
    with open('shutdown.txt', 'a') as f:
        f.write(f'{ctx.message.content}\n')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Help', color=0x00ff00)
    embed.add_field(name='ping', value='Returns the bot\'s latency')
    embed.add_field(name='prices', value='Returns the current price of a cryptocurrency')
    embed.add_field(name='level', value='Returns the level of a user')
    embed.add_field(name='changelevel', value='Changes the level of a user')
    embed.add_field(name='stats', value='Stats of the bot')
    embed.add_field(name='serverstats', value='Stats of the server')
    embed.add_field(name='createuser', value='Creates a user in the database')
    embed.add_field(name='inputsql', value='Inputs data into the database')
    embed.add_field(name='deletesql', value='Deletes data from the database')
    embed.add_field(name='sql', value='Returns data from the database')
    embed.add_field(name='wordcount', value='Shows how many words a channel has')
    embed.add_field(name='log', value='Logs all messages in a channel')
    embed.add_field(name='avatar', value='Sends a users avatar')
    embed.add_field(name='time', value='Sends the current time')
    embed.add_field(name='rps', value='Plays rock paper scissors with the bot')
    embed.add_field(name='coinflip', value='Coinflips a coin against the bot')
    embed.add_field(name='number', value='Guess a number between 1 and 10 and win a prize')
    embed.add_field(name='uptime', value='Returns the bot\'s uptime')
    embed.add_field(name='commands', value='Returns the number of commands executed')
    embed.add_field(name='help', value='Returns this message')
    embed.add_field(name='shutdown', value='Shuts down the bot')
    await ctx.send(embed=embed)

bot.run('OTk2MDk2NzQ0MTkyNDk1NjU2.G4hIYo.UZv3e_R0E0QmGzBVShK-CO7rSUUpF1U-u1SHdE')
