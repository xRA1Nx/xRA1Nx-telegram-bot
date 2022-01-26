import requests
from bs4 import BeautifulSoup

d_currency = {'евро': 'EUR',
              'рубль': 'RUB',
              'доллар': 'USD',
              'турецкая лира': 'TYR',
              'юань': "CNY",
              'гривна': "CNY"
              }

link1 = "https://world-weather.ru/pogoda/russia/moscow/"


def get_weather(link):
    r = requests.get(link).content
    soup = BeautifulSoup(r, "lxml")

    div_now_gr = soup.find("div", id="weather-now-number")
    now_gr = div_now_gr.getText()

    div_now_title = soup.find("div", class_="weather-now-info")
    span = div_now_title.find("span", id="weather-now-icon")
    now_title = span.get('title')

    dn = f"сейчас на улице {now_gr}, {now_title}"

    ul = soup.find("ul", id="vertical_tabs")
    spans = ul.find_all("span")
    data_days = ul.find_all("div", class_="day-week")
    data_month = ul.find_all("div", class_="month")
    data_dates = ul.find_all("div", class_="numbers-month")
    data_gr_at_day = ul.find_all("div", class_="day-temperature")
    data_gr_at_night = ul.find_all("div", class_="night-temperature")

    l_days = []
    l_dates = []
    l_gr_at_day = []
    l_gr_at_night = []
    l_title = list(filter(lambda x: x, map(lambda x: x.get("title"), spans)))

    for i in range(len(data_days)):
        l_days.append(data_days[i].getText())
        l_dates.append(data_dates[i].getText() + " " + data_month[i].getText())
        l_gr_at_day.append(data_gr_at_day[i].getText())
        l_gr_at_night.append(data_gr_at_night[i].getText())

    l_data = list(
        map(lambda day, date, gr_at_day, gr_at_night,
                   title: f"•{day}  {date}: днем {gr_at_day}, ночью {gr_at_night} - {title} ", l_days,
            l_dates, l_gr_at_day, l_gr_at_night, l_title))
    ww = "\n".join(l_data)
    return ww, dn


weak_weather_fc, data_now = get_weather(link1)
