import requests
from bs4 import BeautifulSoup


class UserChar:
    """

    """
    User_name = ""
    User_HTML = ""
    User_IMG_URL = ""
    User_server = ""
    User_Level = ""
    User_Class = ""

    def __init__(self, name=""):
        self.User_name = name
        if not name == "":
            self.set_name_and_get_information(name)

    def set_name_and_get_information(self, name=""):
        """
        캐릭터의 이름을 설정하고
        해당 캐릭터의 HTML 문서를 크롤링
        """
        self.User_name = name
        self.User_HTML = BeautifulSoup(requests.get(f'https://maple.gg/u/{self.User_name}').text, "html.parser")
        if self.is_valid():
            # 캐릭터의 외형
            self.User_IMG_URL = str(self.User_HTML.find("img", {"alt": self.User_name}))
            self.User_IMG_URL = self.User_IMG_URL[
                                self.User_IMG_URL.find("https"):self.User_IMG_URL.rfind(".png") + 4].replace("s", "", 1)

            # 캐릭터의 서버
            self.User_server = str(self.User_HTML.select("h3"))
            self.User_server = self.User_server[self.User_server.find("alt=") + 5:self.User_server.find('" class')]

            # 캐릭터의 레벨, 직업
            User_Information = self.User_HTML.find_all("li", {"class": "user-summary-item"})
            self.User_Level = User_Information[0].string
            self.User_Class = User_Information[1].string
            del User_Information

    def is_valid(self):
        """
        캐릭터가 존재하면 True
        존재하지 않으면 False값을 return
        """
        return True if (self.User_HTML.find("img", {"alt": "검색결과 없음"}) == None) else False

    def get_MuLung(self):
        """
        캐릭터의 최고 무릉도장 정보를 리턴
        """
        # 갱신된 기록이 없다면 None 리턴
        if not self.User_HTML.select(
                "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div.mb-3 > img"
        ) == []:
            return None

        User_MuLung_HTML = self.User_HTML.find("div", {"class": "py-0 py-sm-4"})
        User_MuLung_Floor = User_MuLung_HTML.find('h1').string.replace(" ", "")[:-2]
        User_MuLung_Time = User_MuLung_HTML.find('small').string

        # 갱신일, 갱신시점의 레벨
        User_MuLung_HTML = self.User_HTML.find("footer", {"class": "user-summary-box-footer"})
        User_MuLung_Level = str(User_MuLung_HTML.find("span"))
        User_MuLung_Level = User_MuLung_Level[User_MuLung_Level.find("Lv."):User_MuLung_Level.find("Lv.") + 6]
        User_MuLung_Date = User_MuLung_HTML.find_all("span")[-1].string

        # 월드랭킹, 전체랭킹
        User_MuLung_Server_Rank, User_MuLung_Rank = User_MuLung_HTML.find_all("span")[1:-1]

        return [User_MuLung_Floor, User_MuLung_Time, User_MuLung_Level, User_MuLung_Server_Rank.string,
                User_MuLung_Rank.string, User_MuLung_Date]

    def get_TheSeed(self):
        """
        캐릭터의 최고 시드 정보를 리턴
        """

        # 갱신된 기록이 없다면 None 리턴
        if not self.User_HTML.select(
                "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > div > div.mb-3 > img"
        ) == []:
            return None

        User_TheSeed_HTML = self.User_HTML.find_all("div", {"class": "py-0 py-sm-4"})[-1]
        User_TheSeed_Floor = User_TheSeed_HTML.find('h1').string.replace(" ", "")[:-2]
        User_TheSeed_Time = User_TheSeed_HTML.find('small').string

        # 갱신일, 갱신시점의 레벨
        User_TheSeed_HTML = self.User_HTML.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > footer")
        User_TheSeed_Level = str(User_TheSeed_HTML[0].find("span"))
        User_TheSeed_Level = User_TheSeed_Level[User_TheSeed_Level.find("Lv."):User_TheSeed_Level.find("Lv.") + 6]
        User_TheSeed_Date = User_TheSeed_HTML[0].find_all("span")[-1].string

        # 월드랭킹, 전체랭킹
        User_TheSeed_Server_Rank, User_TheSeed_Rank = User_TheSeed_HTML[0].find_all("span")[1:-1]
        User_TheSeed_Server_Rank = str(User_TheSeed_Server_Rank)
        User_TheSeed_Server_Rank = User_TheSeed_Server_Rank[
                                   User_TheSeed_Server_Rank.find(">") + 1:User_TheSeed_Server_Rank.find("\n")]

        return [User_TheSeed_Floor, User_TheSeed_Time, User_TheSeed_Level,
                User_TheSeed_Server_Rank + '위' if User_TheSeed_Server_Rank[-1] != '위' else User_TheSeed_Server_Rank,
                User_TheSeed_Rank.string, User_TheSeed_Date]

    def get_Union(self):
        """
        캐릭터의 마지막 유니온 정보를 리턴
        """
        if not self.User_HTML.select(
                "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(3) > section > div > div.mb-3 > img"
        ) == []:
            return None

        User_Union_Information = self.User_HTML.find_all("div", {"class": "pt-3 pb-2 pb-sm-3"})[0]
        User_Union_grade = User_Union_Information.find("div").string
        User_Union_Level = User_Union_Information.find("span").string

        User_Union_IMG_URL = str(User_Union_Information.find("img"))
        User_Union_IMG_URL = User_Union_IMG_URL[User_Union_IMG_URL.find("https:"):User_Union_IMG_URL.rfind(".png") + 4]

        return [User_Union_grade, User_Union_Level, User_Union_IMG_URL]

    def get_achievement(self):
        """
        캐릭터의 마지막 업적 정보를 리턴
        """
        if not self.User_HTML.select(
                "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > div > div.mb-3 > img"
        ) == []:
            return None

        User_achievement_Information = self.User_HTML.find_all("div", {"class": "pt-3 pb-2 pb-sm-3"})[1]
        User_achievement_grade = User_achievement_Information.find("div").string
        User_achievement_score = User_achievement_Information.find("span").string

        User_achievement_IMG_URL = str(User_achievement_Information.find("img"))
        User_achievement_IMG_URL = User_achievement_IMG_URL[
                                   User_achievement_IMG_URL.find("https:"):User_achievement_IMG_URL.rfind(".png") + 4]

        return [User_achievement_grade, User_achievement_score, User_achievement_IMG_URL]

    def get_CharInformation(self):
        """
        캐릭터의 종합 정보를 리턴
        :return:
        """
        pass
