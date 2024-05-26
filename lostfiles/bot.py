import telebot
from telebot import types
import sqlite3
import json
from datetime import date, datetime

bot = telebot.TeleBot('6956940513:AAF9iUMSw9Q-PiSd9R3KLF3JJ-AOZ2XIM1Y')

name = None
time = None
aud = None
photo = None
card_id = None


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Просмотр списка записей')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Добавление описания')
    btn3 = types.KeyboardButton('Удаление записи')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Дарова", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['show_list'])
def show_list(message):
    bot.send_message(message.chat.id, "Список потерянных предметов, занесённых в базу данных:")

    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT * FROM main_itemcard')
    cards = cur.fetchall()

    info = ''
    for el in cards:
        info += f'{el[0]}) Название: {el[1]}\nВремя нахождения: {el[4]}\nМесто нахождения: {el[5]}\nОписание: {el[6]}\n\n'

    cur.close()
    conn.close()
    bot.send_message(message.chat.id, info)


@bot.message_handler(commands=['delete'])
def delete_post(message):
    bot.send_message(message.chat.id, "Выберите номер записи, которую хотите удалить")
    bot.register_next_step_handler(message, delete_by_id)


def delete_by_id(message):
    card_id = message.text
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM main_itemcard WHERE id='{card_id}'")
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "Запись успешно удалена.")


@bot.message_handler(commands=['add_content'])
def add_content(message):
    bot.send_message(message.chat.id, "Выберите номер записи, которую хотите изменить")
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
    bot.send_message(message.chat.id, "Запись успешно обновлена.")


@bot.message_handler(commands=['refresh'])
def new_post(message):
    path = 'E330.json'

    with open(path, 'r') as f:
        data = json.loads(f.read())

        global name, time, aud, photo

        name = data[0]['item_name']
        #TODO формат времени без тире и говна всякого
        time = data[0]['date']
        aud = data[0]['aud']

        bot.send_message(message.chat.id, 'Информация о нахождении:')

        photo = open(f'./{data[0]["img_path"]}', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id,
                         f'Название: {name}\nВремя нахождения: {time}\nМесто нахождения: {aud} \n')

        photo = data[0]['img_path']

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Добавить запись', callback_data='add_post')
        btn2 = types.InlineKeyboardButton('Не добавлять', callback_data='no_add')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id,"Выберите дальнейшее действие:", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'add_post':
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM main_class WHERE name='{name}'")

        class_id = cur.fetchall()[0][0]
        time_create = str(datetime.now())

        #TODO слаг без двоеточий, контент чтоб не None а не добавлено был
        cur.execute(f"INSERT INTO main_itemcard (name, slug, photo, time_found, place_found, content, status, item_class_id, resp_user_id) VALUES ('{name}', '{name + str(time)}', '{photo}', '{time}', '{aud}', NULL, 1, '{class_id}', 1)")
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(callback.message.chat.id, "Запись успешно добавлена.")
        #TODO кнопка не отжимается
    elif callback.data == 'no_add':
        #TODO очищать ненужные данные
        bot.reply_to(callback.message.chat.id, "Запись не была добавлена.")


@bot.message_handler(content_types=['text'])
#TODO кнопки не должны прожиматься пока другие отрабатывают
def on_click(message):
    if message.text == 'Просмотр списка записей':
        show_list(message)
    elif message.text == 'Добавление описания':
        add_content(message)
    elif message.text == 'Удаление записи':
        delete_post(message)


bot.polling(none_stop=True)
