import telebot
from telebot import types
from config import TOKEN
from pymysql import Error
import sqlite3
import time
import os

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    try:

        # for i in range(len(prices)):
        #     cursor.execute('INSERT INTO products (name, price, type) VALUES (?, ?, ?)',
        #     [list(prices.keys())[i], prices[list(prices.keys())[i]], 'шт'])
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text="Отправить номер телефона", request_contact=True))
        bot.send_message(chat_id=message.chat.id, text='Пожалуйста, нажмите кнопку ниже для отправки номера телефона,'
                                                       ' это нужно для совершения заказов:',
                         reply_markup=markup)

    except Exception as e:
        print(e)




@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        try:
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("""INSERT INTO users (phone, user_id, name) VALUES (?, ?, ?)""",
                           [message.contact.phone_number, message.chat.id, message.chat.first_name])
            cursor.close()
            connect.commit()
            connect.close()
        except sqlite3.IntegrityError as e:
            pass
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        btn2 = types.KeyboardButton("Корзина")
        btn4 = types.KeyboardButton("Телефон оператора")
        btn5 = types.KeyboardButton("О нас")
        btn6 = types.KeyboardButton("Информация о доставке")
        markup.add(btn1, btn2)
        markup.add(btn4, btn5)
        markup.add(btn6)
        bot.send_photo(message.chat.id, photo=open('photos/2022-10-07 7.05.00 PM.jpg', 'rb'), caption='''{0.first_name}, Добро Пожаловать в Наш магазин Азбука Океана! 🐟🐠

У нас представлен  прекрасный  выбор охлаждённой и мороженой рыбы, морепродуктов, консервов, икры, а также продукции собственного производства.
Еженедельные обновления, акции, которые делают покупки еще более приятными и дополнительные скидки (да и такое у нас бывает) — здесь вы узнаете об этом первыми😉

Мы находимся по адресу: Казань, ул. Гвардейская, 14.

Режим работы с 09:00 - 20:00

Принимаем заказы и отвечаем на ваши вопросы онлайн и по телефону +79872151533

Итак, нажмите «Меню»'''.format(
            message.from_user), reply_markup=markup)


jk = {}
adres = {}
komm = {}
dostavka = {}
prices = {'Икра Кеты вес - 7000р/кг': 700, 'Икра Горбуши вес - 5900р/кг': 590, 'Икра Осетра 100гр': 6090, 'Икра Осетра 50гр': 3050,
          'Икра Стерляди 100гр': 5075, 'Икра Стерляди 50гр': 2535, 'Икра Палтуса 90г ст/б': 440, 'Икра Щуки  113гр, ст/б': 720,
          'Икра Сига 120г ж/б с/к': 135, 'Икра Трески Премиум 170гр': 175, 'Икра Сельди 120г ж/б с/к': 115,
          'Икра Минтая Премиум 170гр': 175, 'Икра Минтая 120г ж/б с/к': 110,
            #БАДЫ
          'Из дикого лосося 600 мг блистер': 410, 'Из дикого лосося 300мг(мал.)блистер': 372,
          'Из дикого лосося 300мг(апел.)блистер': 372, 'Из дикого лосося 1000 мг блистер': 620,
          'Из дикого камч.лосося 1000мг банка': 1885,
            #Вяленая рыба
          'Нерка х/к АО - 1650р/кг': 330, 'Корюшка вяленая с икрой - 2755р/кг': 551,
          'Филе Сёмги сл/сол АО - 2650р/кг': 530, 'Скумбрия х/к АО': 580,
            #Консервы
          '"Сырок в желе" 240гр': 127, 'Ряпушка сиб. обж. в масле': 143, '"Пыжьян в желе" 240гр': 127,
          '"Язь в желе" 240гр': 127, 'Тефтели частиковые в том. соусе': 94, 'Сырок обжаренный в том. соусе': 96,
          'Ряпушка сиб. нат. с доб. масла': 127, 'Фрик. из рыб с овощ.в том.соусе': 85, 'Налим филе натур с доб. масла': 94,
          'Щука натуральная с доб. масла': 110, 'Фрик. из сиговых рыб': 98, 'Щука в томатном соусе': 97,
          'Сырок в томатном соусе': 116, 'Налим филе обж. в том. соусе': 100, 'Налим натур с доб. масла': 110,
          'Ряпушка сибирская копч в масле': 180, 'Щука обжаренная в томатном соусе': 104, 'Язь обжаренный в масле': 98,
          'Сугудай из Муксуна 200гр': 550, 'Сугудай из Чира 200 гр': 530, 'Сугудай из Омуля 200гр': 510,
          'Сугудай из Сига 200гр': 465,
            #Морепродукты
          'Гребешок сев.курL 1/12 (нефасов.)': 2200, 'Кальмар-Трубки без глазури': 460, 'Коктейль в масле из морепродуктов': 990,
          'Морской коктейль с/м вес': 550, 'Крев очищ. без хв. 31/40 Ваннамей': 1550, 'Креветки Аргентина 31/50 в панцире': 1550,
          'Креветки (21-25) с/м очищ с хв 1 кг': 1295, 'Крев Арг.Крас. с/м очищ 20/30 500г': 890, 'Крев Ваннамей с/м б/г 26-30,500г': 930,
          'Крев Арг. Крас. с/м в панц 20/30 1кг': 1300, 'Мидии Киви, на половинках раковины': 1155,
          'Мидии в/м 200/300': 720, 'Рапан мясо': 727, 'Угорь жареный под соусом, 200гр': 395,
            #Рыба
          'Сёмга охлаждённая 3-4кг': 1600, 'Форель охлаждённая': 1100, 'Дорадо охлаждённая 400-600г': 790, 'Горбуша ПБГ': 500,
          'Камбала Палтусовидная с/м': 550, 'Скумбрия Атлант с/м ПБГ': 390, 'Дори с/м': 485,
          'Сибас охл с/г': 830, 'Стейк Угольной рыбы чищ': 1625, 'Стейк Палтуса чищ': 1310, 'Стейк Сёмги с/м': 1880,
          'Стейк Сёмги охлаждённый': 1950, 'Стейк Камбалы чищ': 695, 'Тунец (филе в/у 2-4)': 1630, 'Филе Хека в тубах 50*8см': 495,
          'Филе Горбуши Polar порц 6х400': 410, 'Филе Форели': 1580,
          'Филе пангасиуса с/м 5% глазурь': 445, 'Форель чищенная с/м': 1290, 'Голец': 550,
          'Дорадо чищенная': 950, 'Конгрио с/м': 770, 'Минтай б/г с/м': 240, 'Палтус охлаждённый': 1260,
          'Сёмга Чили 5-6 кг с/м': 1600, 'Суп набор (в асс-те)': 280, 'Суп набор Форели': 280, 'Терпуг Курильский с/м': 355,
          'Угольная рыба, ПБГ': 1440, 'Тушка Форели ': 1390, 'Стейк Нерки с/м': 1330,
          #Салаты
          'Салат из морской водорослей (Чука)': 510,
          #Соусы
          'Соус слад чили для роллов 360г': 215, 'Соус соевый сладкий ст/б 300мл': 310, 'Соус "Паста Том Ям" 50гр': 77,
          'Соус кисло-сладкий 300мл, ст/бут': 195, 'Соус соевый ORGANIC 300мл, ст/бут': 180,
          'Соус из чёрных соевых бобов 280гр': 255, 'Соус чили с лимоном, 150 мл': 245,
          'Соус соевый ORGANIC 150мл, ст/бут': 159, 'Соус Терияки(для маринада) 200мл': 208,
          'Соус Унаги для морепродуктов 200мл': 205, 'Соус Кимчи 200мл, ст/б': 247, 'Устричный высш кат 148г ст/бут': 150,
          'Пряный из лонгана имбиря 150мл': 275, 'Острый соус для крев и мидий 315г': 210, 'Соус "Рыбный" 200мл ст/б': 200, 'Чили кисло-сладкий (мягкий) 200гр': 195,
          'Соус соевый слабосоленый 300 мл': 175, 'Соус ЦУЮ соевый 300 мл конц.': 360,
          'Кисло-сладкий с ананасами, 150 мл': 295, 'Острый соус с хруст. перцем чили': 282,

          }



@bot.message_handler(content_types=['text'])
def func(message):

    if message.text == "Время работы":
        bot.send_message(message.chat.id, text="Мы работаем каждый день с 9:00 до 20:00 мск")
    elif message.text == 'Телефон оператора':
        bot.send_message(message.chat.id, text ="телефон: +7 (987) 215-15-33")
    elif message.text == 'Меню':
        markup = types.InlineKeyboardMarkup()
        button2 = types.InlineKeyboardButton(text="БАДЫ (Омега-3)", callback_data='БАДЫ (Омега-3)')
        button3 = types.InlineKeyboardButton("Вяленая рыба", callback_data='Вяленая рыба')
        button4 = types.InlineKeyboardButton("Икра", callback_data='Икра')
        button5 = types.InlineKeyboardButton("Консервы", callback_data='Консервы')
        button6 = types.InlineKeyboardButton("Морепродукты", callback_data='Морепродукты')
        button7 = types.InlineKeyboardButton("Свежемороженая рыба", callback_data='Свежемороженая рыба')
        button9 = types.InlineKeyboardButton("Салаты", callback_data='Салаты')
        button0 = types.InlineKeyboardButton("Соусы", callback_data='Соусы')
        button10 = types.InlineKeyboardButton("Охлажденная рыба", callback_data='Охлажденная рыба')

        markup.add(button10)
        markup.add(button7)
        markup.add(button3)
        markup.add(button6)
        markup.add(button4)
        markup.add(button5, button2)
        markup.add(button9, button0)
        res = bot.send_photo(chat_id=message.chat.id, photo=open('photos/M6f3ezYuvsY.jpeg', 'rb'))
        jk[message.chat.id] = []
        jk[message.chat.id].append(res.id)
        bot.send_message(message.chat.id, text='Выберите нужную вам категорию:',
                       reply_markup=markup)
    elif message.text == 'Корзина':


        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute('SELECT product_id FROM cart WHERE user_id=?', [message.chat.id])
        rows = cursor.fetchall()
        rowsprices = [''.join(i) for i in rows]
        newrows = []
        for i in rowsprices:
            cursor.execute('SELECT amount FROM cart WHERE product_id=? AND user_id=?',
                           [i, message.chat.id])
            amount = cursor.fetchone()[0]
            newrows.append(prices[i] * amount)
        for i in dict(zip(rowsprices, newrows)):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Увеличить', callback_data=f'{i}+'), types.InlineKeyboardButton(text='Уменьшить', callback_data=f'{i}-'))
            markup.add(types.InlineKeyboardButton(text='❌ Удалить', callback_data=f'{i}❌'))
            cursor.execute('SELECT amount FROM cart WHERE product_id=? AND user_id=?',
                                    [i, message.chat.id])
            amount = cursor.fetchone()[0]
            cursor.execute('SELECT type FROM products WHERE name=?', [i])
            type = cursor.fetchone()[0]

            bot.send_message(chat_id=message.chat.id, text=f'{i} - {amount} {type} - {dict(zip(rowsprices, newrows))[i]}р', reply_markup=markup)
        if sum(newrows) > 0:
            print()
            print(newrows)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Оформить заказ', callback_data="Заказ"))

            bot.send_message(text=f'Общая сумма заказа: {sum(newrows)}р'
                                  f' \nОбратите внимание, что итоговая стоимость может отличаться'
                                  f' \n \n Для оформления заказа нажмите на кнопку ниже',
                             chat_id=message.chat.id, reply_markup=markup)
        else:
            bot.send_message(text='Кажется, в корзине еще ничего нет!', chat_id=message.chat.id)

        cursor.close()
        connect.commit()
        connect.close()
    elif message.text == 'О нас':
        bot.send_message(text='''Мы - магазин Азбука Океана. 
У нас представлен  прекрасный  выбор охлаждённой и мороженой рыбы, морепродуктов, консервов, икры, а также продукции собственного производства.
Еженедельные обновления, акции, которые делают покупки еще более приятными и дополнительные скидки (да и такое у нас бывает) — здесь вы узнаете об этом первыми😉

Мы находимся по адресу: Казань, ул. Гвардейская, 14.

Режим работы с 09:00 - 20:00

Принимаем заказы и отвечаем на ваши вопросы онлайн и по телефону +7 (987) 215-15-33''', chat_id=message.chat.id)
    # elif message.text == 'обновление бд':
    #     # def func():
    #     #     dir_name = "/Users/grasmurr/PycharmProjects/fish_shop/фото"
    #     #     test = os.listdir(dir_name)
    #     #     g = [i for i in sorted(prices)]
    #     #     f1 = [os.path.abspath(i) for i in sorted(test) if not os.path.abspath(i).endswith('Store')]
    #     #     f2 = ['/home1/фото' + i[i.rfind('/'):] for i in f1]
    #     #     print(f2)
    #     #
    #     #     connect = sqlite3.connect('users.db')
    #     #     cursor = connect.cursor()
    #     #
    #     #     for i in range(len(prices)):
    #     #         cursor.execute('UPDATE products SET photo =? WHERE name=?', [f2[i], g[i]])
    #     #     cursor.close()
    #     #     connect.commit()
    #     #     connect.close()
    #     #     bot.send_message(message.chat.id, text="Успешно!")
    #     pass
    elif message.text == 'Информация о доставке':
        bot.send_message(text='''Заказ можно забрать самовывозом либо заказать доставку

Бесплатная доставка осуществляется от 2000р

Платная - заказом яндекс такси до вашего места нахождения

Мы находимся по адресу: Казань, ул. Гвардейская, 14.''', chat_id=message.chat.id)

    else:
        zakaz = ''
        komm[message.chat.id] = message.text

        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        cursor.execute('SELECT product_id FROM cart WHERE user_id=?', [message.chat.id])
        rows = cursor.fetchall()
        rowsprices = [''.join(i) for i in rows]
        newrows = []
        for i in rowsprices:
            cursor.execute('SELECT amount FROM cart WHERE product_id=? AND user_id=?',
                           [i, message.chat.id])
            amount = cursor.fetchone()[0]
            newrows.append(prices[i] * amount)

        if sum(newrows) > 0:


            for i in dict(zip(rowsprices, newrows)):
                cursor.execute('SELECT amount FROM cart WHERE product_id=? AND user_id=?',
                               [i, message.chat.id])
                amount = cursor.fetchone()[0]
                cursor.execute('SELECT type FROM products WHERE name=?', [i])
                type = cursor.fetchone()[0]
                zakaz += f'{i} - {amount} {type} - {dict(zip(rowsprices, newrows))[i]}р \n \n'

            markup = types.InlineKeyboardMarkup()
            button2 = types.InlineKeyboardButton(text="Подтвердить", callback_data='Подтверждаю')
            button3 = types.InlineKeyboardButton(text='Изменить комментарий', callback_data='komm')
            button4 = types.InlineKeyboardButton(text="Отменить", callback_data='Отмена')

            markup.add(button2, button3)
            markup.add(button4)

            if dostavka[message.chat.id] == 'Нет':
                bot.send_message(chat_id=message.chat.id, text=f'Ваш заказ:\n\n{zakaz}\nОбщая сумма заказа: {sum(newrows)}р\n\nКомментарий: {komm[message.chat.id]} ', reply_markup=markup)
            else:
                if sum(newrows) < 2000:
                    bot.send_message(chat_id=message.chat.id,
                                 text=f'Ваш заказ:\n\n{zakaz}\nОбщая сумма заказа: {sum(newrows)}р\n\nКомментарий: {komm[message.chat.id]} \n \nСтоимость доставки будет включена отдельно в стоимость заказа',
                                 reply_markup=markup)
                else:
                    bot.send_message(chat_id=message.chat.id,
                                     text=f'Ваш заказ:\n\n{zakaz}\nОбщая сумма заказа: {sum(newrows)}р\n\nКомментарий: {komm[message.chat.id]} ',
                                     reply_markup=markup)

        else:
            bot.send_message(chat_id=message.chat.id, text=f'На такую программу я не запрограммирован')






a = []
          #Икра




@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    try:
        req = call.data.split('_')[0]
        a.append(req)
        if len(a) > 150:
            del a[:100]
        print(a)
        if req == 'Икра':
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Икра Кеты вес - 7000р/кг', callback_data='Икра Кеты вес - 7000р/кг'))
            markup.add(types.InlineKeyboardButton(text='Икра Горбуши вес - 5900р/кг', callback_data='Икра Горбуши вес - 5900р/кг'))
            markup.add(types.InlineKeyboardButton(text='Икра Осетра 100гр', callback_data='Икра Осетра 100гр'))
            markup.add(types.InlineKeyboardButton(text='Икра Осетра 50гр', callback_data='Икра Осетра 50гр'))
            markup.add(types.InlineKeyboardButton(text='Икра Стерляди 100гр', callback_data='Икра Стерляди 100гр'))
            markup.add(types.InlineKeyboardButton(text='Икра Стерляди 50гр', callback_data='Икра Стерляди 50гр'))
            markup.add(types.InlineKeyboardButton(text='Икра Палтуса 90г ст/б', callback_data='Икра Палтуса 90г ст/б'))
            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'),
                       types.InlineKeyboardButton(text='Следующая страница', callback_data='Икра 2 страница'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Икра 2 страница':
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Икра Щуки  113гр, ст/б', callback_data='Икра Щуки  113гр, ст/б'))
            markup.add(types.InlineKeyboardButton(text='Икра Сига 120г ж/б с/к', callback_data='Икра Сига 120г ж/б с/к'))
            markup.add(types.InlineKeyboardButton(text='Икра Трески Премиум 170гр', callback_data='Икра Трески Премиум 170гр'))
            markup.add(types.InlineKeyboardButton(text='Икра Сельди 120г ж/б с/к', callback_data='Икра Сельди 120г ж/б с/к'))
            markup.add(types.InlineKeyboardButton(text='Икра Минтая Премиум 170гр', callback_data='Икра Минтая Премиум 170гр'))
            markup.add(types.InlineKeyboardButton(text='Икра Минтая 120г ж/б с/к', callback_data='Икра Минтая 120г ж/б с/к'))
            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Икра'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'БАДЫ (Омега-3)':
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Из дикого лосося 300мг(мал.)блистер', callback_data='Из дикого лосося 300мг(мал.)блистер'))
            markup.add(types.InlineKeyboardButton(text='Из дикого лосося 300мг(апел.)блистер', callback_data='Из дикого лосося 300мг(апел.)блистер'))
            markup.add(types.InlineKeyboardButton(text='Из дикого лосося 600 мг блистер', callback_data='Из дикого лосося 600 мг блистер'))
            markup.add(types.InlineKeyboardButton(text='Из дикого лосося 1000 мг блистер', callback_data='Из дикого лосося 1000 мг блистер'))
            markup.add(types.InlineKeyboardButton(text='Из дикого камч.лосося 1000мг банка', callback_data='Из дикого камч.лосося 1000мг банка'))


            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Вяленая рыба':
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Нерка х/к АО - 1650р/кг', callback_data='Нерка х/к АО - 1650р/кг'))
            markup.add(types.InlineKeyboardButton(text='Скумбрия х/к АО', callback_data='Скумбрия х/к АО'))
            markup.add(types.InlineKeyboardButton(text='Филе Сёмги сл/сол АО - 2650р/кг', callback_data='Филе Сёмги сл/сол АО - 2650р/кг'))
            markup.add(types.InlineKeyboardButton(text='Корюшка вяленая с икрой - 2755р/кг', callback_data='Корюшка вяленая с икрой - 2755р/кг'))

            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Консервы':
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='"Сырок в желе" 240гр', callback_data='"Сырок в желе" 240гр'))
            markup.add(types.InlineKeyboardButton(text='Ряпушка сиб. обж. в масле', callback_data='Ряпушка сиб. обж. в масле'))
            markup.add(types.InlineKeyboardButton(text='"Пыжьян в желе" 240гр', callback_data='"Пыжьян в желе" 240гр'))
            markup.add(types.InlineKeyboardButton(text='"Язь в желе" 240гр', callback_data='"Язь в желе" 240гр'))
            markup.add(types.InlineKeyboardButton(text='Тефтели частиковые в том. соусе', callback_data='Тефтели частиковые в том. соусе'))
            markup.add(types.InlineKeyboardButton(text='Сырок обжаренный в том. соусе', callback_data='Сырок обжаренный в том. соусе'))
            markup.add(types.InlineKeyboardButton(text='Ряпушка сиб. нат. с доб. масла', callback_data='Ряпушка сиб. нат. с доб. масла'))
            markup.add(types.InlineKeyboardButton(text='Фрик. из рыб с овощ.в том.соусе', callback_data='Фрик. из рыб с овощ.в том.соусе'))
            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'), types.InlineKeyboardButton(text='Следующая страница', callback_data='Консервы 2 страница'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Консервы 2 страница':
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Налим филе натур с доб. масла', callback_data='Налим филе натур с доб. масла'))
            markup.add(types.InlineKeyboardButton(text='Щука натуральная с доб. масла', callback_data='Щука натуральная с доб. масла'))
            markup.add(types.InlineKeyboardButton(text='Фрик. из сиговых рыб', callback_data='Фрик. из сиговых рыб'))
            markup.add(types.InlineKeyboardButton(text='Щука в томатном соусе', callback_data='Щука в томатном соусе'))
            markup.add(types.InlineKeyboardButton(text='Сырок в томатном соусе', callback_data='Сырок в томатном соусе'))
            markup.add(types.InlineKeyboardButton(text='Налим филе обж. в том. соусе', callback_data='Налим филе обж. в том. соусе'))
            markup.add(types.InlineKeyboardButton(text='Налим натур с доб. масла', callback_data='Налим натур с доб. масла'))
            markup.add(types.InlineKeyboardButton(text='Ряпушка сибирская копч в масле', callback_data='Ряпушка сибирская копч в масле'))
            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Консервы'), types.InlineKeyboardButton(text='Следующая страница', callback_data='Консервы 3 страница'))

            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Консервы 3 страница':
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Щука обжаренная в томатном соусе', callback_data='Щука обжаренная в томатном соусе'))
            markup.add(types.InlineKeyboardButton(text='Язь обжаренный в масле', callback_data='Язь обжаренный в масле'))
            markup.add(types.InlineKeyboardButton(text='Сугудай из Муксуна 200гр', callback_data='Сугудай из Муксуна 200гр'))
            markup.add(types.InlineKeyboardButton(text='Сугудай из Чира 200 гр', callback_data='Сугудай из Чира 200 гр'))
            markup.add(types.InlineKeyboardButton(text='Сугудай из Омуля 200гр', callback_data='Сугудай из Омуля 200гр'))
            markup.add(types.InlineKeyboardButton(text='Сугудай из Сига 200гр', callback_data='Сугудай из Сига 200гр'))
            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Консервы 2 страница'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Морепродукты':
            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Гребешок сев.курL 1/12 (нефасов.)', callback_data='Гребешок сев.курL 1/12 (нефасов.)'))
            markup.add(types.InlineKeyboardButton(text='Кальмар-Трубки без глазури', callback_data='Кальмар-Трубки без глазури'))
            markup.add(types.InlineKeyboardButton(text='Коктейль в масле из морепродуктов', callback_data='Коктейль в масле из морепродуктов'))
            markup.add(types.InlineKeyboardButton(text='Морской коктейль с/м вес', callback_data='Морской коктейль с/м вес'))
            markup.add(types.InlineKeyboardButton(text='Крев очищ. без хв. 31/40 Ваннамей', callback_data='Крев очищ. без хв. 31/40 Ваннамей'))
            markup.add(types.InlineKeyboardButton(text='Креветки Аргентина 31/50 в панцире', callback_data='Креветки Аргентина 31/50 в панцире'))
            markup.add(types.InlineKeyboardButton(text='Креветки (21-25) с/м очищ с хв 1 кг', callback_data='Креветки (21-25) с/м очищ с хв 1 кг'))
            markup.add(types.InlineKeyboardButton(text='Крев Арг.Крас. с/м очищ 20/30 500г', callback_data='Крев Арг.Крас. с/м очищ 20/30 500г'))

            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'),
                       types.InlineKeyboardButton(text='Следующая страница', callback_data='Морепродукты 2 страница'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Морепродукты 2 страница':

            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Крев Ваннамей с/м б/г 26-30,500г', callback_data='Крев Ваннамей с/м б/г 26-30,500г'))
            markup.add(types.InlineKeyboardButton(text='Крев Арг. Крас. с/м в панц 20/30 1кг', callback_data='Крев Арг. Крас. с/м в панц 20/30 1кг'))
            markup.add(types.InlineKeyboardButton(text='Мидии Киви, на половинках раковины', callback_data='Мидии Киви, на половинках раковины'))
            markup.add(types.InlineKeyboardButton(text='Мидии в/м 200/300', callback_data='Мидии в/м 200/300'))
            markup.add(types.InlineKeyboardButton(text='Рапан мясо', callback_data='Рапан мясо'))
            markup.add(types.InlineKeyboardButton(text='Угорь жареный под соусом, 200гр', callback_data='Угорь жареный под соусом, 200гр'))
            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Морепродукты'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Свежемороженая рыба':

            markup = types.InlineKeyboardMarkup()


            markup.add(types.InlineKeyboardButton(text='Горбуша ПБГ', callback_data='Горбуша ПБГ'))
            markup.add(types.InlineKeyboardButton(text='Камбала Палтусовидная с/м', callback_data='Камбала Палтусовидная с/м'))
            markup.add(types.InlineKeyboardButton(text='Скумбрия Атлант с/м ПБГ', callback_data='Скумбрия Атлант с/м ПБГ'))
            markup.add(types.InlineKeyboardButton(text='Дори с/м', callback_data='Дори с/м'))
            markup.add(types.InlineKeyboardButton(text='Стейк Угольной рыбы чищ', callback_data='Стейк Угольной рыбы чищ'))
            markup.add(types.InlineKeyboardButton(text='Стейк Палтуса чищ', callback_data='Стейк Палтуса чищ'))

            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'), types.InlineKeyboardButton(text='Следующая страница', callback_data='Свежемороженая рыба 2 страница'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Свежемороженая рыба 2 страница':

            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Стейк Сёмги с/м', callback_data='Стейк Сёмги с/м'))
            markup.add(types.InlineKeyboardButton(text='Стейк Камбалы чищ', callback_data='Стейк Камбалы чищ'))
            markup.add(types.InlineKeyboardButton(text='Тунец (филе в/у 2-4)', callback_data='Тунец (филе в/у 2-4)'))
            markup.add(types.InlineKeyboardButton(text='Сёмга Чили 5-6 кг с/м', callback_data='Сёмга Чили 5-6 кг с/м'))
            markup.add(types.InlineKeyboardButton(text='Филе Хека в тубах 50*8см', callback_data='Филе Хека в тубах 50*8см'))
            markup.add(types.InlineKeyboardButton(text='Филе Горбуши Polar порц 6х400', callback_data='Филе Горбуши Polar порц 6х400'))

            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Свежемороженая рыба'), types.InlineKeyboardButton(text='Следующая страница', callback_data='Свежемороженая рыба 3 страница'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Свежемороженая рыба 3 страница':

            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Филе Форели', callback_data='Филе Форели'))
            markup.add(types.InlineKeyboardButton(text='Филе пангасиуса с/м 5% глазурь', callback_data='Филе пангасиуса с/м 5% глазурь'))
            markup.add(types.InlineKeyboardButton(text='Форель чищенная с/м', callback_data='Форель чищенная с/м'))
            markup.add(types.InlineKeyboardButton(text='Голец', callback_data='Голец'))
            markup.add(types.InlineKeyboardButton(text='Дорадо чищенная', callback_data='Дорадо чищенная'))
            markup.add(types.InlineKeyboardButton(text='Конгрио с/м', callback_data='Конгрио с/м'))


            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Свежемороженая рыба 2 страница'),
                       types.InlineKeyboardButton(text='Следующая страница', callback_data='Свежемороженая рыба 4 страница'))

            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Свежемороженая рыба 4 страница':

            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Минтай б/г с/м', callback_data='Минтай б/г с/м'))


            markup.add(types.InlineKeyboardButton(text='Суп набор (в асс-те)', callback_data='Суп набор (в асс-те)'))
            markup.add(types.InlineKeyboardButton(text='Суп набор Форели', callback_data='Суп набор Форели'))
            markup.add(types.InlineKeyboardButton(text='Терпуг Курильский с/м', callback_data='Терпуг Курильский с/м'))
            markup.add(types.InlineKeyboardButton(text='Угольная рыба, ПБГ', callback_data='Угольная рыба, ПБГ'))
            markup.add(types.InlineKeyboardButton(text='Тушка Форели ', callback_data='Тушка Форели '))
            markup.add(types.InlineKeyboardButton(text='Стейк Нерки с/м', callback_data='Стейк Нерки с/м'))

            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Свежемороженая рыба 3 страница'))

            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Салаты':

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Салат из морской водорослей (Чука)', callback_data='Салат из морской водорослей (Чука)'))
            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'))

            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Соусы':

            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Соус слад чили для роллов 360г', callback_data='Соус слад чили для роллов 360г'))
            markup.add(types.InlineKeyboardButton(text='Соус соевый сладкий ст/б 300мл', callback_data='Соус соевый сладкий ст/б 300мл'))
            markup.add(types.InlineKeyboardButton(text='Соус "Паста Том Ям" 50гр', callback_data='Соус "Паста Том Ям" 50гр'))
            markup.add(types.InlineKeyboardButton(text='Соус кисло-сладкий 300мл, ст/бут', callback_data='Соус кисло-сладкий 300мл, ст/бут'))
            markup.add(types.InlineKeyboardButton(text='Соус соевый ORGANIC 300мл, ст/бут', callback_data='Соус соевый ORGANIC 300мл, ст/бут'))
            markup.add(types.InlineKeyboardButton(text='Соус из чёрных соевых бобов 280гр', callback_data='Соус из чёрных соевых бобов 280гр'))
            markup.add(types.InlineKeyboardButton(text='Соус чили с лимоном, 150 мл', callback_data='Соус чили с лимоном, 150 мл'))

            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'),
                       types.InlineKeyboardButton(text='Следующая страница', callback_data='Соусы 2 страница'))
            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Соусы 2 страница':

            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Соус соевый ORGANIC 150мл, ст/бут', callback_data='Соус соевый ORGANIC 150мл, ст/бут'))
            markup.add(types.InlineKeyboardButton(text='Соус Терияки(для маринада) 200мл', callback_data='Соус Терияки(для маринада) 200мл'))
            markup.add(types.InlineKeyboardButton(text='Соус Унаги для морепродуктов 200мл', callback_data='Соус Унаги для морепродуктов 200мл'))
            markup.add(types.InlineKeyboardButton(text='Соус Кимчи 200мл, ст/б', callback_data='Соус Кимчи 200мл, ст/б'))
            markup.add(types.InlineKeyboardButton(text='Устричный высш кат 148г ст/бут', callback_data='Устричный высш кат 148г ст/бут'))
            markup.add(types.InlineKeyboardButton(text='Пряный из лонгана имбиря 150мл', callback_data='Пряный из лонгана имбиря 150мл'))
            markup.add(types.InlineKeyboardButton(text='Острый соус для крев и мидий 315г', callback_data='Острый соус для крев и мидий 315г'))

            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Соусы'),
                       types.InlineKeyboardButton(text='Следующая страница', callback_data='Соусы 3 страница'))

            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Соусы 3 страница':

            markup = types.InlineKeyboardMarkup()

            markup.add(types.InlineKeyboardButton(text='Соус "Рыбный" 200мл ст/б', callback_data='Соус "Рыбный" 200мл ст/б'))
            markup.add(types.InlineKeyboardButton(text='Чили кисло-сладкий (мягкий) 200гр', callback_data='Чили кисло-сладкий (мягкий) 200гр'))
            markup.add(types.InlineKeyboardButton(text='Соус соевый слабосоленый 300 мл', callback_data='Соус соевый слабосоленый 300 мл'))
            markup.add(types.InlineKeyboardButton(text='Соус ЦУЮ соевый 300 мл конц.', callback_data='Соус ЦУЮ соевый 300 мл конц.'))
            markup.add(types.InlineKeyboardButton(text='Кисло-сладкий с ананасами, 150 мл', callback_data='Кисло-сладкий с ананасами, 150 мл'))
            markup.add(types.InlineKeyboardButton(text='Острый соус с хруст. перцем чили', callback_data='Острый соус с хруст. перцем чили'))
            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='Соусы 2 страница'))

            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Охлажденная рыба':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Сёмга охлаждённая 3-4кг', callback_data='Сёмга охлаждённая 3-4кг'))
            markup.add(types.InlineKeyboardButton(text='Форель охлаждённая', callback_data='Форель охлаждённая'))
            markup.add(types.InlineKeyboardButton(text='Дорадо охлаждённая 400-600г', callback_data='Дорадо охлаждённая 400-600г'))
            markup.add(types.InlineKeyboardButton(text='Палтус охлаждённый', callback_data='Палтус охлаждённый'))
            markup.add(types.InlineKeyboardButton(text='Вернуться обратно', callback_data='Меню'))

            bot.edit_message_text(text=f'Категория {req}', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Меню':
            markup = types.InlineKeyboardMarkup()
            button2 = types.InlineKeyboardButton(text="БАДЫ (Омега-3)", callback_data='БАДЫ (Омега-3)')
            button3 = types.InlineKeyboardButton("Вяленая рыба", callback_data='Вяленая рыба')
            button4 = types.InlineKeyboardButton("Икра", callback_data='Икра')
            button5 = types.InlineKeyboardButton("Консервы", callback_data='Консервы')
            button6 = types.InlineKeyboardButton("Морепродукты", callback_data='Морепродукты')
            button7 = types.InlineKeyboardButton("Свежемороженая рыба", callback_data='Свежемороженая рыба')
            button9 = types.InlineKeyboardButton("Салаты", callback_data='Салаты')
            button0 = types.InlineKeyboardButton("Соусы", callback_data='Соусы')
            button10 = types.InlineKeyboardButton("Охлажденная рыба", callback_data='Охлажденная рыба')

            markup.add(button10)
            markup.add(button7)
            markup.add(button3)
            markup.add(button6)
            markup.add(button4)
            markup.add(button5, button2)
            markup.add(button9, button0)
            try:
                res = bot.edit_message_media(media=types.InputMedia(media=open('photos/M6f3ezYuvsY.jpeg', 'rb'), type="photo"),
                                             chat_id=call.message.chat.id, message_id=jk[call.message.chat.id][-1])
                jk[call.message.chat.id].append(res.id)
            except telebot.apihelper.ApiTelegramException as wef:
                pass
            bot.edit_message_text(text='Выберите нужную вам категорию:', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'add':
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute('SELECT product_id FROM cart WHERE user_id=?', [call.message.chat.id])
            wdv = [''.join(i) for i in cursor.fetchall()]
            print(wdv)
            if a[-2] not in wdv[:]:
                cursor.execute('INSERT INTO cart (user_id, product_id, price, amount) VALUES (?, ?, ?, ?)',
                       [call.message.chat.id, a[-2], prices[a[-2]], 1])
                bot.answer_callback_query(callback_query_id=call.id, text='Добавлено! \n \n Для изменения количества перейдите в корзину', show_alert=True)
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Товар уже есть в корзине! \n \n Для изменения количества перейдите в корзину',
                                          show_alert=True)

            cursor.close()
            connect.commit()
            connect.close()
        elif req == 'Заказ':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Оформить доставку', callback_data='Доставка'))
            markup.add(types.InlineKeyboardButton(text='Оформить самовывоз', callback_data='Самовывоз'))
            markup.add(types.InlineKeyboardButton(text='Отмена', callback_data='Отмена'))
            bot.edit_message_text(text=f'Выберите способ доставки товаров', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Самовывоз':
            dostavka[call.message.chat.id] = 'Нет'
            markup = types.InlineKeyboardMarkup()
            bot.edit_message_text(text=f'Мы находимся по адресу: Казань, ул. Гвардейская, 14.\n \n'
                                       f'Напишите пожалуйста комментарий,'
                                       f' во сколько вам будет удобно подъехать за заказом, а также любые другие пожелания: '
                                       f'', reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Доставка':
            dostavka[call.message.chat.id] = 'Да'
            markup = types.InlineKeyboardMarkup()
            bot.edit_message_text(text=f'Напишите пожалуйста комментарий с: \n\n1. Адресом доставки'
                                       f'\n2. Во сколько вам будет удобно забрать заказ, а также любые другие пожелания: '
                                       f'', reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        elif req == 'Подтверждаю':
            markup = types.ReplyKeyboardMarkup()
            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("""SELECT name, phone FROM users WHERE user_id=?""",[call.message.chat.id])
            rows1 = cursor.fetchall()[0]
            cursor.execute('SELECT product_id, amount FROM cart WHERE user_id=?', [call.message.chat.id])
            tovary = cursor.fetchall()
            typ = []
            for i in tovary:
                cursor.execute('SELECT type FROM products WHERE name=?', [i[0]])
                typ.append(cursor.fetchall()[-1])
            cursor.execute('SELECT product_id FROM cart WHERE user_id=?', [call.message.chat.id])
            rows = cursor.fetchall()
            rowsprices = [''.join(i) for i in rows]
            newrows = []
            for i in rowsprices:
                cursor.execute('SELECT amount FROM cart WHERE product_id=? AND user_id=?',
                               [i, call.message.chat.id])
                amount = cursor.fetchone()[0]
                newrows.append(prices[i] * amount)

            bot.send_message(chat_id=1360460983, text=f'Заказ пользователя {rows1}: \n \n {list(zip(tovary, typ))} \n \n Общая сумма заказа: {sum(newrows)} \n\n Комментарий:{komm[call.message.chat.id]}', reply_markup=markup)
            cursor.execute('DELETE FROM cart WHERE user_id=?', [call.message.chat.id])
            cursor.close()
            connect.commit()
            connect.close()
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            time.sleep(1.5)
            bot.send_message(chat_id=call.message.chat.id, text='Благодарим вас за заказ!\nОператор свяжется с вами в ближайшее время')
        elif req == 'Отмена':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        elif req == 'komm':
            bot.send_message(chat_id=call.message.chat.id, text='Хорошо, напишите новый комментарий:')
        else:
            if req.endswith('+') or req.endswith('-') or req.endswith('❌'):
                if req.endswith('-'):
                    connect = sqlite3.connect('users.db')
                    cursor = connect.cursor()

                    cursor.execute('SELECT amount FROM cart WHERE product_id=? AND user_id=?',
                                   [req[:-1], call.message.chat.id])
                    amount = cursor.fetchone()[0]
                    if amount == 1:
                        cursor.execute('DELETE FROM cart WHERE user_id=? AND product_id=?', [call.message.chat.id, req[:-1]])
                    else:
                        cursor.execute('UPDATE cart SET amount = amount - 1 WHERE user_id=? AND product_id=?', [call.message.chat.id, req[:-1]])
                    bot.answer_callback_query(callback_query_id=call.id, text='Успешно удалено! \n Нажмите кнопку "корзина" еще раз, чтобы увидеть обновленную корзину!', show_alert=True)
                    cursor.close()
                    connect.commit()
                    connect.close()
                elif req.endswith('+'):
                    connect = sqlite3.connect('users.db')
                    cursor = connect.cursor()
                    cursor.execute('UPDATE cart SET amount = amount + 1 WHERE user_id=? AND product_id=?', [call.message.chat.id, req[:-1]])
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Успешно! \n Нажмите кнопку "корзина" еще раз,'
                                                   ' чтобы увидеть обновленную корзину!',
                                              show_alert=True)
                    cursor.close()
                    connect.commit()
                    connect.close()
                elif req.endswith('❌'):
                    connect = sqlite3.connect('users.db')
                    cursor = connect.cursor()
                    cursor.execute('DELETE FROM cart WHERE user_id=? AND product_id=?', [call.message.chat.id, req[:-1]])
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Успешно! \n Нажмите кнопку "корзина" еще раз,'
                                                   ' чтобы увидеть обновленную корзину!',
                                              show_alert=True)
                    cursor.close()
                    connect.commit()
                    connect.close()
            else:
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute('SELECT type FROM products WHERE name=?', [req])
                type = cursor.fetchone()[0]
                cursor.execute('SELECT photo FROM products WHERE name=?', [req])
                photo = cursor.fetchone()[0]

                try:
                    res = bot.edit_message_media(media=types.InputMedia(media=open(f'{photo}', 'rb'), type="photo"),
                                                 chat_id=call.message.chat.id, message_id=jk[call.message.chat.id][-1])
                    jk[call.message.chat.id].append(res.id)
                except telebot.apihelper.ApiTelegramException as wef:
                    pass


                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add'))
                markup.add(types.InlineKeyboardButton(text='Назад', callback_data=f'{a[-2]}'))
                bot.edit_message_text(text=f'Вы выбрали: {req}\n \nЕго цена: {prices[req]}р/{type}',
                                      reply_markup=markup, chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
                cursor.close()
                connect.commit()
                connect.close()

    except Error and KeyError as e:
        bot.answer_callback_query(callback_query_id=call.id,
                                  text='Товар уже есть в корзине! \n Нажмите кнопку "корзина" еще раз, чтобы увидеть обновленную корзину!',
                                  show_alert=True)
    except telebot.apihelper.ApiTelegramException as qqwev:
        bot.answer_callback_query(callback_query_id=call.id,
                                  text='Ошибка! \n Нажмите кнопку "Меню" еще раз, чтобы увидеть меню!',
                                  show_alert=True)



while True:
    bot.polling(non_stop=True, interval=0)
