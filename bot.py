import telebot

from history import save_history
from keyBoard import keyboard_markup
from CookRequest import CookRequest
from for_bd import dish_for_one, all_dish_for_one, recipes
from calculation import calculation
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


def processing_message(request_json):

    message = request_json['message']
    chat_id = message['chat']['id']
    if chat_id not in cook_requests:

        cook_requests[chat_id] = CookRequest(chat_id)
    message_text = message['text']
    if message.get('entities') and message_text == '/start':
        # начало работы боты, получаем количество людей

        bot.send_message(chat_id=chat_id, text='выберите или введите сколько будет порций',
                         reply_markup=keyboard_markup(range(1, 31), digit=True))
    elif message.get('entities') and message_text == '/recipe':
        # получить рецепт по указаному блюду  cook_request.dish
        cook_request = cook_requests.get(chat_id)
        if cook_request.dish:
            portion = recipes[cook_request.dish][0]
            recipe = recipes[cook_request.dish][1]
            bot.send_message(chat_id=chat_id, text=f'Одна порция - {portion}\nРецепт - {recipe}\n'
                                                    'чтобы начать сначала нажмите /start')
        else:
            bot.send_message(chat_id=chat_id, text='Блюдо еще не выбрано,чтобы начать сначала нажмите /start')
    elif message_text.isdigit():

        # если ввели число - сохраняем как количество порций и делаем клавиатру из типов блюд
        cook_request = cook_requests.get(chat_id)
        cook_request.count_people = int(message_text)
        types_dish = dish_for_one.keys()
        bot.send_message(chat_id=chat_id,
                         text=f'порций - {cook_request.count_people}\n'
                              'выберите тип блюда\n чтобы начать сначала нажмите /start',
                         reply_markup=keyboard_markup(types_dish))
    else:

        bot.send_message(chat_id=chat_id, text=f'не корректное сообщение, для начала работы нажмите /start ')


def processing_callback_query(request_json):

    dish = request_json['callback_query']['data']
    chat_id = request_json['callback_query']['message']['chat']['id']
    cook_request = cook_requests.get(chat_id)
    if dish.isdigit():
        # если ввели число - сохраняем как количество порций и делаем клавиатру из типов блюд
        cook_request = cook_requests.get(chat_id)
        cook_request.count_people = int(dish)
        bot.send_message(chat_id=chat_id, text=f'порций - {cook_request.count_people}\nвыберите блюдо',
                         reply_markup=keyboard_markup(dish_for_one.keys()))

    elif dish in dish_for_one:
        # если прислали тип блюда отправляем клавиатуру с блюдами
        cook_request.typy_dish = dish
        if dish_for_one.get(dish, []):
            bot.send_message(chat_id=chat_id, text=f'порций - {cook_request.count_people},\n'
                                                   f'тип блюда - {cook_request.typy_dish}\n'
                                                   'выберите блюдо',
                             reply_markup=keyboard_markup(dish_for_one.get(dish, [])))
        else:
            bot.send_message(chat_id=chat_id, text=f'{dish} - нет данных в базе\n '
                                                   'для начала работы нажмите /start')
    elif dish in all_dish_for_one:
        # если прислали нужное блюдо, отправляем расчет ингридиентов по порциям.
        if all_dish_for_one.get(dish):
            cook_request.dish = dish
            calculat = calculation(dish, cook_request.count_people)
            answer = (f'порций - {cook_request.count_people},\n'
                      f'блюдо - {cook_request.dish}\n'
                      f'{calculat}\n'
                      f'Получить рецепт {cook_request.dish} нажмите /recipe\n'
                      'Для начала работы нажмите /start')
            bot.send_message(chat_id=chat_id, text=answer)
            save_history(cook_request)  # сохраняем результат
        else:
            bot.send_message(chat_id=chat_id,
                             text=f'{dish} - нет данных по этому блюду\n для начала работы нажмите /start')


# храним объекты CookRequest
cook_requests = {}
