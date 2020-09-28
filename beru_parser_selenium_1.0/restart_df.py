# -*- coding: utf-8 -*-

import re
import pandas as pd
import telegram_bot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Pool
from multiprocessing import Process, Queue
from threading import Thread
from datetime import datetime
import time

URLS = [line.rstrip('\n') for line in open('beru_urls.txt', 'r')]
DF_PATH = 'cache\\data.csv'
COLUMNS = ['Название', 'Цена', 'Ссылка']
LAST_TITLE = ""
PAGES = ['', '&page=2#2-10', '&page=3#3-10', '&page=4#4-10']

df = pd.DataFrame([], columns=COLUMNS)
df.to_csv(DF_PATH, index=False, encoding='utf-8')


class PsrserBeru:
    def __init__(self, page):
        self.browser = webdriver.Chrome()
        self.next_page = page
        # self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        # self.options.add_argument('window-size=1920x935')
        # self.browser = webdriver.Chrome(chrome_options=self.options)

    def run(self):
        global LAST_TITLE
        urls = list(map(lambda x: x + self.next_page, URLS))
        page = self.next_page.lstrip('&page=').split('#')[0]
        page = '1' if page == '' else page
        while True:
            print(f"Process: {page} | {datetime.now()}")
            for url in urls:
                df_loaded = self.load_df()
                self.browser.get(url)
                # self.driver.find_element_by_xpath("//button[contains(@class, '_4qhIn2-ESi') and contains(@class, 'iJTPbCZAiZ') and contains(@class, '_2Ksnl1e_eZ') and contains(@class, '_39B7yXQbvm')]").click()
                # time.sleep(3)
                items = self.parse_page()
                for item in items:
                    if (item[0] not in list(df_loaded['Название'])) and (item[0] != LAST_TITLE):
                        LAST_TITLE = item[0]
                        self.send_message(item=list(item))
        # self.browser.close()

    def load_df(self):
        load_df = pd.read_csv(DF_PATH)
        return load_df

    def parse_page(self):
        titles = self.browser.find_elements_by_xpath("//div[@data-tid = '518f5fc0']")
        titles_list = [title.text.replace(',', '.') for title in titles]
        prices = self.browser.find_elements_by_xpath("//div[contains(@class, '_1u3j_pk1db')]")
        prices_list = [re.sub("^\s+|\n|\r|\s+$|₽| ", '', price.text) for price in prices]
        urls = self.browser.find_elements_by_xpath(
            "//a[contains(@class, '_3ioN70chUh') and contains(@class, 'Usp3kX1MNT') and contains(@class, '_3Uc73lzxcf')]")
        urls_list = [item.get_attribute('href') for item in urls]
        items_info = list(zip(titles_list, prices_list, urls_list))
        return items_info

    def send_message(self, item):
        print(item)
        df = pd.DataFrame([item], columns=COLUMNS)
        df.to_csv(DF_PATH, mode='a', header=None, index=False, encoding='utf-8')
        message_text = f'{item[0]}\r\nЦена: {item[1]}\r\n{item[2]}'
        # telegram_bot.send_message(message_text)

def run_pricess(page):
    parser = PsrserBeru(page=page)
    parser.run()

def main():
    with Pool(4) as process:
        process.map(run_pricess, PAGES)


if __name__ == '__main__':
        try:
            main()
        except Exception as e:
            print(f'Ошибка чтения страницы. Пожалуйста подождите...\n{e}')
            time.sleep(10)
            main()
