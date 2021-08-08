from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import ftplib
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

options = webdriver.ChromeOptions()
# options.headless = True
options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')


class SeekingAlpha():
    today_date = datetime.datetime.today().strftime("%Y-%m-%d")
    filename = f'output-{today_date}.csv'

    def __init__(self):

        self.error_page = 1

        self.working()

    def working(self):

        try:

            self.driver = webdriver.Chrome('chromedriver.exe', options=options)

            self.createFolder('data')

            for i in range(self.error_page, 11):

                self.page = i

                url = f"https://seekingalpha.com/earnings/earnings-calendar/{i}"

                self.driver.get(url)

                earnings_table = self.driver.find_element_by_css_selector('table.earningsTable')

                earnings_table_body = earnings_table.find_element_by_css_selector("tbody")

                all_rows = earnings_table_body.find_elements_by_css_selector('tr')

                if not os.path.isdir('data'):
                    os.makedirs('data')

                for row in all_rows:

                    data_list = str(row.text).split('\n')

                    if len(data_list) > 1 and len(data_list) != 0:
                        symbol = data_list[0]
                        name = data_list[1]
                        date = str(data_list[2]).split(' ')

                        release_date = date[0]
                        release_time = date[1]

                        data_to_csv = {
                            'Symbol': symbol,
                            'Name': name,
                            'Release Date': release_date,
                            'Release Time': release_time
                        }

                        if not os.path.exists(f'data/{self.filename}'):
                            self.csvCreater()
                            self.csvupdate(data_to_csv)
                        else:
                            self.csvupdate(data_to_csv)
                        print(symbol, name, release_date, release_time)
                # sleep(30)

            self.driver.quit()
        except NoSuchElementException:
            self.driver.quit()

            self.error_page = self.page

            sleep(3)

            self.working()

    def csvCreater(self):
        with open('data/' + f'{self.filename}', 'w', newline='', encoding="utf-8") as file:
            fieldNames = ['Symbol', 'Name', 'Release Date', 'Release Time']
            thewriter = csv.DictWriter(file, fieldnames=fieldNames)
            thewriter.writeheader()

    def csvupdate(self, data_to_csv):
        with open('data/' + f'{self.filename}', 'a', newline='', encoding="utf-8") as file:
            fieldNames = ['Symbol', 'Name', 'Release Date', 'Release Time']
            thewriter = csv.DictWriter(file, fieldnames=fieldNames)
            thewriter.writerow(data_to_csv)

    def createFolder(self, name):
        print(name)
        try:
            os.mkdir(name)
            print("\nDirectory ", name, " Created ")
        except FileExistsError:
            print("\nDirectory ", name, " already exists")


bot = SeekingAlpha()
