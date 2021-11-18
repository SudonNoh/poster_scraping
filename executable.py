from web_control import web_controller
import time

process = web_controller()

user = ''
pw = ''
login_url = 'https://sitc2021.onlineeventpro.freeman.com/login'
poster_url = 'https://sitc2021.onlineeventpro.freeman.com/posters'
join_url = 'https://sitc2021.onlineeventpro.freeman.com'

process.login(user, pw, login_url)
process.get_url(poster_url)

link_list = []
count_link = 0

try:
    while True:
        page_link_list = process.for_url(join_url)
        link_list += page_link_list
        process.next_page(count_link)
        count_link += 1
        print(len(link_list))
except:
    print('출력이 끝났습니다.')

for i in link_list:
    process.get_url(i)
    process.go_to_site()
    process.print_window()


time.sleep(2)

process.driver_shutdown()

