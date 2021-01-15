import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "http://www.konkuk.ac.kr/do/MessageBoard/"

NOTICES = [
    {
        "category": "학사",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=notice",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "1"
    },
    {
        "category": "장학",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=11688412",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "2"
    },
    {
        "category": "취업/진로",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=11731332&cat=0011400001",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "3"
    },
    {
        "category": "현장실습",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=11731332&cat=0011400003",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "4"
    },
    {
        "category": "창업",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=11731332&cat=0011400004",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "5"
    },
    {
        "category": "국제",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=notice&cat=0000300002",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "6"
    },
    {
        "category": "학생",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=notice&cat=0000300003",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "7"
    },
    {
        "category": "산학/연구",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=notice&cat=0000300001",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "8"
    },
    {
        "category": "일반",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=notice&cat=0000300006",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "9"
    },
    {
        "category": "코로나19 알림",
        "url": "http://www.konkuk.ac.kr/do/MessageBoard/ArticleList.do?forum=11782906",
        "latest_notice": "",
        "latest_post": "",
        "category_num": "10"
    },
]


def get_soup(URL):
    req = requests.get(URL)
    html = req.text
    return BeautifulSoup(html, 'html.parser')


def get_end_page_num(URL):
    soup = get_soup(URL)
    end_page = soup.select_one(
        '#content > form:nth-child(1) > div.paginate > a.next')

    # ['href'].split('rel=')[1]

    if end_page == None:
        return 0
    else:
        return end_page['href'].split('rel=')[1]


def get_trs(URL, end_page):
    trs_list = []
    for page_num in range(0, int(end_page)+1):
        soup = get_soup(URL + "&p=" + str(page_num))

        table = soup.find("table", {"class": "list"})
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")

        for tr in trs:
            trs_list.append(tr)
    return trs_list


def check_updated(latest: str, href, NOTICE):
    if href != NOTICE[latest]:
        print("UPDATED", latest, "in", NOTICE["category"])
        # POST to Django
        post_updated(href, NOTICE)

        # update latest post
        NOTICE[latest] = href

        return True
    else:
        return False


def post_updated(href: str, NOTICE):
    data = {
        "href": href,
        "notice_num": NOTICE["category_num"],
        "category_title": NOTICE["category"]
    }
    res = requests.post("127.0.0.1:8000/updated/", data=data)


def init_notice(latest: str, href, NOTICE):
    try:
        print("INITIALIZE", latest, "in", NOTICE["category"], "to", href)
        NOTICE[latest] = href
    except:
        print("INITIALIZE FAILED")


def init_notices():
    for NOTICE in NOTICES:
        URL = NOTICE["url"]

        end_page = get_end_page_num(URL)
        trs = get_trs(URL, end_page)

        isNoticeDone = False
        isPostDone = False
        td_index = 2

        if NOTICE["category"] == "장학" or NOTICE["category"] == "코로나19 알림":
            td_index = 1

        for tr in trs:
            td = tr.find_all("td")
            href = BASE_URL + td[td_index].find("a")["href"]
            title = td[td_index].find("a").get_text().strip()
            hasClass = tr.has_attr("class")

            if hasClass:
                if isNoticeDone == False:
                    init_notice("latest_notice", href, NOTICE)
                    isNoticeDone = True
                else:
                    continue
            else:
                if isPostDone == False:
                    init_notice("latest_post", href, NOTICE)
                    isPostDone = True
                else:
                    continue


def check_notices():
    for NOTICE in NOTICES:
        URL = NOTICE["url"]

        end_page = get_end_page_num(URL)
        trs = get_trs(URL, end_page)

        isNoticeDone = False
        isPostDone = False
        td_index = 2

        if NOTICE["category"] == "장학" or NOTICE["category"] == "코로나19 알림":
            td_index = 1

        for tr in trs:
            td = tr.find_all("td")
            href = BASE_URL + td[td_index].find("a")["href"]
            title = td[td_index].find("a").get_text().strip()
            hasClass = tr.has_attr("class")

            if hasClass:
                if isNoticeDone == False:
                    check_updated("latest_notice", href, NOTICE)
                    isNoticeDone = True
                else:
                    continue
            else:
                if isPostDone == False:
                    check_updated("latest_post", href, NOTICE)
                    isPostDone = True
                else:
                    continue


if __name__ == "__main__":
    init_notices()

    while True:
        check_notices()
        time.sleep(3)
