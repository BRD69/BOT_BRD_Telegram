import bs4
import requests
from bs4 import BeautifulSoup

URL = "https://my-calend.ru/holidays"

st_accept = "text/html"
st_useragent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537")

headers = {
    "Accept": st_accept,
    "User-Agent": st_useragent
}


def get_holidays():
    list_holidays = []
    req = requests.get(URL, headers=headers)
    req.encoding = 'utf-8'
    src = req.text

    try:
        soup = BeautifulSoup(src, 'lxml')
    except bs4.FeatureNotFound:
        list_holidays.append("Ошибка получения данных. FeatureNotFound")
        return list_holidays

    ul_list = soup.find('ul', class_="holidays-items")
    if ul_list is None:
        list_holidays.append("Ошибка получения данных. soup.find")
        return list_holidays

    li_elements = ul_list.find_all('li')
    if len(li_elements) == 0:
        list_holidays.append("Ошибка получения данных. ul_list.find_all")
        return list_holidays

    for li in li_elements:
        text_content = f"Данные не получены"
        contents = li.contents
        if len(contents) > 1:
            text_content = contents[1].text
        list_holidays.append(text_content)

    return list_holidays


if __name__ == "__main__":
    print(get_holidays())
