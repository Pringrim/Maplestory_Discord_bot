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
    result_Embed.add_field(name="!무릉, !시드, !유니온, !업적", value="Maple.gg 기준 정보를 불러옵니다.", inline=False)
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
        return_Embed = discord.Embed(title="!시드 <닉네임>\n!더시드 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 더 시드 최고기록을 보여줍니다.",
                                     color=side_bar_color)
        return_Embed.set_footer(text="더 시드 최고기록",
                                icon_url=variable.ICO_TheSeed)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
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

    return_Embed = discord.Embed(title=name, description="", color=side_bar_color)
    return_Embed.add_field(name=f'해저 {User_TheSeed[0]} 층',
                           value=f'{User_TheSeed[1]}\n{User_TheSeed[2]} / {User_Information.User_Class}\n\n'
                                 f'서버 {User_TheSeed[3]}\n전체 {User_TheSeed[4]}\n\n{User_TheSeed[5]}',
                           inline=False)
    return_Embed.set_thumbnail(url=User_Information.User_IMG_URL)
    return_Embed.set_footer(text="더 시드 최고기록",
                            icon_url=variable.ICO_TheSeed)

    await ctx.channel.send(embed=return_Embed, reference=ctx.message)


@bot.command(aliases=["유니온", "유뇬"])
async def union(ctx, *name):
    if not len(name):
        return_Embed = discord.Embed(title="!유니온 <닉네임>\n!유뇬 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 유니온 기록을 보여줍니다.",
                                     color=side_bar_color)
        return_Embed.set_footer(text="유니온",
                                icon_url=variable.IMG_UNION)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return
    name = name[0]

    User_Information = WebScraping.UserChar(name)
    # 캐릭터가 존재하지 않을 때
    if not User_Information.is_valid():
        return_Embed = discord.Embed(title="검색되지 않았어요!", description="잘못된 이름을 입력한 것 같아요.", color=side_bar_color)
        return_Embed.set_footer(text="유니온",
                                icon_url=variable.IMG_UNION)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    User_Union = User_Information.get_Union()
    # 유니온 기록이 없을 때
    if User_Union == None:
        return_Embed = discord.Embed(title="검색되지 않았어요!", description="기록이 존재하지 않아요.", color=side_bar_color)
        return_Embed.set_footer(text="유니온",
                                icon_url=variable.IMG_UNION)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    return_Embed = discord.Embed(title=name, description="", color=side_bar_color)
    return_Embed.add_field(name=f'{User_Union[0]}',
                           value=f'{User_Union[1]}\n전투력 : {User_Union[2]}',
                           inline=False)
    return_Embed.set_thumbnail(url=User_Information.User_IMG_URL)
    return_Embed.set_footer(text=f'{User_Union[-1]}',
                            icon_url=User_Union[3].replace("s", "", 1))

    await ctx.channel.send(embed=return_Embed, reference=ctx.message)


@bot.command(aliases=["업적"])
async def show_achievement(ctx, *name):
    print(name)
    if not len(name):
        return_Embed = discord.Embed(title="!업적 <닉네임>", description="Maple.gg 기준 해당 캐릭터의 업적 기록을 보여줍니다.",
                                     color=side_bar_color)
        return_Embed.set_footer(text="업적",
                                icon_url=variable.IMG_achievement)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return
    name = name[0]

    User_Information = WebScraping.UserChar(name)
    # 캐릭터가 존재하지 않을 때
    if not User_Information.is_valid():
        return_Embed = discord.Embed(title="검색되지 않았어요!", description="잘못된 이름을 입력한 것 같아요.", color=side_bar_color)
        return_Embed.set_footer(text="업적",
                                icon_url=variable.IMG_achievement)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    User_achievement = User_Information.get_achievement()
    # 업적 기록이 없을 때
    if User_achievement == None:
        return_Embed = discord.Embed(title="검색되지 않았어요!", description="기록이 존재하지 않아요.", color=side_bar_color)
        return_Embed.set_footer(text="업적",
                                icon_url=variable.IMG_achievement)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    return_Embed = discord.Embed(title=name, description="", color=side_bar_color)
    return_Embed.add_field(name=f'{User_achievement[0]}',
                           value=f'{User_achievement[1]}점\n{User_Information.User_Level} / {User_Information.User_Class}\n\n'
                                 f'{User_achievement[-1]}',
                           inline=False)
    return_Embed.set_thumbnail(url=User_Information.User_IMG_URL)
    return_Embed.set_footer(text="유니온 등급",
                            icon_url=User_achievement[2])

    await ctx.channel.send(embed=return_Embed, reference=ctx.message)


@bot.command(aliases=["추옵", "추가옵션"])
async def option(ctx, *name):
    if not len(name):
        return_Embed = discord.Embed(title="추가옵션 도움말", color=side_bar_color)
        return_Embed.add_field(name="!추옵 <방어구 레벨>\n!추가옵션 <방어구 레벨>", value="해당 방어구의 추가옵션 수치를 보여줍니다.", inline=False)
        return_Embed.add_field(name="!추옵 <무기 이름>\n!추가옵션 <무기 이름>", value="해당 무기의 공/마 추가옵션 수치를 보여줍니다.", inline=False)
        return_Embed.add_field(name="예시", value=f"!추옵 파프아대 또는 !추옵 파프니르 리스크홀더\n"
                                                f"!추옵 라피스3형 또는 !추옵 라즐리3형", inline=False)
        return_Embed.set_footer(text="추가옵션",
                            icon_url=variable.ICO_fire_of_rebirth)
        await ctx.channel.send(embed=return_Embed, reference=ctx.message)
        return

    # 레벨로 검색할 경우(방어구)
    if name[0].isnumeric():
        if int(name[0]) < 100 or int(name[0]) > 200 or (int(name[0]) > 160 and int(name[0]) < 200):
            await ctx.channel.send(
                embed=discord.Embed(title="추옵을 찾을 수 없어요!", description="잘못된 값을 입력하지는 않았나요?",
                                    color=side_bar_color),
                reference=ctx.message)
            return

        result_Level = (int(name[0]) - 100) // 10

        re = discord.Embed(title=f'{name[0]}레벨의 방어구 추옵표', description="", color=side_bar_color)
        re.add_field(name=f'단일 스텟',
                     value=f'1단계 {variable.one_stat[result_Level][0]}\n'
                           f'2단계 {variable.one_stat[result_Level][1]}\n'
                           f'3단계 {variable.one_stat[result_Level][2]}\n'
                           f'4단계 {variable.one_stat[result_Level][3]}\n'
                           f'5단계 {variable.one_stat[result_Level][4]}\n',
                     inline=True)
        re.add_field(name=f'이중 스텟',
                     value=f'1단계 {variable.two_stats[result_Level][0]}\n'
                           f'2단계 {variable.two_stats[result_Level][1]}\n'
                           f'3단계 {variable.two_stats[result_Level][2]}\n'
                           f'4단계 {variable.two_stats[result_Level][3]}\n'
                           f'5단계 {variable.two_stats[result_Level][4]}\n',
                     inline=True)
        re.add_field(name=f'공/마/기타',
                     value=f'1단계 {variable.others_value[0]}\n'
                           f'2단계 {variable.others_value[1]}\n'
                           f'3단계 {variable.others_value[2]}\n'
                           f'4단계 {variable.others_value[3]}\n'
                           f'5단계 {variable.others_value[4]}\n',
                     inline=True)
        re.add_field(name=f'착감',
                     value=f'1단계 {variable.level_limit_down_value[0]}\n'
                           f'2단계 {variable.level_limit_down_value[1]}\n'
                           f'3단계 {variable.level_limit_down_value[2]}\n'
                           f'4단계 {variable.level_limit_down_value[3]}\n'
                           f'5단계 {variable.level_limit_down_value[4]}\n',
                     inline=True)
        re.add_field(name=f'HP / MP',
                     value=f'1단계 {format(variable.hpmp[result_Level][0], ",")}\n'
                           f'2단계 {format(variable.hpmp[result_Level][1], ",")}\n'
                           f'3단계 {format(variable.hpmp[result_Level][2], ",")}\n'
                           f'4단계 {format(variable.hpmp[result_Level][3], ",")}\n'
                           f'5단계 {format(variable.hpmp[result_Level][4], ",")}\n',
                     inline=True)
        re.set_thumbnail(url=variable.ICO_fire_of_rebirth)
        await ctx.channel.send(embed=re, reference=ctx.message)
        return

    # 아이템 이름으로 검색할 경우(무기)
    else:
        weapon_name = ""
        for i in name:
            weapon_name += i

        if variable.weapon_option.get(weapon_name, 0):
            re = discord.Embed(title=f'{variable.weapon_option[weapon_name][0]}의 추옵표', description="",
                               color=side_bar_color)
            re.add_field(name=f'공 / 마',
                         value=f'1단계 {variable.weapon_option[weapon_name][1]}\n'
                               f'2단계 {variable.weapon_option[weapon_name][2]}\n'
                               f'3단계 {variable.weapon_option[weapon_name][3]}\n'
                               f'4단계 {variable.weapon_option[weapon_name][4]}\n'
                               f'5단계 {variable.weapon_option[weapon_name][5]}\n',
                         inline=True)
            re.set_thumbnail(url=variable.ICO_fire_of_rebirth)
            await ctx.channel.send(embed=re, reference=ctx.message)
            return
        else:
            for i in variable.weapon_option.values():
                if weapon_name == i[0].replace(" ", ""):
                    re = discord.Embed(title=f'{i[0]}의 추옵표', description="", color=side_bar_color)
                    re.add_field(name=f'공 / 마',
                                 value=f'1단계 {i[1]}\n'
                                       f'2단계 {i[2]}\n'
                                       f'3단계 {i[3]}\n'
                                       f'4단계 {i[4]}\n'
                                       f'5단계 {i[5]}\n',
                                 inline=True)
                    re.set_thumbnail(url=variable.ICO_fire_of_rebirth)
                    await ctx.channel.send(embed=re, reference=ctx.message)
                    return

            await ctx.channel.send(
                embed=discord.Embed(title="추옵을 찾을 수 없어요!", description="잘못된 이름을 입력하지는 않았나요?",
                                    color=side_bar_color),
                reference=ctx.message)
            return
