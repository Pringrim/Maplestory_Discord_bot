import variable
import discord
from discord.ext import commands

bot_token = variable.test_bot_token
bot = commands.Bot(command_prefix=["!"])
bot.remove_command('help')
side_bar_color = 0xFFBB00


@bot.event
async def on_ready():
    print(f'Login Bot - {bot.user}')  # 봇이 로그인 하면 로그인 정보를 출력


async def on_message(message):
    if message.author == bot.user:  # 봇이 보낸 메시지는 무시(유저만 받음)
        return


@bot.command(aliases=["도움", "help", "명령어", "기능"])
async def show_help(ctx):
    result_Embed = discord.Embed(
        title="도움말", description="호출하기\n! 또는 메!",
        color=side_bar_color)
    result_Embed.add_field(name="!무릉, !시드, !유니온, !업적, !정보, !코디", value="Maple.gg 기준 정보를 불러옵니다.", inline=False)
    result_Embed.add_field(name="!장비 <부위> <닉네임>", value="해당 캐릭터가 장착중인 장비의 정보를 불러옵니다.", inline=False)
    result_Embed.add_field(name="!추옵 <아이템 이름>", value="해당 장비의 추옵 정보를 불러옵니다.", inline=False)
    result_Embed.set_thumbnail(
        url="http://avatar.maplestory.nexon.com/Character/AJGFLJMCHABCFJCDDPGNOAAPMMFCEGJAGOFNMGJCFIPEADOJAKFIPKIPKBEBHANDDOHPGFNGCPDGFCIELEEGLGMKAOHIODJHJCDECDCDOMOOOLJICMJGAEGHCEMGEBCGHKMLNBFFMBLLDJDEPEBMODJAHOBGDIIFGDPJBNPPHKNEMGGDFAOOFPJPBHBCKKPNEJGOHDDKEGHDILEIEHMJNHMBMOAAKHGICJFAGOLAOMGCGMHEDPFFLLMKNCBBDGGO.png")
    await ctx.send(embed=result_Embed, reference=ctx.message)
