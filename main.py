import schedule
import time
from modules.vk import get_token, get_subs
from modules.sql import *
from datetime import datetime

def create_tables():
    with open('groups_list.txt') as groups:
        group_list = []
        for group in groups:
            group_list.append(group.replace('vk.com/', '').strip('\n'))

    for group in group_list:
        # у одной из групп в названии прописана точка, что создаёт конфликт при создании SQL-таблицы с данным именем
        create_table(group.replace('.', '_'))
    return group_list


def job():
    conn = sqlite3.connect("groups_info.db")
    group_list = create_tables()
    date = datetime.today().strftime("%d.%m.%Y")
    
    for group in group_list:
        subs = get_subs(group, access_token)
        # мы ранее поменяли все точки в названиях групп на нижние подчёркивания
        add_data(group.replace('.', '_'), date, subs)
    print(f"Добавлена статистика за {date}")
    conn.close()


if __name__ == "__main__":
    access_token = input('Введите токен для ВК (если у Вас нет токена,\nнапечатайте "нет" и пройдите по ссылке): ')
    if access_token == "нет":
        get_token()
        access_token = input('Введите полученный токен для ВК: ')

    schedule.every().day.at("09:00").do(job)
    # для проверки работы кода:
    # schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)