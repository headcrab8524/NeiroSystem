import telebot
from telebot import types
import sqlite3
import json
from datetime import date, datetime
import time as t
import os
import shutil

bot = telebot.TeleBot('6956940513:AAF9iUMSw9Q-PiSd9R3KLF3JJ-AOZ2XIM1Y')

name = None
time = None
aud = None
photo = None
card_id = None
save_path = None
img_path_data = None
source_path = None
wait = False

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('Просмотр списка записей')
markup.row(btn1)
btn2 = types.KeyboardButton('Добавление описания')
btn3 = types.KeyboardButton('Удаление записи')
markup.row(btn2, btn3)
btn4 = types.KeyboardButton('Изменить статус записи')
markup.row(btn4)


@bot.message_handler(commands=['start'])
def start(message):
    #TODO оставлять ответственному только его jsonы
    bot.send_message(message.chat.id, "Дарова", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['info'])
def show_info(message):
    # TODO выводить информацию об ответственном лице (его кафедра, аудитории). Пока тут тестим message
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['show_list'])
def show_list(message):
    bot.send_message(message.chat.id, "Список потерянных предметов, занесённых в базу данных:",
                     reply_markup=types.ReplyKeyboardRemove())

    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT * FROM main_itemcard')
    cards = cur.fetchall()

    info = ''
    for el in cards:
        info += f'{el[0]}) Название: {el[1]}\nВремя нахождения: {el[4]}\nМесто нахождения: {el[5]}\nОписание: {el[6]}\nСтатус: {el[8]}\n'

    cur.close()
    conn.close()
    bot.send_message(message.chat.id, info, reply_markup=markup)


@bot.message_handler(commands=['delete'])
def delete_post(message):
    bot.send_message(message.chat.id, "Выберите номер записи, которую хотите удалить",
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, delete_by_id)


def delete_by_id(message):
    card_id = message.text
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM main_itemcard WHERE id='{card_id}'")
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "Запись успешно удалена.", reply_markup=markup)


@bot.message_handler(commands=['add_content'])
def add_content(message):
    bot.send_message(message.chat.id, "Выберите номер записи, которую хотите изменить",
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, update_by_id)


def update_by_id(message):
    global card_id
    card_id = message.text
    bot.send_message(message.chat.id, "Введите текст для добавления")
    bot.register_next_step_handler(message, update_content)


def update_content(message):
    content = message.text
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(f"UPDATE main_itemcard SET content='{content}' WHERE id='{card_id}'")
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "Запись успешно обновлена.", reply_markup=markup)


@bot.message_handler(commands=['change_status'])
def change_status(message):
    bot.send_message(message.chat.id, "Выберите номер записи, которую хотите изменить",
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, update_status_by_id)


def update_status_by_id(message):
    global card_id
    card_id = message.text
    bot.send_message(message.chat.id, "Задайте статус")
    bot.register_next_step_handler(message, update_status)


def update_status(message):
    status = message.text
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(f"UPDATE main_itemcard SET status='{status}' WHERE id='{card_id}'")
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "Запись успешно обновлена.", reply_markup=markup)


@bot.message_handler(commands=['refresh'])
def new_post(message):
    global wait
    path = 'data.json'

    with open(path, 'r') as f:
        data = json.loads(f.read())

    global name, time, aud, photo, save_path, img_path_data, source_path

    for el in data:
        wait = True
        name = el[0]['item_name']
        time = el[0]['date']
        aud = el[0]['aud']
        img_path_data = el[0]["img_path"].split("-")

        bot.send_message(message.chat.id, 'Информация о нахождении:')

        photo = open(f'./{el[0]["img_path"]}', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id,
                             f'Класс предмета: {name}\nВремя нахождения: {time}\nМесто нахождения: {aud} \n')

        photo = f'./{el[0]["img_path"]}'
        source_path = f'{el[0]["img_path"]}'

        inline_markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Добавить запись', callback_data='add_post')
        button2 = types.InlineKeyboardButton('Не добавлять', callback_data='no_add')
        inline_markup.row(button1, button2)
        bot.send_message(message.chat.id, "Выберите дальнейшее действие:", reply_markup=inline_markup)

        while wait:
            t.sleep(1)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global source_path, wait
    if callback.data == 'add_post':

        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute(f"SELECT id, rus_name FROM main_class WHERE name='{name}'")

        info = cur.fetchall()
        class_id = info[0][0]
        rus_name = info[0][1]

        destination_path = f"./media/photos/{img_path_data[0]}/{img_path_data[1]}/{img_path_data[2]}/"
        save_path = destination_path.replace('./media/', '') + str(source_path)

        cur.execute(f"INSERT INTO main_itemcard (name, slug, photo, time_found, place_found, content, status, item_class_id, resp_user_id) VALUES ('{rus_name}', '{str(name).replace(' ', '_') + str(time).replace(':', '-')}', '{save_path.replace('./', '')}', '{time}', '{aud}', 'Не добавлено', 1, '{class_id}', 1)")
        conn.commit()
        cur.close()
        conn.close()

        if not os.path.exists(destination_path):
            os.makedirs(destination_path, exist_ok=True)
        shutil.copy2(source_path, destination_path)

        bot.send_message(callback.message.chat.id, "Запись успешно добавлена.", reply_markup=markup)

    elif callback.data == 'no_add':
        bot.send_message(callback.message.chat.id, "Запись не была добавлена.", reply_markup=markup)

    wait = False


@bot.message_handler(content_types=['text'])
def on_click(message):
    if message.text == 'Просмотр списка записей':
        show_list(message)
    elif message.text == 'Добавление описания':
        add_content(message)
    elif message.text == 'Удаление записи':
        delete_post(message)
    elif message.text == 'Изменить статус записи':
        change_status(message)


bot.polling(none_stop=True)
