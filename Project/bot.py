# -*- coding:utf-8-*-

import telebot
from telebot import types
from string import Template
import urllib.parse as up
import psycopg2
import time
import datetime
import gspread
import validate_email
import os

token=os.environ.get('TOKEN')
bot = telebot.TeleBot(str(token))

up.uses_netloc.append("postgres")
key = os.environ.get('password')
db = psycopg2.connect(f"dbname='rahycxvn' user='rahycxvn' host='hattie.db.elephantsql.com' password={key}")
cursor = db.cursor()
group_id = -your_group_id_in_telegram
user_data = {}

class User:
    def __init__(self, parentsname):
        self.parentsname = parentsname
        self.childname = ''
        self.birthday = ''
        self.mail = ''
        self.mobile = ''
        self.direction = ''
        self.skill = ''
        self.shiftatschool = ''
        self.category = ''
        self.description = ''

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('О нас 🪐')
    itembtn2 = types.KeyboardButton('Зарегистрироваться 🚀')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Здравствуйте " + message.from_user.first_name + ", что бы вы хотели узнать?")
    bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IRiApWU-mTOpPRoVp7a0c9Lg5UYvQACAQEAAladvQoivp8OuMLmNCME', reply_markup=markup)

@bot.message_handler(regexp='О нас 🪐')
@bot.message_handler(commands=['info'])
def send_about(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Зарегистрироваться 🚀')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, "*Я - бот ДЮТТА.*\n\n*Наш сайт* https://robo74.ru/\n*Мы на telegram* https://t.me/tehkids74 \n*Мы на instagrame* https://www.instagram.com/tehkids74/ \n*Наш видеоканал* https://www.youtube.com/channel/UC3P6PnoiXT6a4g6RHQTYLSA \n*Мы на twitter* https://twitter.com/tehkids74 \n*МЫ на facebook* https://www.facebook.com/dutt74/ \n*Мы на Дзене* https://zen.yandex.ru/tehkids \n*Мы на vk* https://vk.com/tehkids74 \n*Пресс служба* media@robo74.ru \n*Наш емейл* pismadir@robo74.ru \n\n*Контакты:*\n454031, Россия,\nг. Челябинск,\nул. Черкасская, д. 1а\nул. Орджоникидзе, д. 50\n\n +7 (900) 029-50-10 *ДЮТТ*\n +7 (904) 808-60-10 *Кванториум Челябинск*\n +7 (351) 945-22-01 *Кванториум Магнитогорск*\n +7 (982) 277-46-61 *IT-Куб Южноуральск*\n +7 (922) 713-09-83 *IT-Куб Сатка*", reply_markup=markup, parse_mode= "Markdown")
    bot.send_message(message.chat.id, "Для регистрации Вы должны написать /reg или нажать на кнопку 👇")


@bot.message_handler(regexp='Зарегистрироваться 🚀')
@bot.message_handler(commands=['reg'])
def user_reg(message):
    # Проверка есть ли пользователь в БД
    user_id = message.from_user.id
    sql = f"SELECT * FROM users WHERE id = {message.from_user.id}"
    cursor.execute(sql)
    existsUser = cursor.fetchone()

    if (existsUser == None):
        markup = types.ReplyKeyboardRemove(selective=False)
        keyboard = types.InlineKeyboardMarkup()
        button_first = types.InlineKeyboardButton(text="Согласен ✅", callback_data="accept")
        keyboard.add(button_first)
        bot.send_message(message.chat.id, "Регистрация невозможна без вашего согласия на обработку ваших персональных данных", reply_markup=markup)
        bot.send_message(message.chat.id, "Согласны ли вы на обработку ваших персональных данных?", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Ваша заявка уже в процессе рассмотрения, ожидайте.")
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('Отменить заявку ❌')
        markup1.add(itembtn1)
        bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IxiApcnKCWLGm0N0uCA8phrMN844gACSwIAAladvQpiUEXQUPpxnCME', reply_markup=markup1)

@bot.callback_query_handler(func=lambda call: call.data in ["accept"])
@bot.message_handler(regexp='Пройти регистрацию заново 🪄')
@bot.message_handler(commands=['correct'])
def user_reg2(call):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(call.from_user.id, "Введите ФИО родителя", reply_markup=markup)
    bot.register_next_step_handler(msg, process_parentsname_step)
    
def process_parentsname_step(message):
    user_id = message.from_user.id
    user_data[user_id] = User(message.text)
    msg = bot.send_message(message.chat.id, "Введите ФИО обучающегося")
    bot.register_next_step_handler(msg, process_childname_step)

def process_childname_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.childname = message.text
    msg = bot.send_message(message.chat.id, "Дата рождения обучающегося (дд.мм.гггг)")
    bot.register_next_step_handler(msg, process_dateofbirth_step)

def process_dateofbirth_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.birthday = message.text

    date = message.text
    try:
        valid_date = time.strptime(date, '%d.%m.%Y')
        print(valid_date)
        msg = bot.send_message(message.chat.id, "Ваша почта")
        bot.register_next_step_handler(msg, process_mail_step)
    except ValueError:
        bot.reply_to(message, 'Неверный формат даты (дд.мм.гггг), попробуйте еще раз.')
        bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IZiApXO9J5lnSwElgcGxXHAYC5N-QAC-QADVp29CpVlbqsqKxs2IwQ')
        msg = bot.send_message(message.chat.id, "Дата рождения обучающегося (дд.мм.гггг)")
        bot.register_next_step_handler(msg, process_dateofbirth_step)

def process_mail_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.mail = message.text

    email = validate_email.validate_email(message.text)
    if email == True:
        msg = bot.send_message(message.chat.id, "Введите Ваш номер телефона")
        bot.register_next_step_handler(msg, process_mobile_step)
    else:
        bot.reply_to(message, 'Неверно указан почтовый адрес, попробуйте еще раз.')
        bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IZiApXO9J5lnSwElgcGxXHAYC5N-QAC-QADVp29CpVlbqsqKxs2IwQ')
        msg = bot.send_message(message.chat.id, "Ваша почта")
        bot.register_next_step_handler(msg, process_mail_step)

def process_mobile_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.mobile = message.text

    if len(str(message.text)) == 11 and int(message.text) == int(message.text): 
         markup_direction = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
         itembtn1 = types.KeyboardButton('Авиамоделирование (10-16 лет)')
         itembtn2 = types.KeyboardButton('Автомоделирование (10-16 лет)')
         itembtn3 = types.KeyboardButton('Программирование на базе Arduino (12-16 лет)')
         itembtn4 = types.KeyboardButton('Судомоделирование (10-16 лет)')
         itembtn5 = types.KeyboardButton('Компьютерное зрение (14-17 лет)')
         itembtn6 = types.KeyboardButton('Хайтек-цех (12-16 лет)')
         itembtn7 = types.KeyboardButton('*Baby-техник (внебюджет; 3-7 лет)')
         itembtn8 = types.KeyboardButton('*Программирование на Scratch (внебюджет; 8-12 лет)')
         itembtn9 = types.KeyboardButton('*Графический дизайн (внебюджет; 12-16 лет)')
         itembtn10 = types.KeyboardButton('*Увлекательная робототехника (внебюджет; 8-14 лет)')
         itembtn11 = types.KeyboardButton('*Разработка приложений под Android (внебюджет; 12-16 лет)')
         itembtn12 = types.KeyboardButton('*3D-моделирование (внебюджет; 11-16 лет)')
#         itembtn13 = types.KeyboardButton('Другое')
         markup_direction.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11, itembtn12) #, itembtn13

         msg = bot.send_message(message.chat.id, "Направление обучения", reply_markup=markup_direction)
         bot.register_next_step_handler(msg, process_direction_step)

    elif len(message.text) == 12:
         markup_direction = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
         itembtn1 = types.KeyboardButton('Авиамоделирование (10-16 лет)')
         itembtn2 = types.KeyboardButton('Автомоделирование (10-16 лет)')
         itembtn3 = types.KeyboardButton('Программирование на базе Arduino (12-16 лет)')
         itembtn4 = types.KeyboardButton('Судомоделирование (10-16 лет)')
         itembtn5 = types.KeyboardButton('Компьютерное зрение (14-17 лет)')
         itembtn6 = types.KeyboardButton('Хайтек-цех (12-16 лет)')
         itembtn7 = types.KeyboardButton('*Baby-техник (внебюджет; 3-7 лет)')
         itembtn8 = types.KeyboardButton('*Программирование на Scratch (внебюджет; 8-12 лет)')
         itembtn9 = types.KeyboardButton('*Графический дизайн (внебюджет; 12-16 лет)')
         itembtn10 = types.KeyboardButton('*Увлекательная робототехника (внебюджет; 8-14 лет)')
         itembtn11 = types.KeyboardButton('*Разработка приложений под Android (внебюджет; 12-16 лет)')
         itembtn12 = types.KeyboardButton('*3D-моделирование (внебюджет; 11-16 лет)')
#         itembtn13 = types.KeyboardButton('Другое')
         markup_direction.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11, itembtn12) #, itembtn13

         msg = bot.send_message(message.chat.id, "Направление обучения", reply_markup=markup_direction)
         bot.register_next_step_handler(msg, process_direction_step)
    
    else:
        bot.reply_to(message, 'Неверно указан номер телефона, попробуйте еще раз.')
        bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IZiApXO9J5lnSwElgcGxXHAYC5N-QAC-QADVp29CpVlbqsqKxs2IwQ')
        msg = bot.send_message(message.chat.id, "Введите Ваш номер телефона")
        bot.register_next_step_handler(msg, process_mobile_step)

def process_direction_step(message):
    markup_skill = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Вводный модуль')
    itembtn2 = types.KeyboardButton('Продвинутый модуль - соревновательные и проектные группы')
    markup_skill.add(itembtn1, itembtn2)

    user_id = message.from_user.id
    user = user_data[user_id]
    user.direction = message.text
    msg = bot.send_message(message.chat.id, "Уровень обучения", reply_markup=markup_skill)
    bot.register_next_step_handler(msg, process_skill_step)

def process_skill_step(message):
    markup_shiftatschool = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('1 смена')
    itembtn2 = types.KeyboardButton('2 смена')
    markup_shiftatschool.add(itembtn1, itembtn2)

    user_id = message.from_user.id
    user = user_data[user_id]
    user.skill = message.text
    msg = bot.send_message(message.chat.id, "Смена в школе", reply_markup=markup_shiftatschool)
    bot.register_next_step_handler(msg, process_shiftatschool_step)

def process_shiftatschool_step(message):
    markup_category = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Многодетная семья')
    itembtn2 = types.KeyboardButton('Ребенок-инвалид')
    itembtn3 = types.KeyboardButton('Неполная семья')
    markup_category.add(itembtn1, itembtn2, itembtn3)

    user_id = message.from_user.id
    user = user_data[user_id]
    user.shiftatschool = message.text
    msg = bot.send_message(message.chat.id, "Cоциальная категория обучающегося", reply_markup=markup_category)
    bot.register_next_step_handler(msg, process_category_step)

def process_category_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.category = message.text
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Комментарий к заявке на обучение", reply_markup=markup)
    bot.register_next_step_handler(msg, process_description_step)

#дата регистрации
today = datetime.datetime.today()
data_reg = today.strftime("%d.%m.%Y")

def process_description_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.description = message.text
    
    bot.send_message(message.chat.id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="HTML")

    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Да')
    itembtn2 = types.KeyboardButton('Нет')
    markup1.add(itembtn1, itembtn2)
    msg = bot.send_message(message.chat.id,"Ваши данные введены верно?", reply_markup=markup1)
    bot.register_next_step_handler(msg, process_final_step)

def process_final_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.agreement = message.text

    if message.text == "Да":
        sql = f"INSERT INTO users (id, first_name, last_name, telegram_user_id, user_data_reg) VALUES (%s, %s, %s, '@{message.chat.username}', '{data_reg}')"
        val = (user_id, message.from_user.first_name, message.from_user.last_name)
        cursor.execute(sql, val)

        # Регистрация заявки
        sql = f"INSERT INTO regs (id, parentsname, childname, birthday, mail, mobile, direction, skill, shiftatschool, category, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (user_id, user.parentsname, user.childname, user.birthday, user.mail, user.mobile, user.direction, user.skill, user.shiftatschool, user.category, user.description)
        cursor.execute(sql, val)
        db.commit()

        #дозапись google sheets
        CREDENTIALS_FILE = 'googlesheets/botdutttelegram-9c0cba3e1c28.json'
        gc = gspread.service_account(filename = CREDENTIALS_FILE)
        sh = gc.open_by_key('1YH1yopZtn1HsdXNwCzijYIDiLLng5sGh-hDajm7sTg0')
        worksheet = sh.sheet1
        transaction = [user_id, user.parentsname, user.childname, user.birthday, user.mail, user.mobile, user.direction, user.skill, user.shiftatschool, user.category, user.description]
        worksheet.append_row(transaction) # каждый раз при добавлении списка в таблицу, данные будут вносится на пустую строку вниз.

        bot.send_message(message.chat.id, "Вы успешно зарегистрированны!")
        bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IhiApaIZw6bpoVMF8tbOVWwtOayKwAC_gADVp29CtoEYTAu-df_IwQ')
        bot.send_message(group_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="HTML")
        
        cursor.execute(f"SELECT id FROM survey WHERE id = '{message.from_user.id}'")
        result = cursor.fetchone()
        if result is None:
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembtn1 = types.KeyboardButton('Оценить')
            itembtn2 = types.KeyboardButton('Не сейчас')
            markup1.add(itembtn1, itembtn2)
            msg = bot.send_message(message.chat.id, 'Не желаете оставить отзыв о работе бота?', reply_markup=markup1)
            bot.register_next_step_handler(msg, process_survey_step)
        else:
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembtn1 = types.KeyboardButton('Отменить заявку ❌')
            markup1.add(itembtn1)
            bot.send_message(message.chat.id, "Если хотите отменить поданную заявку, то нажмите на кнопку ниже", reply_markup=markup1)
        
    elif message.text == "Нет":
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('Пройти регистрацию заново 🪄')
        markup1.add(itembtn1)
        bot.send_message(message.chat.id, "Для того, чтобы зарегистрировать свои данные снова, напишите /correct или нажмите на кнопку 👇", reply_markup=markup1)

def getRegData(user, title, name):
    t = Template("$title <b>$name</b> \nФИО родителя: <b>$parentsname</b>\nФИО обучающегося: <b>$childname</b>\nДата рождения обучающегося: <b>$birthday</b>\nПочта: <b>$mail</b> \nНомер телефона: <b>$mobile</b> \nНаправление обучения: <b>$direction</b>\nУровень обучения: <b>$skill</b> \nСмена в школе: <b>$shiftatschool</b> \nCоциальная категория обучающегося: <b>$category</b> \nКомментарий к заявке на обучение: <b>$description</b>")
    return t.substitute({
        'title': title,
        'name' : name,
        'parentsname' : user.parentsname,
        'childname' : user.childname,
        'birthday' : user.birthday,
        'mail' : user.mail,
        'mobile' : user.mobile,
        'direction' : user.direction,
        'skill' : user.skill,
        'shiftatschool' : user.shiftatschool,
        'category' : user.category,
        'description' : user.description
    })

@bot.message_handler(regexp='Отменить заявку ❌')
@bot.message_handler(commands=['cancellation'])
def send_welcome(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Зарегистрироваться 🚀')
    markup1.add(itembtn1)

    cursor.execute(f"SELECT id FROM users WHERE id = '{message.from_user.id}'")
    result = cursor.fetchone()
    if result is None:
        bot.send_message(message.chat.id,'У нас и так нет Вашей заявки! Напишите /reg или нажмите на кнопку 👇, чтобы сделать заявку', reply_markup=markup1)
        bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IZiApXO9J5lnSwElgcGxXHAYC5N-QAC-QADVp29CpVlbqsqKxs2IwQ')
    else:
        result_scnd = []
        cursor.execute(f"SELECT id, parentsname, childname, birthday, mail, mobile, direction, skill, shiftatschool, category, description  FROM regs WHERE id = '{message.from_user.id}'")
        result1 = cursor.fetchall()
        for row in result1:
            for x in row:
                result_scnd.append(str(x))     

        #удаление из google sheet
        cursor.execute("SELECT id FROM users")
        users_list = []
        massive_big = cursor.fetchall()
        for row in massive_big:
            for x in row:
                users_list.append(str(x))
        print(users_list)
        print(result_scnd)
        CREDENTIALS_FILE = 'googlesheets/botdutttelegram-9c0cba3e1c28.json'
        gc = gspread.service_account(filename = CREDENTIALS_FILE)
        sh = gc.open_by_key('1YH1yopZtn1HsdXNwCzijYIDiLLng5sGh-hDajm7sTg0')
        worksheet = sh.sheet1
        worksheet.delete_rows(int(users_list.index(f'{message.from_user.id}'))+2)

        #удаление из postgresql
        cursor.execute(f"DELETE FROM users WHERE id = '{message.from_user.id}'")
        cursor.execute(f"DELETE FROM regs WHERE id = '{message.from_user.id}'")
        db.commit()
     
        bot.send_message(message.chat.id, 'Ваша заявка удалена, напишите /reg или нажмите на кнопку 👇 для повторной регистрации', reply_markup=markup1)
        bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IpiApb0iuxW6WxtRdM_Hu1z3IoIDwACSQIAAladvQoqlwydCFMhDiME')
        
        bot.send_message(group_id, f'Заявка пользователя <b>"{result_scnd[2]}"</b> (@{message.chat.username}) с идентификатором <b>{message.from_user.id}</b> отменена', parse_mode="HTML")
        
def process_survey_step(message):
    if message.text == 'Оценить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn1 = types.KeyboardButton('⭐️')
        itembtn2 = types.KeyboardButton('⭐️⭐️')
        itembtn3 = types.KeyboardButton('⭐️⭐️⭐️')
        itembtn4 = types.KeyboardButton('⭐️⭐️⭐️⭐️')
        itembtn5 = types.KeyboardButton('⭐️⭐️⭐️⭐️⭐️')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
        msg = bot.send_message(message.chat.id, 'Поставьте чат-боту оценку от 1 до 5', reply_markup=markup)
        bot.register_next_step_handler(msg, process_survey1_step)
    elif message.text == 'Не сейчас':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('Отменить заявку ❌')
        markup1.add(itembtn1)
        bot.send_message(message.chat.id, "Если хотите отменить поданную заявку, то нажмите на кнопку ниже", reply_markup=markup1)
    
def process_survey1_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    if message.text == '⭐️':
        user.survey_grade = 1
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Оставьте комментарий к работе чат-бота', reply_markup=markup)
        bot.register_next_step_handler(msg, process_survey3_step)
    elif message.text == '⭐️⭐️':
        user.survey_grade = 2
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Оставьте комментарий к работе чат-бота', reply_markup=markup)
        bot.register_next_step_handler(msg, process_survey3_step)
    elif message.text == '⭐️⭐️⭐️':
        user.survey_grade = 3
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Оставьте комментарий к работе чат-бота', reply_markup=markup)
        bot.register_next_step_handler(msg, process_survey3_step)
    elif message.text == '⭐️⭐️⭐️⭐️':
        user.survey_grade = 4
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Оставьте комментарий к работе чат-бота', reply_markup=markup)
        bot.register_next_step_handler(msg, process_survey3_step)
    elif message.text == '⭐️⭐️⭐️⭐️⭐️':
        user.survey_grade = 5
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Оставьте комментарий к работе чат-бота', reply_markup=markup)
        bot.register_next_step_handler(msg, process_survey3_step)
    else:
        bot.reply_to(message, 'Неверно указана оценка, попробуйте еще раз.')
        bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAED3IZiApXO9J5lnSwElgcGxXHAYC5N-QAC-QADVp29CpVlbqsqKxs2IwQ')
        msg = bot.send_message(message.chat.id, "Поставьте чат-боту оценку от 1 до 5 (воспользуйтесь предложенными кнопками)")
        bot.register_next_step_handler(msg, process_survey1_step)

def process_survey3_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.survey_comment = message.text
    bot.send_message(message.chat.id, 'Спасибо за отзыв!')
    sql = f"INSERT INTO survey (id, grade, comment) VALUES ('{message.from_user.id}', %s, %s)"
    val = (user.survey_grade, user.survey_comment)
    cursor.execute(sql, val)
    db.commit()
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('Отменить заявку ❌')
    markup1.add(itembtn1)
    bot.send_message(message.chat.id, "Если хотите отменить поданную заявку, то нажмите на кнопку ниже", reply_markup=markup1)
        
        
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
