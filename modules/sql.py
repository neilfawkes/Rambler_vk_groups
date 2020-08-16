import sqlite3
import pandas as pd

conn = sqlite3.connect("groups_info.db")
cursor = conn.cursor()

def create_table(table_name):
    query = "CREATE TABLE IF NOT EXISTS {table} (date text, subs text)"
    cursor.execute(query.format(table=table_name))


def add_data(table_name, date, subs):
    # переменная date выделена для того, чтобы SQL игнорировал точки в дате и не выдавал ошибку
    query = "INSERT INTO {table} VALUES ('" + date + "', {subs})"
    cursor.execute(query.format(table=table_name, date=date, subs=subs))
    conn.commit()


def print_table(table_name):
    query = "select * from {table}"
    print(table_name)
    print(pd.read_sql(query.format(table=table_name), conn), end='\n\n')


def add_column(table_name, column_name):
    '''
    Функция добавления новой колонки в существующие таблицы.
    Не реализована, но может быть добавдлена при необходимости собирать дополнительную информацию о сообществах.
    '''
    query = "ALTER TABLE {table} ADD COLUMN {column} text"
    cursor.execute(query.format(table=table_name, column=column_name))


if __name__ == "__main__":
    with open('groups_list.txt') as groups:
        group_list = []
        for group in groups:
            group_list.append(group.replace('vk.com/', '').strip('\n'))
    
    for group in group_list:
        print_table(group.replace('.', '_'))
    
    conn.close()