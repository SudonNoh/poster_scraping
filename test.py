from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip
from bs4 import BeautifulSoup

chrome_service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')
# options.add_argument('headless')
# window size 설정: 'window-size=1920,1080'
# background 실행: 'headless'
driver = webdriver.Chrome(service=chrome_service, options=options)
driver.implicitly_wait(5)

driver.get(url='https://sitc2021.onlineeventpro.freeman.com/login')

user = ''
pw = ''

elem = driver.find_element(By.ID, "email-address")
elem.send_keys(user)
elem = driver.find_element(By.ID, "confirmation-number")
elem.send_keys(pw)
elem.send_keys(Keys.ENTER)

driver.get(url='https://sitc2021.onlineeventpro.freeman.com/posters')
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
y = soup.find_all('h2', {'class': 'poster-card_posterTitle__1v0C4'})
count = 0
for i in y:
    count += 1
    print(count)
    if not i("span"):
        print(i.text)
    else:
        print(i("span")[0]["title"])


print(soup.find_all('a', {'class': 'poster-card_outerHolder__1Hw6u card-wrapper_holder__3I_E0'}))

for href in soup.find_all('a', {'class': 'poster-card_outerHolder__1Hw6u card-wrapper_holder__3I_E0'}):
    print('https://sitc2021.onlineeventpro.freeman.com' + href["href"])

driver.quit()






time.sleep(2)
driver.get(url='https://sitc2021.onlineeventpro.freeman.com/login?redirect_uri=/posters/30838579/Dissecting--catenin-associated-inflammation-in-patients-with-desmoid-fibromatosis-to-identify-prognostic-biomarkers')

time.sleep(3)
iframe = driver.find_element(By.ID, "webviewer-1")
driver.switch_to.frame(iframe)

time.sleep(5)
driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/button[4]').click()
driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[5]/div/button[2]').click()
driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[11]/div/div/div[2]/div[2]/div/select').click()
driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[11]/div/div/div[2]/div[2]/div/select/option[1]').click()
driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[11]/div/div/div[4]/button').click()

time.sleep(2)
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
pyperclip.copy("1번.pdf")
pyautogui.hotkey('ctrl', 'v')

# 저장
pyautogui.moveTo(1071, 511)
pyautogui.click()
# 저장하는데, 시간이 필요함
time.sleep(2)

# position = pyautogui.position()
# print('이름 변경 포지션')
# print('position x:', position.x)
# print('position y:', position.y)

driver.quit()
