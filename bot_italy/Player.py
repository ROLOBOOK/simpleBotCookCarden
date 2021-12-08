from random import choice, choices
from config import PATH_WORDS
import re


class Player:
    def __init__(self, id, bot, words):
        self.words = words
        self.bot = bot
        self.id = id
        self.count_stady_word = 6
        self.count_mistake = 0
        self.stady_words = choices(list(self.words.keys()),
                                   k=self.count_stady_word)
        self.new_word = ''
        self.flag_add_word = False
        self.help = '\nКоманды:  /help /study /new'

    def send_msg(self, msg):
        if msg:
            self.bot.send_message(chat_id=self.id, text=f'{msg}{self.help}')

    def get_new_stady_words(self):
        self.stady_words = choices(list(self.words.keys()),
                                   k=self.count_stady_word)
        self.send_new_stady_words()

    def get_new_stady_word(self):
        self.count_mistake = 0
        if not self.stady_words:
            self.get_new_stady_words()
        self.new_word = self.stady_words.pop()

    def send_new_stady_word(self):
        if len(self.new_word) == 0:
            self.get_new_stady_word()
        self.send_msg(f'\nПереведи слово - {self.new_word}')

    def send_new_stady_words(self):
        self.send_msg(f'\n'.join(
                [f'{word} - {self.words[word]}' for word in self.stady_words]))

    def add_word(self, message):
        self.flag_add_word = False
        if re.findall(r'^\b[a-z]+\b\s+\b[а-я]+\b', message.lower()):
            a, b = message.split()
            if a not in self.words and b not in self.words:
                self.words[a], self.words[b] = b,  a
                self.send_msg(f'{message} добавлено для изучения')
            else:
                self.send_msg(f'{message} уже есть в списке для изучения')
        else:
            self.send_msg(f'{message} неразпознано.')

    def save_words(self):
        with open(PATH_WORDS, 'w') as f:
            json.dump(self.words, f, indent=2, ensure_ascii=False,
                      encoding='utf8')
