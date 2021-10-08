import discord, os
import random
import youtube_dl
from discord.ext import commands


# set status
game = discord.Game("밤샘 코딩")
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game, intents=intents)

# 제비뽑기 참가용 임시 user data
global user
user = []

# command
@bot.command(aliases=['hi', '안녕'])
async def hello(ctx):
    await ctx.send(f'{ctx.author.mention} 안녕~ 씨부엉')

@bot.command(aliases=['도움말', 'h'])
async def 도움(ctx):
    embed = discord.Embed(title="씨부엉이", description="밤샘 코딩 하는 씨부엉이입니다.", color=0x4432a8) 
    embed.add_field(name="1. 인사", value='!hello, !안녕, !hi\n 부엉이에게 인사해보세요!')
    embed.add_field(name="2. 제비뽑기 참여", value='!참여\n 제비 뽑기에 참여합니다!')    
    
    await ctx.send(embed=embed)

@bot.command()
async def 참여(ctx):
    global user
    user_tmp = ctx.author.name+'#'+ctx.author.discriminator

    print(user)
    if user_tmp in user:
        await ctx.send(f'{ctx.author.mention} 이미 참여하셨습니다!')
    else:
        user.append(ctx.author.name+'#'+ctx.author.discriminator)
        await ctx.send(f'{ctx.author} 제비뽑기 참여 완료!')

@bot.command()
async def 초기화(ctx):
    global user
    user = []
    print(user)
    await ctx.send("참여자 초기화!")

@bot.command()
async def 참여자(ctx):
    global user
    await ctx.send(f'참여자 : {user}')

@bot.command(name='제비뽑기')
async def random_choice(ctx, count=1):
    """택 N 당첨"""
    global user
    results = [m for m in user ] 
    print(results)    
    if count > len(results) or count <= 0:
        await ctx.send('invalid data')
        return
    choices = random.choices(results,k=count)
    result = []
    for member in choices:
        result.append(member)
    await ctx.send(f'당첨 : {", ".join(result)}')

@bot.command(name='재생')
async def play(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
    	await channel.connect()
    	await ctx.send("음성 채널 입장 : " + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command(name='나가')
async def leave(ctx):
    await bot.voice_clients[0].disconnect()

@bot.command(name='일시정지')
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("이미 일시정지 중!")

@bot.command(name='다시 재생')
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("이미 재생 중!")
        
@bot.command(name='멈춰')
async def stop(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()
    else:
        await ctx.send("재생 중이지 않음!")

# read token
token_path = os.path.dirname(os.path.abspath(__file__))+'/token.txt'
t = open(token_path, "r", encoding='utf-8')
token = t.read()

bot.run(token)