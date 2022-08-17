#variable.py는 숨김파일
import variable
import discord
from discord.ext import commands
import WebScraping

import requests
from bs4 import BeautifulSoup

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
        url="https://raw.githubusercontent.com/Pringrim/Maplestory_Discord_bot/main/img/spirit_of_stone.png")
    await ctx.send(embed=result_Embed, reference=ctx.message)

@bot.command(aliases=["무릉", "무릉도장"])
async def mu(ctx, *name):
    if not len(name):
        await ctx.channel.send(
            embed=discord.Embed(title="!무릉 <닉네임>\n!무릉도장 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 무릉 최고기록을 보여줍니다.",
                                color=side_bar_color), reference=ctx.message)
        return

    name = name[0]
    bs = BeautifulSoup(requests.get(f'https://maple.gg/u/{name}').text, "html.parser")
    if len(bs.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div.text-secondary")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="기록이 없거나 갱신되지 않았을 수 있습니다."),
                               reference=ctx.message)
        return

    user_information = bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div > div > h1")
    if not len(user_information):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="캐릭터 이름을 확인해주세요."),
                               reference=ctx.message)
        return

    user_floor = str(user_information)[49:str(user_information)[49:].find(" ") + 48]  # 무릉 층수 구하기

    user_time_tmp = bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div > div > small")
    user_time = str(user_time_tmp)[38:str(user_time_tmp).find("초") + 1]  # 무릉 시간 구하기

    user_level_tmp = bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > footer > div.d-block.mb-1 > span")
    user_level = str(user_level_tmp[0])[6:str(user_level_tmp[0]).find("\n")]  # 무릉 레벨 구하기

    user_job = str(user_level_tmp[0])[str(user_level_tmp).rfind(" "):-7]

    user_rank_tmp = bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > footer > div.mb-2")
    user_server_rank = str(user_rank_tmp[0])[
                       str(user_rank_tmp[0]).find("<span>") + 6:str(user_rank_tmp[0]).find("위") + 1]
    user_rank = str(user_rank_tmp[0])[str(user_rank_tmp[0]).rfind("<span>") + 6:str(user_rank_tmp[0]).rfind("위") + 1]

    user_date_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > footer > div.user-summary-date > span")[
                            0])
    user_date = user_date_tmp[user_date_tmp.find(": ") + 2:user_date_tmp.rfind("일") + 1]

    user_pic_tmp = str(bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-4.pt-1.pt-sm-0.pb-1.pb-sm-0.text-center.mt-2.mt-lg-0 > div > div.col-6.col-md-8.col-lg-6 > img")[
                           0])
    user_pic_url = user_pic_tmp[user_pic_tmp.find("https:"):user_pic_tmp.rfind(".png") + 4].replace("s", "", 1)

    re = discord.Embed(title=name, description="", color=side_bar_color)
    re.add_field(name=f'{user_floor} 층',
                 value=f'{user_time}\n{user_level} / {user_job}\n\n서버 {user_server_rank}\n전체 {user_rank}\n\n기준일 : {"20" + user_date if user_date != "오늘" else user_date}',
                 inline=False)
    re.set_thumbnail(url=user_pic_url)
    re.set_footer(text="무릉도장 최고기록",
                  icon_url="https://w.namu.la/s/ea22206ca91fa53dc3903f65d6a462ba87788a36a15913b4f2f30666af1a6c1c6534f93334c4b88913651b5398a066c3cc8fc07c505d2d693ef6e901a83615eeca783261675ea33f33fc5c49f25df79a9a0f07772c9244a3e4668e644f93d40c")
    await ctx.channel.send(embed=re, reference=ctx.message)