
from telegram import ParseMode
import urllib.request as urllib2

from config import GREETING_TEXT, INFO_TEXT, MEDIA_LINK, SUPPORT
from keyboards import first_keyboard, second_keyboard, choose_website, no_keyboard
from db import (db, get_or_create_user, add_link, how_many_links, 
                guest_quanity, get_user_rate, get_date_from_sql, add_ip_adress)


def hello_user(update, context):
    keyboard = first_keyboard()
    update.message.reply_text(
        text = GREETING_TEXT,
        reply_markup = keyboard,
        parse_mode = ParseMode.HTML)


def conditionals_info(update, context):
     keyboard = first_keyboard()
     update.message.reply_text(
        text = INFO_TEXT,
        reply_markup = keyboard,
        parse_mode = ParseMode.HTML
        )


def create_id(update, context):
    phone = update.message.contact.phone_number
    user = get_or_create_user(update.effective_user, phone)
    keyboard = second_keyboard()
    update.message.reply_text(
        text = f"Ок, запомнил\nТвой ID: <b>{user['user_id']}</b>, к нему будут привязаны все полученные ссылки\nТеперь ты можешь получить ссылку и начать рекламировать",
        reply_markup = keyboard,
        parse_mode = ParseMode.HTML)


def choose_adv(update, context):
    keyboard = choose_website()
    update.message.reply_text(
        text = "Выбери сайт для получения ссылки:",
        reply_markup = keyboard)


def send_utm_link(update, context):
    query = update.callback_query
    query.answer()
    choosen_website = update.callback_query.data
    user_id = update.effective_user.id
    link_id = how_many_links(user_id)
    short_link = link_shorter(choosen_website, user_id, link_id)
    add_link(user_id, short_link, choosen_website)
    query.edit_message_text(text = f'Твоя персональная ссылка: {short_link}\n\nРекламные материалы:{MEDIA_LINK}\n\nПартнер может использовать свои материалы, если они будут эффективней.\nПри возникновении вопросов обращаться: {SUPPORT}')


def link_shorter(choosen_website, user_id, link_id):
    long_link = f'https://{choosen_website}/?utm_source={user_id}&utm_medium={link_id}'
    fetcher = urllib2.urlopen(
         'https://clck.ru/--?url='+ long_link)
    short_link = fetcher.read().decode('utf-8')
    return short_link


def profile_info(update, context):
    link_quanity = how_many_links(update.effective_user.id)
    user = get_or_create_user(update.effective_user)
    guest = guest_quanity(update.effective_user.id)
    personal_rate = get_user_rate(update.effective_user.id)
    total_fee = guest * personal_rate
    # <b>Получено ссылок:</b> {link_quanity}\n
    info = f"<b>id:</b> {user['user_id']}\n<b>Имя:</b> {user['user_name']}\n<b>Номер телефона:</b> {user['phone']}\n<b>Всего переходов:</b> {guest}<b>\nСтавка за пользователя:</b> {personal_rate} руб.\nК выплате: {total_fee} руб.\n\nЕсли счетчик не увеличивается, запустите команду /update"
    update.message.reply_text(
        text= info,
        parse_mode=ParseMode.HTML
    )


def get_money(update, context):
    update.message.reply_text(
        text= f'Вывод средств для пользователя <b>{update.effective_user.username}</b> заблокирован!\nВывод средств доступен после <b>09.02.2022</b>\n\nЕсли партнер набрал боле 10-ти переходов, то может запросить тестовую выплату. Для этого нужно отправить публикацию, где упоминается полученная ссылка, в поддержку @tylpanov77, после чего оператор произведет выплату по вашим реквизитам',
        parse_mode=ParseMode.HTML
    )


def update_database(update, context):
    result = get_date_from_sql()
    for i in result:
        ip = i['ip_address']
        utm_source = i['utm_source']
        if len(utm_source) != 10:
            continue
        user_id = int(utm_source)
        print(len(utm_source))
        add_ip_adress(user_id, ip)
    update.message.reply_text(
        text= 'Даннные посещений по ссылке обновлены, перейдите в раздел <b>«Профиль»</b>, для проверки',
        parse_mode=ParseMode.HTML
    )


def get_number_text(update, text):
    update.message.reply_text(
        text= 'Напиши свой номер в ответном сообщении',
        reply_markup = no_keyboard(),
        parse_mode=ParseMode.HTML)



def save_number(update, context):
    number = update.message.text
    user = get_or_create_user(update.effective_user, phone=number)
    keyboard = second_keyboard()
    update.message.reply_text(
        text= f"Хорошо, запомнил\nТвой ID: <b>{user['user_id']}</b>, к нему будут привязаны все полученные ссылки\nТеперь ты можешь получить ссылку и начать рекламировать",
        parse_mode=ParseMode.HTML,
        reply_markup = keyboard)


def get_error(update, context):
     update.message.reply_text(
        text= f"Прости я не смог распознать этот текст, если нужно отправить <b>номер для регистрации</b>, попробуй написать его в другом формате",
        parse_mode=ParseMode.HTML)