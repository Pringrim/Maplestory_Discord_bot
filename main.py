import bot as botpy
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

token = botpy.bot_token
side_bar_color = 0xFFBB00
botpy.bot.run(token)

@botpy.bot.command(aliases=["!", "정보"])
async def information(ctx, *name):
    if not len(name):
        await ctx.channel.send(
            embed=discord.Embed(title="!! <닉네임>\n!정보 <닉네임>",
                                description="Maple.gg 기준 해당 캐릭터의 레벨, 직업, 인기도, 길드 정보를 보여줍니다.", color=side_bar_color),
            reference=ctx.message)
        return
    name = name[0]
    bs = BeautifulSoup(requests.get(f'https://maple.gg/u/{name}').text, "html.parser")

    if not len(bs.select("#user-profile > section > div.row.row-normal > div.col-lg-8 > h3 > img")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="캐릭터 이름을 확인해주세요."),
                               reference=ctx.message)
        return

    update_date_tmp = str(bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-8 > div.mt-2.text-right.clearfix > div.float-left.font-size-12.text-left > span.d-block.font-weight-light")[
                              0])
    update_date = update_date_tmp[update_date_tmp.find(":") + 1:update_date_tmp.rfind("\n")].strip()

    user_ch_tmp = str(bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-4.pt-1.pt-sm-0.pb-1.pb-sm-0.text-center.mt-2.mt-lg-0 > div > div.col-6.col-md-8.col-lg-6 > img")[
                          0])
    user_ch = user_ch_tmp[user_ch_tmp.find("http"):user_ch_tmp.rfind("png") + 3]

    user_server_icon_tmp = str(bs.select("#user-profile > section > div.row.row-normal > div.col-lg-8 > h3 > img")[0])
    user_server_icon_url = user_server_icon_tmp[user_server_icon_tmp.find("https:"):user_server_icon_tmp.rfind(" ") - 1]
    user_server = user_server_icon_tmp[user_server_icon_tmp.find("alt=") + 5:]
    user_server = user_server[:user_server.find("class") - 2]

    user_level_tmp = str(bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-8 > div.user-summary > ul > li:nth-child(1)")[0])
    user_level = user_level_tmp[user_level_tmp.find("Lv."):user_level_tmp.find(")") + 1]

    user_job_tmp = str(bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-8 > div.user-summary > ul > li:nth-child(2)")[0])
    user_job_tmp = user_job_tmp[:user_job_tmp.rfind("</li>")]
    user_job = user_job_tmp[user_job_tmp.rfind(">") + 1:]

    user_po_tmp = str(bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-8 > div.user-summary > ul > li:nth-child(3) > span:nth-child(2)")[
                          0])
    user_po = user_po_tmp[6:-7]

    user_guild_tmp = bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-8 > div.row.row-normal.user-additional > div.col-lg-2.col-md-4.col-sm-4.col-12.mt-3 > a")
    if not len(user_guild_tmp):
        user_guild = "-"
    else:
        user_guild_tmp = str(user_guild_tmp[0])[:-4]
        user_guild = user_guild_tmp[user_guild_tmp.rfind(">") + 1:]

    re = discord.Embed(title=name, description="", color=side_bar_color)
    re.add_field(name=f'{user_server}',
                 value=f'{user_level} / {user_job}\n\n길드{" : " + user_guild if user_guild != "-" else "없음"}\n인기도 : {user_po}',
                 inline=False)
    re.set_thumbnail(url=user_ch.replace("s", "", 1))
    re.set_footer(text=f'마지막 갱신 : {update_date}', icon_url=user_server_icon_url.replace("s", "", 1))

    await ctx.channel.send(embed=re, reference=ctx.message)


@botpy.bot.command()
async def 코디(ctx, *name):
    # 이름 인자가 없음
    if not len(name):
        await ctx.channel.send(
            embed=discord.Embed(title="!코디 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 코디 정보를 보여줍니다.",
                                color=side_bar_color),
            reference=ctx.message)
        return
    name = name[0]
    bs = BeautifulSoup(requests.get(f'https://maple.gg/u/{name}').text, "html.parser")

    # 기록을 확인할 수 없음
    if not len(bs.select("#user-profile > section > div.row.row-normal > div.col-lg-8 > h3 > img")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="캐릭터 이름을 확인해주세요."),
                               reference=ctx.message)
        return

    # 캐릭터의 외형 주소
    user_ch_tmp = str(bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-4.pt-1.pt-sm-0.pb-1.pb-sm-0.text-center.mt-2.mt-lg-0 > div > div.col-6.col-md-8.col-lg-6 > img")[
                          0])
    user_ch = user_ch_tmp[user_ch_tmp.find("http"):user_ch_tmp.rfind("png") + 3]

    # 의상 이름 불러오기
    user_codi = []
    for i in bs.find_all("span", {"class": "character-coord__item-name"}):
        user_codi.append(i.text)

    # 코디 분석 표 임베드 생성, 출력
    re = discord.Embed(title=name, description="", color=side_bar_color)
    re.add_field(name=f'코디 분석',
                 value=f'성형 : {user_codi[0]}\n헤어 : {user_codi[1]}\n모자 : {user_codi[2]}\n상의 : {user_codi[3]}\n하의 : {user_codi[4]}\n신발 : {user_codi[5]}\n무기 : {user_codi[6]}',
                 inline=False)
    re.set_thumbnail(url=user_ch.replace("s", "", 1))

    await ctx.channel.send(embed=re, reference=ctx.message)





