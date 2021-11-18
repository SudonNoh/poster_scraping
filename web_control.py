from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip

from bs4 import BeautifulSoup


class web_controller:

    def __init__(self):
        self.chrome_service = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('window-size=1920,1080')
        self.driver = webdriver.Chrome(service=self.chrome_service, options=self.options)
        self.driver.implicitly_wait(5)

    def login(self, user_id, user_pw, url):
        self.driver.get(url=url)

        elem = self.driver.find_element(By.ID, "email-address")
        elem.send_keys(user_id)
        elem = self.driver.find_element(By.ID, "confirmation-number")
        elem.send_keys(user_pw)
        elem.send_keys(Keys.ENTER)

    # for_url / go_to_site 전에 실행해야 함
    def get_url(self, url):
        self.driver.get(url=url)
        self.driver.implicitly_wait(5)

    def next_page(self, count_link):
        # 특정한 element를 알고 있을 때 그 위치로 이동
        next_btn =[
            '//*[@id="content"]/div[2]/div/div/div[2]/button',
            '//*[@id="content"]/div[2]/div/div/div[2]/button[2]'
        ]

        if count_link == 0:
            x = 0
        else:
            x = 1

        elem = self.driver.find_element(By.XPATH, next_btn[x])
        action = ActionChains(self.driver)
        action.move_to_element(elem).perform()

        elem.send_keys(Keys.ENTER)

    def for_url(self, url):
        time.sleep(5)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        link_list = []

        for href in soup.find_all('a', {'class': 'poster-card_outerHolder__1Hw6u card-wrapper_holder__3I_E0'}):
            link_list.append(url + href["href"])

        return link_list

    def go_to_site(self):

        iframe = self.driver.find_element(By.ID, "webviewr-1")
        self.driver.switch_to.frame(iframe)

        time.sleep(3)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/button[4]').click()
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[5]/div/button[2]').click()
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[11]/div/div/div[2]/div[2]/div/select').click()
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app"]/div[1]/div[11]/div/div/div[2]/div[2]/div/select/option[1]').click()
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[11]/div/div/div[4]/button').click()

    def print_window(self, file_name):
        # PDF dropdown 선택
        pyautogui.moveTo(1500, 165)
        pyautogui.click()

        # PDF로 변환 선택
        pyautogui.moveTo(1500, 220)
        pyautogui.click()

        # 확인버튼 클릭
        pyautogui.moveTo(1481, 908)
        pyautogui.click()

        time.sleep(1)

        # 저장 위치 변경
        pyautogui.moveTo(98, 196)
        pyautogui.click()

        # 제목 변경 위치까지 이동
        pyautogui.moveTo(231, 448)
        pyautogui.click()

        # 제목 변경
        pyautogui.press('delete')
        pyperclip.copy(file_name + '.pdf')
        pyautogui.hotkey('ctrl', 'v')

        # 저장
        pyautogui.moveTo(1071, 511)
        pyautogui.click()
        # 저장하는데, 시간이 필요함
        time.sleep(2)

    def driver_shutdown(self):
        self.driver.quit()
