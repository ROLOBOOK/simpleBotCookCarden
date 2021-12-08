import telebot
from config import TOKEN_ITALY, PATH_WORDS, MASTER_CHAT_ID
import json

from .Player import Player


bot = telebot.TeleBot(TOKEN_ITALY)


def get_words():
    with open(PATH_WORDS, encoding='utf8') as f:
        d = json.load(f)
    return d


words = get_words()

players = {}


def command_start(player):
    player.send_new_stady_words()


def command_new_stady_words(player):
    player.get_new_stady_words()


def command_add_words(player):
    if player.id in MASTER_CHAT_ID:
        player.flag_add_word = True
        player.send_msg("Введите итальянское слово и русский перевод")
    else:
        bot.send_message(chat_id=player.id,
                         text='Функция в разработке')


def command_start_study(player):
    player.send_new_stady_word()


def command_list_commands(player):
    bot.send_message(chat_id=player.id,
                     text='''
/start: вывести список слов для изучения,
/new: обновить список слов для изучения,
/add: добавить слово для изучения,
/help: список команд,
/study: написать перевод слова
''')


COMMANDS = {
    '/start': command_start,
    '/new': command_new_stady_words,
    '/add': command_add_words,
    '/help': command_list_commands,
    '/study': command_start_study,
}


def processing_message(request_json):
    message = request_json['message']
    chat_id = message['chat']['id']
    message_text = message['text'].lower()

    if chat_id not in players:
        # создаем игрока
        players[chat_id] = Player(chat_id, bot, words)

    player = players[chat_id]

    if message.get('entities'):
        # если получили команду
        if message_text in COMMANDS:
            COMMANDS[message_text](player)
        else:
            player.send_msg(f'Ошибка в команде {message_text}!')

    elif player.flag_add_word:
        # добавляем слова в словарь
        player.add_word(message_text)

    elif message_text in words:
        # если слово правильное, отправляем новое слово
        player.get_new_stady_word()
        player.send_new_stady_word()
    else:
        # пытаемся отправить подсказку
        player.count_mistake += 1
        help = words.get(player.new_word)
        if player.count_mistake == 1:
            player.send_msg(f'Подсказка: - {help[:1]}')
        elif player.count_mistake == 2:
            player.send_msg(f'Подсказка: - {help[:3]}')
        elif player.count_mistake > 2:
            player.send_msg(f'Ответ - {help}')
            player.get_new_stady_word()
            player.send_new_stady_word()
        else:
            player.send_msg(f'Чевой это?!')


