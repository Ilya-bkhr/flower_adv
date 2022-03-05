import logging
import re
import locale


from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackQueryHandler, ConversationHandler)

import settings
from handlers import (hello_user, conditionals_info, create_id, choose_adv,
                      send_utm_link, profile_info, get_money, update_database, 
                      get_number_text, save_number, get_error)


logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    locale.setlocale(category=locale.LC_ALL, locale='ru_RU.utf-8')
    my_bot = Updater(settings.API_KEY, use_context=True)
    dp = my_bot.dispatcher
    
 
    
    dp.add_handler(CommandHandler('start', hello_user))
    dp.add_handler(CommandHandler('info', conditionals_info))
    dp.add_handler(CommandHandler('update', update_database))
    dp.add_handler(MessageHandler(Filters.contact, create_id))
    dp.add_handler(MessageHandler(Filters.regex(re.compile(r'выбрать рекламодателя', re.IGNORECASE)), choose_adv))
    dp.add_handler(MessageHandler(Filters.regex(re.compile(r'профиль', re.IGNORECASE)), profile_info))
    dp.add_handler(MessageHandler(Filters.regex(re.compile(r'Вывод средств', re.IGNORECASE)), get_money))
    dp.add_handler(MessageHandler(Filters.regex(re.compile(r'Отправить номер текстом', re.IGNORECASE)), get_number_text))
    dp.add_handler(MessageHandler(Filters.regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$') , save_number))
    dp.add_handler(MessageHandler(Filters.text, get_error))
    dp.add_handler(CallbackQueryHandler(send_utm_link, pattern = 'xn----8sbem5anmml8ghw.xn--p1ai|xn----7sbbh3bdjglf1ae5jk2a.xn--p1ai|tylpanov77.ru|tylpanov.ru'))
    logging.info('Bot have started')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == '__main__':
    main()


