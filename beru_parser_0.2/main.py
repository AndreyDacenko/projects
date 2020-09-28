import requests
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing import Pool
import telegram_bot
import proxy_agent
import fake_useragent

last_item_title = ''


class ParserBeru:
    def __init__(self, url):
        self.agent = proxy_agent.chose_agent()
        self.proxy = proxy_agent.chose_proxy()
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            # 'User-Agent': self.agent,
            'Accept-Language': 'ru-Ru',
        }
        # self.session.proxies = {'http': self.proxy}
        self.url = url
        self.start_page = 'https://beru.ru'
        self.df_path = 'cache/data.csv'
        self.data = pd.read_csv(self.df_path)
        self.columns = ['Название', 'Цена', 'Ссылка']

    def get_page(self):
        res = self.session.get(url=self.url)
        res.raise_for_status()
        return res.text

    def parse_page(self):
        global last_item_title
        soup = BeautifulSoup(self.get_page(), 'lxml')
        items = soup.select('._34aqPZUfgr')
        if items:
            for item in items:
                item_url = item.select_one('a').get('href')
                item_url = self.start_page + item_url
                item_price = item.find('span', attrs={'data-tid': 'c3eaad93'}).text
                item_title = item.find('div', attrs={'data-tid': '518f5fc0'}).find('span', attrs={
                    'data-tid': '52906e8d'}).text.replace(',', '.')
                item_data = [item_title, item_price, item_url]
                if (item_title not in list(self.data['Название'])) and (item_title != last_item_title):
                    last_item_title = item_title
                    # self.send_message(item_data)

    def send_message(self, item_data):
        df = pd.DataFrame([item_data], columns=self.columns)
        df.to_csv(self.df_path, mode='a', header=None, index=False, encoding='utf-8')
        message_text = f'{item_data[0]}\r\nЦена: {item_data[1]}\r\n{item_data[2]}'
        # telegram_bot.send_message(message_text)
        print(item_data)


def make_processes(url):
    parser = ParserBeru(url=url)
    parser.parse_page()
    # parser.get_page()

def main():
    links = [line.rstrip('\n') for line in open('beru_urls.txt')]
    # make_processes('https://beru.ru')
    with Pool(1) as process:
        process.map(make_processes, links)


if __name__ == '__main__':
    while True:
        try:
            print(datetime.now())
            main()
        except Exception as e:
            print('Ошибка чтения страницы. Пожалуйста подождите...')
            print(e)
            time.sleep(5)
