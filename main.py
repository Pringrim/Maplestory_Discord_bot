import bot as botpy
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

token = botpy.bot_token
side_bar_color = 0xFFBB00
botpy.bot.run(token)


@botpy.bot.command(aliases=["무릉", "무릉도장"])
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


@botpy.bot.command()
async def 시드(ctx, *name):
    if not len(name):
        await ctx.channel.send(embed=discord.Embed(title="!시드 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 시드 최고기록을 보여줍니다.",
                                                   color=side_bar_color), reference=ctx.message)
        return

    name = name[0]
    bs = BeautifulSoup(requests.get(f'https://maple.gg/u/{name}').text, "html.parser")

    if len(bs.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > div > div.text-secondary")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="기록이 없거나 갱신되지 않았을 수 있습니다."),
                               reference=ctx.message)
        return

    if not len(bs.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > div > div > div > h1")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="캐릭터 이름을 확인해주세요."),
                               reference=ctx.message)
        return

    user_floor_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > div > div > div > h1")[
                             0])
    user_floor = user_floor_tmp[user_floor_tmp.rfind("bold") + 6:user_floor_tmp.rfind("\n")]

    user_time_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > div > div > div > small")[
                            0])
    user_time = user_time_tmp[user_time_tmp.find(">") + 1:user_time_tmp.rfind("초") + 1]

    user_level_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > footer > div.d-block.mb-1 > span")[
                             0])
    user_level = str(user_level_tmp)[6:str(user_level_tmp).find("\n")]  # 시드 레벨 구하기

    user_job = str(user_level_tmp)[str(user_level_tmp).rfind(" "):-7]

    user_rank_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > footer > div.mb-2")[
                            0])
    user_rank_tmp = user_rank_tmp[user_rank_tmp.find("<span>"):]

    user_server_rank = str(user_rank_tmp)[str(user_rank_tmp).find("<span>") + 6:str(user_rank_tmp).find("\n")] + "위"
    user_rank = str(user_rank_tmp)[str(user_rank_tmp).rfind("<span>") + 6:str(user_rank_tmp).rfind("위") + 1]

    user_date_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > footer > div.user-summary-date > span")[
                            0])
    user_date = user_date_tmp[user_date_tmp.find(": ") + 2:user_date_tmp.rfind("일") + 1]

    user_pic_tmp = str(bs.select(
        "#user-profile > section > div.row.row-normal > div.col-lg-4.pt-1.pt-sm-0.pb-1.pb-sm-0.text-center.mt-2.mt-lg-0 > div > div.col-6.col-md-8.col-lg-6 > img")[
                           0])
    user_pic_url = user_pic_tmp[user_pic_tmp.find("https:"):user_pic_tmp.rfind(".png") + 4].replace("s", "", 1)

    re = discord.Embed(title=name, description="", color=side_bar_color)
    re.add_field(name=f'해저 {user_floor} 층',
                 value=f'{user_time}\n{user_level} / {user_job}\n\n서버 {user_server_rank}\n전체 {user_rank}\n\n{"20" + user_date if user_date != "오늘" else user_date}',
                 inline=False)
    re.set_thumbnail(url=user_pic_url)
    re.set_footer(text="더 시드 최고기록",
                  icon_url="https://w.namu.la/s/702d1dc6d96676696feaba3ab397fa8ed6850cc2f3eb6e31a7c467470cb63a39b4630e29c1966db1cf306baa5ab83914bf1fb8e01dfe8b5f2d90159bd63220bdcc7458d12d84ae6dcf0bbf586c7626c11b94b4d0195cb5d2972498ff28d19deb")

    await ctx.channel.send(embed=re, reference=ctx.message)


@botpy.bot.command(aliases=["유니온", "유뇬"])
async def union(ctx, *name):
    if not len(name):
        await ctx.channel.send(
            embed=discord.Embed(title="!유니온 <닉네임>\n!유뇬 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 유니온 레벨을 보여줍니다.",
                                color=side_bar_color), reference=ctx.message)
        return
    name = name[0]

    bs = BeautifulSoup(requests.get(f'https://maple.gg/u/{name}').text, "html.parser")
    if len(bs.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > div > div.text-secondary")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="기록이 없거나 갱신되지 않았을 수 있습니다."),
                               reference=ctx.message)
        return

    if not len(bs.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > div > div > div")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="캐릭터 이름을 확인해주세요."),
                               reference=ctx.message)
        return

    user_union_icon = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > div > div > img")[
                              0])

    union_icon_url = user_union_icon[user_union_icon.find("https:"):user_union_icon.rfind(".png") + 4]

    user_urank_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > div > div > div")[
                             0])
    user_urank = user_urank_tmp[user_urank_tmp.find(">") + 1:-6]

    user_ulevel_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > div > div > span")[
                              0])
    user_ulevel = user_ulevel_tmp[user_ulevel_tmp.find("Lv."):user_ulevel_tmp.rfind("</")]

    user_upower_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > footer > div.d-block.mb-1 > span")[
                              0])
    user_upower = user_upower_tmp[user_upower_tmp.find(" ") + 1:user_upower_tmp.rfind("</span>")]

    user_rank_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > footer > div.mb-2")[
                            0])
    user_rank_tmp = user_rank_tmp[user_rank_tmp.find("<span>") + 6:]
    user_server_rank = user_rank_tmp[:user_rank_tmp.find("\n")]
    user_rank = user_rank_tmp[user_rank_tmp.rfind("<span>") + 6:user_rank_tmp.rfind("</span>") - 1]

    user_date_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > footer > div.user-summary-date > span")[
                            0])
    user_date = user_date_tmp[user_date_tmp.find(":") + 2:-7]

    re = discord.Embed(title=name, description="", color=side_bar_color)
    re.add_field(name=f'{user_urank}',
                 value=f'{user_ulevel} / 전투력 : {user_upower}\n\n서버 {user_server_rank}위\n전체 {user_rank}위\n\n기준일 : {"20" + user_date if user_date != "오늘" else user_date}',
                 inline=False)
    re.set_thumbnail(url=union_icon_url)
    re.set_footer(text="유니온 등급",
                  icon_url=union_icon_url)

    await ctx.channel.send(embed=re, reference=ctx.message)


@botpy.bot.command()
async def 업적(ctx, *name):
    if not len(name):
        await ctx.channel.send(embed=discord.Embed(title="!업적 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 업적 점수를 보여줍니다.",
                                                   color=side_bar_color), reference=ctx.message)
        return
    name = name[0]
    bs = BeautifulSoup(requests.get(f'https://maple.gg/u/{name}').text, "html.parser")

    if len(bs.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > div > div.text-secondary")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="기록이 없거나 갱신되지 않았을 수 있습니다."),
                               reference=ctx.message)
        return
    if not len(bs.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > div > div > div")):
        await ctx.channel.send(embed=discord.Embed(title="기록을 찾을 수 없습니다!", description="캐릭터 이름을 확인해주세요."),
                               reference=ctx.message)
        return

    user_ach_icon_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > div > div > img")[
                                0])
    user_ach_icon_url = user_ach_icon_tmp[user_ach_icon_tmp.find("https:"):user_ach_icon_tmp.rfind(".png") + 4]

    user_ach_class_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > div > div > div")[
                                 0])
    user_ach_class = user_ach_class_tmp[user_ach_class_tmp.find("bold") + 6:-6]

    user_ach_score_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > div > div > span")[
                                 0])
    user_ach_score = user_ach_score_tmp[user_ach_score_tmp.find("업적점수") + 5:-7]

    user_level_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > footer > div.d-block.mb-1 > span")[
                             0])
    user_level = user_level_tmp[user_level_tmp.find("Lv."):user_level_tmp.find('\n')]
    user_job = user_level_tmp[user_level_tmp.rfind(" ") + 1:-7]

    user_date_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > footer > div.user-summary-date > span")[
                            0])
    user_date = user_date_tmp[user_date_tmp.find(": ") + 2:-7]

    user_rank_tmp = str(bs.select(
        "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > footer > div.mb-2")[
                            0])
    user_rank_tmp = user_rank_tmp[user_rank_tmp.find("<span>") + 6:]
    user_server_rank = user_rank_tmp[:user_rank_tmp.find("\n")]
    user_rank = user_rank_tmp[user_rank_tmp.rfind("<span>") + 6:user_rank_tmp.rfind("</span>") - 1]

    re = discord.Embed(title=name, description="", color=side_bar_color)
    re.add_field(name=f'{user_ach_class}',
                 value=f'업적점수 : {user_ach_score}점\n{user_level} / {user_job}\n\n서버 {user_server_rank}위\n전체 {user_rank}위\n\n마지막 갱신일 : {user_date}',
                 inline=False)
    re.set_thumbnail(url=user_ach_icon_url)
    re.set_footer(text="유니온 등급",
                  icon_url=user_ach_icon_url)

    await ctx.channel.send(embed=re, reference=ctx.message)


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


@botpy.bot.command(aliases=["추옵", "추가옵션"])
async def option(ctx, *name):
    if not len(name):
        re = discord.Embed(title="추가옵션 도움말", color=side_bar_color)
        re.add_field(name="!추옵 <무기 이름>\n!추가옵션 <무기 이름>", value="해당 무기의 공/마 추가옵션 수치를 보여줍니다.", inline=False)
        re.add_field(name="!추옵 <방어구 레벨>\n!추가옵션 <방어구 레벨>", value="해당 방어구의 추가옵션 수치를 보여줍니다.", inline=False)
        re.set_footer(text="더 자세한 도움말이 보고싶다면?\n!추가옵션도움말")
        await ctx.channel.send(embed=re, reference=ctx.message)
        return
    return_fire_url = "http://w.namu.la/s/bf114f6b7c91ecbf5b4f90b9485f8b4fd4ae40ca30d76b3a3e6d22b902907089f0c1f7ac37f9999f2f3457946198a3a17a2a188e924f8a31ec135406e6294e5ac328b23df86a147826a3a47e50bad460846d85762f1c909aec0d826a420f78af"

    if name[0].isnumeric():
        el_value = [3, 4, 5, 6, 7]
        level_down_value = [-15, -20, -25, -30, -35]
        one_stat_dic = {
            0: [18, 24, 30, 36, 42],
            1: [18, 24, 30, 36, 42],
            2: [21, 28, 35, 42, 49],
            3: [21, 28, 35, 42, 49],
            4: [24, 32, 40, 48, 56],
            5: [24, 32, 40, 48, 56],
            6: [27, 36, 45, 54, 63],
            10: [33, 44, 55, 66, 77]
        }
        two_stats_dic = {
            0: [9, 12, 15, 18, 21],
            1: [9, 12, 15, 18, 21],
            2: [12, 16, 20, 24, 28],
            3: [12, 16, 20, 24, 28],
            4: [12, 16, 20, 24, 28],
            5: [12, 16, 20, 24, 28],
            6: [15, 20, 25, 30, 35],
            10: [18, 24, 30, 36, 42]
        }
        hpmp_dic = {
            0: [900, 1200, 1500, 1800, 2100],
            1: [990, 1320, 1650, 1980, 2310],
            2: [1080, 1440, 1800, 2160, 2520],
            3: [1170, 1560, 1950, 2340, 2730],
            4: [1260, 1680, 2100, 2520, 2940],
            5: [1350, 1800, 2250, 2700, 3150],
            6: [1440, 1920, 2400, 2880, 3360],
            10: [1800, 2400, 3000, 3600, 4200]
        }

        if int(name[0]) < 100 or int(name[0]) > 200 or (int(name[0]) > 160 and int(name[0]) < 200):
            await ctx.channel.send(
                embed=discord.Embed(title="추옵을 찾을 수 없어요!", description="잘못된 값을 입력하지는 않았나요?",
                                    color=side_bar_color),
                reference=ctx.message)
            return

        result = (int(name[0]) - 100) // 10

        re = discord.Embed(title=f'{name[0]}레벨의 방어구 추옵표', description="", color=side_bar_color)
        re.add_field(name=f'단일 스텟',
                     value=f'1단계 {one_stat_dic[result][0]}\n'
                           f'2단계 {one_stat_dic[result][1]}\n'
                           f'3단계 {one_stat_dic[result][2]}\n'
                           f'4단계 {one_stat_dic[result][3]}\n'
                           f'5단계 {one_stat_dic[result][4]}\n',
                     inline=True)
        re.add_field(name=f'이중 스텟',
                     value=f'1단계 {two_stats_dic[result][0]}\n'
                           f'2단계 {two_stats_dic[result][1]}\n'
                           f'3단계 {two_stats_dic[result][2]}\n'
                           f'4단계 {two_stats_dic[result][3]}\n'
                           f'5단계 {two_stats_dic[result][4]}\n',
                     inline=True)
        re.add_field(name=f'공/마/기타',
                     value=f'1단계 {el_value[0]}\n'
                           f'2단계 {el_value[1]}\n'
                           f'3단계 {el_value[2]}\n'
                           f'4단계 {el_value[3]}\n'
                           f'5단계 {el_value[4]}\n',
                     inline=True)
        re.add_field(name=f'착감',
                     value=f'1단계 {level_down_value[0]}\n'
                           f'2단계 {level_down_value[1]}\n'
                           f'3단계 {level_down_value[2]}\n'
                           f'4단계 {level_down_value[3]}\n'
                           f'5단계 {level_down_value[4]}\n',
                     inline=True)
        re.add_field(name=f'HP / MP',
                     value=f'1단계 {format(hpmp_dic[result][0], ",")}\n'
                           f'2단계 {format(hpmp_dic[result][1], ",")}\n'
                           f'3단계 {format(hpmp_dic[result][2], ",")}\n'
                           f'4단계 {format(hpmp_dic[result][3], ",")}\n'
                           f'5단계 {format(hpmp_dic[result][4], ",")}\n',
                     inline=True)
        re.set_thumbnail(url=return_fire_url)
        await ctx.channel.send(embed=re, reference=ctx.message)
        return
    else:
        weapon_name = ""
        for i in name:
            weapon_name += i
        return_fire_url = "https://raw.githubusercontent.com/Pringrim/Maplestory_discord_bot_test/main/%EC%A7%B9.jpg?token=GHSAT0AAAAAABXTXVBGYS7MVUX3PZVXVLESYXYIK3Q"
        weapon_option_dic = {
            # 파프니르
            "파프아대": ["파프니르 리스크홀더", 11, 16, 21, 28, 36],
            "파프건": ["파프니르 첼리스카", 15, 22, 31, 40, 52],
            "파프너클": ["파프니르 펜리르탈론", 16, 23, 31, 41, 53],
            "파프소울슈터": ["파프니르 엔젤릭슈터", 16, 23, 31, 41, 53],
            "파프에너지소드": ["파프니르 스플릿엣지", 16, 23, 31, 41, 53],
            "파프폴암": ["파프니르 문글레이브", 19, 27, 38, 49, 63],
            "파프활": ["파프니르 윈드체이서", 20, 29, 39, 52, 66],
            "파프듀얼보우건": ["파프니르 듀얼윈드윙", 20, 29, 39, 52, 66],
            "파프에인션트보우": ["파프니르 에인션트 보우", 20, 29, 39, 52, 66],
            "파프체인": ["파프니르 체인", 20, 29, 39, 52, 66],
            "파프단검": ["파프니르 다마스커스", 20, 29, 39, 52, 66],
            "파프부채": ["파프니르 용선", 20, 29, 39, 52, 66],
            "파프한손검": ["파프니르 미스틸테인", 20, 29, 40, 53, 68],
            "파프한손도끼": ["파프니르 트윈클리버", 20, 29, 40, 53, 68],
            "파프한손둔기": ["파프니르 골디언해머", 20, 29, 40, 53, 68],
            "파프석궁": ["파프니르 윈드윙슈터", 20, 29, 40, 53, 68],
            "파프케인": ["파프니르 클레르시엘", 20, 29, 40, 53, 68],
            "파프두손검": ["파프니르 페니텐시아", 21, 31, 42, 55, 71],
            "파프데스페라도": ["파프니르 데스브링어", 21, 31, 42, 55, 71],
            "파프튜너": ["파프니르 포기브리스", 21, 31, 42, 55, 71],
            "파프두손도끼": ["파프니르 배틀클리버", 21, 31, 42, 55, 71],
            "파프두손둔기": ["파프니르 라이트닝어", 21, 31, 42, 55, 71],
            "파프창": ["파프니르 브류나크", 21, 31, 42, 55, 71],
            "파프핸드캐논": ["파프니르 러스터캐논", 21, 31, 42, 55, 71],
            "파프완드": ["파프니르 마나테이커", 25, 36, 49, 65, 83],
            "파프샤이닝로드": ["파프니르 마나크래들,", 25, 36, 49, 65, 83],
            "파프ESP리미터": ["파프니르 ESP리미터", 25, 36, 49, 65, 83],
            "파프스태프": ["파프니르 마나크라운", 25, 36, 49, 65, 83],
            "파프건틀렛리볼버": ["파프니르 빅 마운틴", 16, 23, 31, 41, 53],
            "파프매직건틀렛": ["파프니르 매직 건틀렛", 25, 36, 49, 65, 83],
            "파프브레스슈터": ["파프니르 나이트체이서", 20, 29, 39, 52, 66],

            # 앱솔랩스
            "앱솔아대": ["앱솔랩스 리벤지가즈", 16, 23, 32, 42, 53],
            "앱솔건": ["앱솔랩스 포인팅건", 23, 33, 46, 60, 77],
            "앱솔너클": ["앱솔랩스 블로우너클", 24, 34, 47, 62, 79],
            "앱솔소울슈터": ["앱솔랩스 소울슈터", 24, 34, 47, 62, 79],
            "앱솔에너지소드": ["앱솔랩스 에너지소드", 24, 34, 47, 62, 79],
            "앱솔건틀렛리볼버": ["앱솔랩스 파일갓", 24, 34, 47, 62, 79],
            "앱솔폴암": ["앱솔랩스 햄버드", 28, 41, 56, 74, 95],
            "앱솔활": ["앱솔랩스 슈팅보우", 29, 43, 59, 77, 99],
            "앱솔듀얼보우건": ["앱솔랩스 듀얼보우건", 29, 43, 59, 77, 99],
            "앱솔에이션트보우": ["앱솔랩스 에이션트 보우", 29, 43, 59, 77, 99],
            "앱솔체인": ["앱솔랩스 체인", 29, 43, 59, 77, 99],
            "앱솔단검": ["앱솔랩스 슬래셔", 29, 43, 59, 77, 99],
            "앱솔한손검": ["앱솔랩스 세이버", 30, 44, 60, 79, 101],
            "앱솔한손도끼": ["앱솔랩스 엑스", 30, 44, 60, 79, 101],
            "앱솔한손둔기": ["앱솔랩스 비트해머", 30, 44, 60, 79, 101],
            "앱솔석궁": ["앱솔랩스 크로스보우", 30, 44, 60, 79, 101],
            "앱솔케인": ["앱솔랩스 핀쳐케인", 30, 44, 60, 79, 101],
            "앱솔두손검": ["앱솔랩스 브로드세이버", 31, 46, 63, 82, 106],
            "앱솔데스페라도": ["앱솔랩스 데스페라도", 31, 46, 63, 82, 106],
            "앱솔두손도끼": ["앱솔랩스 브로드엑스", 31, 46, 63, 82, 106],
            "앱솔두손둔기": ["앱솔랩스 브로드해머", 31, 46, 63, 82, 106],
            "앱솔창": ["앱솔랩스 피어싱스피어", 31, 46, 63, 82, 106],
            "앱솔핸드캐논": ["앱솔랩스 블래스트캐논", 32, 47, 64, 84, 108],
            "앱솔완드": ["앱솔랩스 스펠링완드", 37, 54, 73, 97, 124],
            "앱솔샤이닝로드": ["앱솔랩스 샤이닝로드", 37, 54, 73, 97, 124],
            "앱솔ESP리미터": ["앱솔랩스 ESP리미터", 37, 54, 73, 97, 124],
            "앱솔스태프": ["앱솔랩스 스펠링스태프", 37, 54, 75, 98, 126],

            # 아케인셰이드
            "아케인아대": ["아케인셰이드 가즈", 27, 40, 55, 72, 92],
            "아케인건": ["아케인셰이드 피스톨", 39, 58, 79, 104, 133],
            "아케인에너지소드": ["아케인셰이드 에너지체인", 40, 59, 81, 106, 103],
            "아케인너클": ["아케인셰이드 클로", 40, 59, 81, 106, 136],
            "아케인건틀렛리볼버": ["아케인셰이드 엘라하", 40, 59, 81, 106, 136],
            "아케인소울슈터": ["아케인셰이드 소울슈터", 40, 59, 81, 106, 136],
            "아케인폴암": ["아케인셰이드 폴암", 50, 73, 101, 133, 170],
            "아케인부채": ["아케인셰이드 초선", 50, 73, 101, 133, 170],
            "아케인브레스슈터": ["아케인셰이드 브레스 슈터", 50, 73, 101, 133, 170],
            "아케인듀얼보우건": ["아케인셰이드 듀얼보우건", 50, 73, 101, 133, 170],
            "아케인체인": ["아케인셰이드 체인", 50, 73, 101, 133, 170],
            "아케인한손검": ["아케인셰이드 세이버", 51, 75, 103, 136, 175],
            "아케인한손도끼": ["아케인셰이드 엑스", 51, 75, 103, 136, 175],
            "아케인한손둔기": ["아케인셰이드 해머", 51, 75, 103, 136, 175],
            "아케인케인": ["아케인셰이드 케인", 51, 75, 103, 136, 175],
            "아케인석궁": ["아케인셰이드 크로스보우", 51, 75, 103, 136, 175],
            "아케인튜너": ["아케인셰이드 튜너", 54, 78, 108, 142, 182],
            "아케인창": ["아케인셰이드 스피어", 54, 78, 108, 142, 182],
            "아케인두손검": ["아케인셰이드 투핸드소드", 54, 78, 108, 142, 182],
            "아케인두손도끼": ["아케인셰이드 투핸드엑스", 54, 78, 108, 142, 182],
            "아케인두손둔기": ["아케인셰이드 투핸드해머", 54, 78, 108, 142, 182],
            "아케인데스페라도": ["아케인셰이드 데스페라도", 54, 78, 108, 142, 182],
            "아케인핸드캐논": ["아케인셰이드 시즈건", 55, 80, 110, 145, 186],
            "아케인완드": ["아케인셰이드 완드", 63, 92, 126, 167, 214],
            "아케인샤이닝로드": ["아케인셰이드 샤이닝로드", 63, 92, 126, 167, 214],
            "아케인ESP리미터": ["아케인셰이드 ESP리미터", 63, 92, 126, 167, 214],
            "아케인매직건틀렛": ["아케인셰이드 매직 건틀렛", 63, 92, 126, 167, 214],
            "아케인스태프": ["아케인셰이드 스태프", 64, 94, 129, 170, 218],

            # 제로
            "라피스1형": ["라피스 / 라즐리 1형", 4, 7, 12, 17, 23],
            "라즐리1형": ["라피스 / 라즐리 1형", 4, 7, 12, 17, 23],
            "라피스2형": ["라피스 / 라즐리 2형", 4, 7, 12, 17, 24],
            "라즐리2형": ["라피스 / 라즐리 2형", 4, 7, 12, 17, 24],
            "라피스3형": ["라피스 / 라즐리 3형", 5, 10, 16, 23, 32],
            "라즐리3형": ["라피스 / 라즐리 3형", 5, 10, 16, 23, 32],
            "라피스4형": ["라피스 / 라즐리 4형", 5, 11, 17, 25, 34],
            "라즐리4형": ["라피스 / 라즐리 4형", 5, 11, 17, 25, 34],
            "라피스5형": ["라피스 / 라즐리 5형", 5, 11, 18, 26, 36],
            "라즐리5형": ["라피스 / 라즐리 5형", 5, 11, 18, 26, 36],
            "라피스6형": ["라피스 / 라즐리 6형", 6, 13, 21, 30, 41],
            "라즐리6형": ["라피스 / 라즐리 6형", 6, 13, 21, 30, 41],
            "라피스7형": ["라피스 / 라즐리 7형", 9, 20, 32, 47, 64],
            "라즐리7형": ["라피스 / 라즐리 7형", 9, 20, 32, 47, 64],
            "라피스8형": ["라피스 / 라즐리 8형", 11, 23, 38, 56, 76],
            "라즐리8형": ["라피스 / 라즐리 8형", 11, 23, 38, 56, 76],
            "라피스9형": ["라피스 / 라즐리 9형", 18, 40, 65, 95, 131],
            "라즐리9형": ["라피스 / 라즐리 9형", 18, 40, 65, 95, 131],
            "라피스10형": ["라피스 / 라즐리 10형", 21, 46, 75, 110, 151],
            "라즐리10형": ["라피스 / 라즐리 10형", 21, 46, 75, 110, 151]
        }
        if weapon_option_dic.get(weapon_name, 0):
            re = discord.Embed(title=f'{weapon_option_dic[weapon_name][0]}의 추옵표', description="", color=side_bar_color)
            re.add_field(name=f'공 / 마',
                         value=f'1단계 {weapon_option_dic[weapon_name][1]}\n'
                               f'2단계 {weapon_option_dic[weapon_name][2]}\n'
                               f'3단계 {weapon_option_dic[weapon_name][3]}\n'
                               f'4단계 {weapon_option_dic[weapon_name][4]}\n'
                               f'5단계 {weapon_option_dic[weapon_name][5]}\n',
                         inline=True)
            re.set_thumbnail(url=return_fire_url)
            await ctx.channel.send(embed=re, reference=ctx.message)
            return
        else:
            for i in weapon_option_dic.values():
                if weapon_name==i[0].replace(" ",""):
                    re = discord.Embed(title=f'{i[0]}의 추옵표', description="", color=side_bar_color)
                    re.add_field(name=f'공 / 마',
                                 value=f'1단계 {i[1]}\n'
                                       f'2단계 {i[2]}\n'
                                       f'3단계 {i[3]}\n'
                                       f'4단계 {i[4]}\n'
                                       f'5단계 {i[5]}\n',
                                 inline=True)
                    re.set_thumbnail(url=return_fire_url)
                    await ctx.channel.send(embed=re, reference=ctx.message)
                    return

            await ctx.channel.send(
                embed=discord.Embed(title="추옵을 찾을 수 없어요!", description="잘못된 이름을 입력하지는 않았나요?",
                                    color=side_bar_color),
                reference=ctx.message)
            return



