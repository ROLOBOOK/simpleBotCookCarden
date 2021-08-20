import telebot


def keyboard_markup(dishes, digit=False):
    if digit:
        # количесвво кнопок в ряду для цифр (кол-во порций)
        row_width = 8
    else:
        row_width = 2
    # создаем клавиатуру, кнопки, добавляем кнопки к клавиатуре
    markup = telebot.types.InlineKeyboardMarkup(row_width=row_width)
    buttons = [telebot.types.InlineKeyboardButton(text=dish, callback_data=dish) for dish in dishes]
    markup.add(*buttons)
    return markup


if __name__ == '__main__':
    pass