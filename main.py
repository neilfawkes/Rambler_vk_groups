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
        # if group name contains a dot it will cause conflict when creating SQL-table
        create_table(group.replace('.', '_'))
    return group_list


def job():
    conn = sqlite3.connect("groups_info.db")
    group_list = create_tables()
    date = datetime.today().strftime("%d.%m.%Y")
    
    for group in group_list:
        subs = get_subs(group, access_token)
        # we replaced all dots in names with underscores earlier
        add_data(group.replace('.', '_'), date, subs)
    print(f"Added stats, {date}")
    conn.close()


if __name__ == "__main__":
    access_token = input("Input vk access token (if you don't have one please print 'no' and follow the link): ")
    if access_token == "no":
        get_token()
        access_token = input('Input vk access token: ')

    schedule.every().day.at("09:00").do(job)
    # for testing thw code use the following:
    # schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
