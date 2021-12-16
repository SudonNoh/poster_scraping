
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

from bs4 import BeautifulSoup


# user id 와 user pw를 저장한 파일
with open('user.json') as f:
    data = json.load(f)

user = data['id']
pw = data['pw']

login_url = "https://lifesciences.connectmeinforma.com/login?reason=205"
poster_site_enter_url = "https://lifesciences.connectmeinforma.com/lobby/events"
poster_url = "https://lifesciences.connectmeinforma.com/posters"

chrome_service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')
driver = webdriver.Chrome(service=chrome_service, options=options)
driver.implicitly_wait(5)
driver.get(url=login_url)

elem = driver.find_element(By.ID, 'loginForm_email')
elem.send_keys(user)
elem = driver.find_element(By.ID, 'loginPassword')
elem.send_keys(pw)
elem.send_keys(Keys.ENTER)
time.sleep(5)

driver.get(url=poster_site_enter_url)
xpath = '//*[@id="root"]/div/div/div/div[2]/div/div[2]/div/div/div[3]/button'
driver.find_element(By.XPATH, xpath).click()

driver.get(url=poster_url)

time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

driver.quit()

selected_soup = soup.select('div.css-0 > div.css-0')

total_data = []
link = []
count = 0
for i in selected_soup:

    length = int(len(i('p'))/4)
    for count_num, img in zip(range(length), i('img')):
        line_data = []
        # count
        count += 1
        print('\ncount : ', count)
        line_data.append(count)

        # category
        print(i('h2')[0].text)
        line_data.append(i('h2')[0].text)

        print('category : ', i('h2')[0].text)

        num = count_num+(3*count_num)
        # title
        print('title : ', i('p')[num].text)
        line_data.append(i('p')[num].text)
        print('abstract : ', i('p')[num+1].text)
        line_data.append(i('p')[num+1].text)
        print('author : ', i('p')[num+2].text)
        line_data.append(i('p')[num+2].text)
        print('position : ', i('p')[num+3].text)
        line_data.append(i('p')[num+3].text)
        print('link : ', img['src'])
        link.append(img['src'])
        print('hyper : ', img['src'])

        total_data.append(line_data)

col_list = ['SN', 'Category', 'Title', 'Abstract', 'Author', 'Position']
excel = pd.DataFrame(total_data, columns=col_list)
file_path = 'C:/Users/SD NOH/Desktop/노수돈/SIT/BD/'
excel.to_excel(file_path + 'excel.xlsx')


# wb = op.load_workbook(file_path + 'excel.xlsx')
# ws = wb.active
#
# for cell in ws["G"]:
#     print(cell)
#     cell.value = "안녕"
#
#
# for r, hyperlink, count in zip(ws.rows, link, range(len(link))):
#     count = str(count+2)
#     ws['G'+count].value = "Link"
#     ws['G'+count].hyperlink = hyperlink
#     ws['G'+count].style = "Hyperlink"
#
# wb.save(file_path + 'excel.xlsx')