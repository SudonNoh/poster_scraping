from web_control import web_controller
import pandas as pd
import openpyxl as op
import os
import time
import json

# user id 와 user pw를 저장한 파일
with open('user.json') as f:
    data = json.load(f)

process = web_controller()

user = data['id']
pw = data['pw']

login_url = 'https://sitc2021.onlineeventpro.freeman.com/login'
poster_url = 'https://sitc2021.onlineeventpro.freeman.com/posters'
join_url = 'https://sitc2021.onlineeventpro.freeman.com'

process.login(user, pw, login_url)
process.get_url(poster_url)

data_frame_list = []
hyperlink = []
count_link = 0

try:
    while True:
        page_data, col_list, hyperlink_list = process.for_url(join_url)
        data_frame_list += page_data
        hyperlink += hyperlink_list
        process.next_page(count_link)
        count_link += 1
except:
    print('출력이 끝났습니다.\nExcel로 출력합니다.')

# Excel 로 먼저 추출
excel = pd.DataFrame(data_frame_list, columns=col_list)
export_excel = excel[['number', 'title', 'link']]
filepath = "C:/Users/SD NOH/Desktop/pdf/excel.xlsx"
export_excel.to_excel(filepath)

# hyperlink를 수식으로 입력
# wb = op.load_workbook(filepath)
# ws = wb.active

# ws.rows는 excel file의 가장 마지막 행에 있는 data의 행의 위치
# for r, link, count in zip(ws.rows, hyperlink, range(len(hyperlink))):
#     '''
#     출력: r: '(<Cell 'Sheet1'.A1>, <Cell 'Sheet1'.B1>, <Cell 'Sheet1'.C1>, <Cell 'Sheet1'.D1>)'
#     출력: hyperlink: '=HYPERLINK('960.pdf', 'HYPERLINK:960')'
#     '''
#     count = str(count+2)
#     ws['E'+count] = link
#
# wb.save("C:/Users/SD NOH/Desktop/pdf/excel_hyperlink.xlsx")

print("PDF 저장을 시작합니다.")
count = 0
for i in data_frame_list:
    for j in range(3):
        file_list = os.listdir("C:/Users/SD NOH/Desktop/pdf")
        if i[0]+".pdf" in file_list:
            pass
        else:
            print(j, "\n\n")
            print(i[0], ": ", i[2])
            if j == 2:
                process.driver_shutdown()
                process = web_controller()
                time.sleep(3)
                process.login(user, pw, login_url)
            else:
                pass
            process.get_url(i[2])
            try:
                process.go_to_site()
            except:
                pass
            time.sleep(1)
            try:
                process.print_window(i[0], count)
            except:
                pass
            count = 1

time.sleep(2)

process.driver_shutdown()
print("PDF 저장이 끝났습니다.")
