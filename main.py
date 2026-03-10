import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="서버 관리"))
    print(f'관리 봇 [{bot.user.name}] 준비 완료!')



@bot.command()
@commands.has_permissions(moderate_members=True)
async def 격리(ctx, member: discord.Member, minutes: int, *, 사유="사유 미기재"):
    """명령어: !격리 @사용자 시간(분) 사유"""
    duration = timedelta(minutes=minutes)
    try:
        await member.timeout(duration, reason=사유)
        await ctx.send(f"**{member.display_name}**님이 {minutes}분 동안 격리되었습니다.\n사유: {사유}")
    except Exception as e:
        await ctx.send(f"격리 실패: {e}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def 추방(ctx, member: discord.Member, *, 사유="사유 미기재"):
    """명령어: !추방 @사용자 사유"""
    try:
        await member.kick(reason=사유)
        await ctx.send(f"🚪 **{member.display_name}**님을 서버에서 추방했습니다.\n사유: {사유}")
    except Exception as e:
        await ctx.send(f"추방 실패: {e}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: `!격리 @사용자 분` 또는 `!추방 @사용자` 형식으로 입력해 주세요.")

bot.run(TOKEN)