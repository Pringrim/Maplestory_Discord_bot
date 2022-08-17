# variable.py는 숨김파일
import variable
import discord
from discord.ext import commands
import WebScraping

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
        title="도움말", description="호출하기\n!<명령어>",
        color=side_bar_color)
    result_Embed.add_field(name="!무릉, !시드, !유니온, !업적, !정보, !코디", value="Maple.gg 기준 정보를 불러옵니다.", inline=False)
    result_Embed.add_field(name="!추옵 <아이템 이름>", value="해당 무기의 추옵 정보를 불러옵니다.", inline=False)
    result_Embed.add_field(name="!추옵 <아이템 레벨>", value="해당 방어구의 추옵 정보를 불러옵니다.", inline=False)
    result_Embed.set_thumbnail(
        url=variable.spirit_of_stone_URL)
    await ctx.send(embed=result_Embed, reference=ctx.message)


@bot.command(aliases=["무릉", "무릉도장"])
async def show_MuLung(ctx, *name):
    if not len(name):
        return_Embed = discord.Embed(title="!무릉 <닉네임>\n!무릉도장 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 무릉 최고기록을 보여줍니다.",
                                     color=side_bar_color)
        return_Embed.set_footer(text="무릉도장 최고기록",
                                icon_url=variable.ICO_MuLung)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    name = name[0]
    User_Information = WebScraping.UserChar(name)

    print(User_Information.User_IMG_URL)
    # 캐릭터가 존재하지 않을 때
    if not User_Information.is_valid():
        return_Embed = discord.Embed(title="검색되지 않았어요!", description="잘못된 이름을 입력한 것 같아요.", color=side_bar_color)
        return_Embed.set_footer(text="무릉도장 최고기록",
                                icon_url=variable.ICO_MuLung)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    User_MuLung = User_Information.get_MuLung()

    # 무릉도장 기록이 없을 때
    if User_MuLung == None:
        return_Embed = discord.Embed(title="검색되지 않았어요!", description="기록이 존재하지 않아요.", color=side_bar_color)
        return_Embed.set_footer(text="무릉도장 최고기록",
                                icon_url=variable.ICO_MuLung)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    return_Embed = discord.Embed(title=name, description="", color=side_bar_color)
    return_Embed.add_field(name=f'{User_MuLung[0]} 층',
                           value=f'{User_MuLung[1]}\n{User_MuLung[2]} / {User_Information.User_Class}\n\n'
                                 f'서버 {User_MuLung[3]}\n전체 {User_MuLung[4]}\n\n{User_MuLung[5]}',
                           inline=False)

    return_Embed.set_thumbnail(url=User_Information.User_IMG_URL)
    return_Embed.set_footer(text="무릉도장 최고기록",
                            icon_url=variable.ICO_MuLung)
    await ctx.channel.send(embed=return_Embed, reference=ctx.message)


@bot.command(aliases=["시드", "더시드"])
async def show_TheSeed(ctx, *name):
    if not len(name):
        await ctx.channel.send(embed=discord.Embed(title="!시드 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 시드 최고기록을 보여줍니다.",
                                                   color=side_bar_color), reference=ctx.message)
        return

    name = name[0]

    User_Information = WebScraping.UserChar(name)
    # 캐릭터가 존재하지 않을 때
    if not User_Information.is_valid():
        return_Embed = discord.Embed(title="검색되지 않았어요!", description="잘못된 이름을 입력한 것 같아요.", color=side_bar_color)
        return_Embed.set_footer(text="더 시드 최고기록",
                                icon_url=variable.ICO_TheSeed)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    User_TheSeed = User_Information.get_TheSeed()
    # 더 시드 기록이 없을 때
    if User_TheSeed == None:
        return_Embed = discord.Embed(title="검색되지 않았어요!", description="기록이 존재하지 않아요.", color=side_bar_color)
        return_Embed.set_footer(text="더 시드 최고기록",
                                icon_url=variable.ICO_TheSeed)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    re = discord.Embed(title=name, description="", color=side_bar_color)
    re.add_field(name=f'해저 {User_TheSeed[0]} 층',
                 value=f'{User_TheSeed[1]}\n{User_TheSeed[2]} / {User_Information.User_Class}\n\n'
                       f'서버 {User_TheSeed[3]}\n전체 {User_TheSeed[4]}\n\n{User_TheSeed[5]}',
                 inline=False)
    re.set_thumbnail(url=User_Information.User_IMG_URL)
    re.set_footer(text="더 시드 최고기록",
                  icon_url=variable.ICO_TheSeed)

    await ctx.channel.send(embed=re, reference=ctx.message)
