import discord, asyncio, os
import random
from discord import activity
from discord.ext import commands


# set status
game = discord.Game("밤샘 코딩")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game, intents=intents)

# command
@bot.command(aliases=['hi', '안녕'])
async def hello(ctx):
    await ctx.send(f'{ctx.author} 안녕~ 씨부엉')

@bot.command(aliases=['도움말', 'h'])
async def 도움(ctx):
    embed = discord.Embed(title="씨부엉이", description="밤샘 코딩 하는 씨부엉이입니다.", color=0x4432a8) 
    embed.add_field(name="1. 인사", value='!hello, !안녕, !hi')
    
    await ctx.send(embed=embed)

@bot.command(aliases=['온라인'])
async def online(ctx):
    await ctx.send(ctx.guild.members)

@bot.command(name='제비뽑기')
async def random_choice(ctx, count=1):
    """택 N 당첨"""
    results = [m for m in ctx.guild.members if m.bot == False ] #and m.status == 'online'
    print(results)    
    if count > len(results) or count <= 0:
        await ctx.send('invalid data')
        return
    choices = random.choices(results,k=count)
    result = []
    for member in choices:
        result.append(member.mention)
    await ctx.send(f'당첨 : {", ".join(result)}')

# read token
token_path = os.path.dirname(os.path.abspath(__file__))+'/token.txt'
t = open(token_path, "r", encoding='utf-8')
token = t.read()

bot.run(token)