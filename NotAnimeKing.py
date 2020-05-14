import random
import json
from itertools import cycle
import youtube_dl
import discord
from discord.ext import commands, tasks

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

        return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix= get_prefix)
status = cycle(['Watching Twitch.tv/animejayking', 'Watching https://www.youtube.com/channel/UCNVE-ZKFKchrrayLgTtkrLA'])
players = {}

@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Watching https://www.youtube.com/channel/UCNVE-ZKFKchrrayLgTtkrLA'))
    print('bot is ready')

@client.command()
async def ping(ctx):
    await ctx. send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responeses = [' It is certain.',
                  'It is decidedly so.',
                  'Without a doubt.',
                  'Yes – definitely.',
                  'You may rely on it.',
                  'As I see it, yes',
                  'Most likely.',
                  'Outlook good.',
                  'Yes.',
                  'Signs point to yes.',
                  'Reply hazy, try again.',
                  'Ask again later.',
                  'Better not tell you now.',
                  'Cannot predict now.',
                  'Concentrate and ask again.',
                  "Don't count on it.",
                  'My reply is no.',
                  ' My sources say no',
                  'Outlook not so good.',
                  'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responeses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, ammount=5):
    await ctx.channel.purge(limit=ammount)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.sned(f'Banned User {member.mention}')



@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discrominator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discrominator):

            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@purge.error
async def on_command_error(ctx, error):
    if  isinstance(error, commands.MissingPermissions):
        await ctx.send('you cannot use that')

@kick.error
async def on_command_error(ctx, error):
    if  isinstance(error, commands.MissingPermissions):
        await ctx.send('you cannot use that')

@ban.error
async def on_command_error(ctx, error):
    if  isinstance(error, commands.MissingPermissions):
        await ctx.send('you cannot use that')

@unban.error
async def on_command_error(ctx, error):
    if  isinstance(error, commands.MissingPermissions):
        await ctx.send('you cannot use that')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command()
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

client.run('NzA5NTY0MTYyNzI0MDY5NDA2.Xro6fg.SIXANc6rqjYy_iBCR_FW3a1rdwM')
