from telebot import types
from utils.currency_api import convert_currency
from utils.validator import is_valid_amount, is_valid_currency_pair

amount = 0

def start_handler(bot, message):
    bot.send_message(message.chat.id, 'Привіт! Введи суму, яку хочеш конвертувати:')
    bot.register_next_step_handler(message, get_amount, bot)

def get_amount(message, bot):
    global amount
    if not is_valid_amount(message.text):
        bot.send_message(message.chat.id, '❌ Введи число більше 0:')
        bot.register_next_step_handler(message, get_amount, bot)
        return

    amount = float(message.text.strip())

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('USD ➡️ EUR', callback_data='USD/EUR'),
        types.InlineKeyboardButton('EUR ➡️ USD', callback_data='EUR/USD'),
        types.InlineKeyboardButton('USD ➡️ GBP', callback_data='USD/GBP'),
        types.InlineKeyboardButton('Інша пара', callback_data='custom')
    )
    bot.send_message(message.chat.id, 'Оберіть валютну пару або введіть свою:', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_conversion(call):
        if call.data == 'custom':
            bot.send_message(call.message.chat.id, 'Введи валютну пару у форматі XXX/YYY:')
            bot.register_next_step_handler(call.message, custom_currency, bot)
        else:
            from_currency, to_currency = call.data.split('/')
            try:
                result = convert_currency(amount, from_currency, to_currency)
                bot.send_message(call.message.chat.id, f'💱 Результат: {round(result, 2)} {to_currency}')
            except Exception as e:
                bot.send_message(call.message.chat.id, f'Помилка конвертації: {str(e)}')

            bot.send_message(call.message.chat.id, 'Введи нову суму:')
            bot.register_next_step_handler(call.message, get_amount, bot)

def custom_currency(message, bot):
    if not is_valid_currency_pair(message.text):
        bot.send_message(message.chat.id, 'Неправильний формат. Спробуй знову у форматі XXX/YYY.')
        bot.register_next_step_handler(message, custom_currency, bot)
        return
    try:
        from_currency, to_currency = message.text.upper().split('/')
        result = convert_currency(amount, from_currency, to_currency)
        bot.send_message(message.chat.id, f'Результат: {round(result, 2)} {to_currency}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Помилка: {str(e)}. Спробуй знову.')
        bot.register_next_step_handler(message, custom_currency, bot)
        return

    bot.send_message(message.chat.id, 'Введи нову суму:')
    bot.register_next_step_handler(message, get_amount, bot)
