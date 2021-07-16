from aiogram import types
from misc import dp, bot
import sqlite3
from .sqlit import info_members, reg_one_channel, reg_channels,del_one_channel,cheak_traf,obnovatrafika,info_chyornaya_vdova,info_good_film1,info_films_online_everyday,reg_partners_schet,cheach_all_par,info,cheak_zakup,reg_utm
from .callbak_data import obnovlenie
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 678623761 #Бекир
ADMIN_ID_4 = 941730379 #Джейсон

MODERN_ID_5 = 807911349 #Байзат


PARTNERS1 = 430142587 #ДЕНИС
PARTNERS2 = 984418306 #Игорь
#ФАИН PARTNERS3 = 519072406
PARTNERS4 = 921818240 #Юля
PARTNERS5 = 1013231983 # АЛЕКС

ADMIN_ID =[ADMIN_ID_1]

class reg(StatesGroup):
    name = State()
    fname = State()

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()


class del_user(StatesGroup):
    del_name = State()
    del_fname = State()

class reg_trafik(StatesGroup):
    traf1 = State()
    traf2 = State()

class partners12(StatesGroup):
    step1 = State()
    step2 = State()

class utm(StatesGroup):
    step1 = State()
    step2 = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_b = types.InlineKeyboardButton(text='NEW канал', callback_data='new_channel')# Добавляет 1 канал
        bat_c = types.InlineKeyboardButton(text='NEW Список', callback_data='new_channels') # Добавляет список каналов через пробел
        bat_d = types.InlineKeyboardButton(text='Удалить канал', callback_data='delite_channel')# Удаляет канал из списка
        bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_j = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
        bat_setin = types.InlineKeyboardButton(text='Настройка трафика', callback_data='settings')
        den_but = types.InlineKeyboardButton(text='Ден', callback_data='chyornaya_vdova')
        alex_but = types.InlineKeyboardButton(text='Алекс', callback_data='good_film1')
        yulya_but = types.InlineKeyboardButton(text='Юля', callback_data='films_online_everyday')
        sbros_but = types.InlineKeyboardButton(text='Сбросить статистику', callback_data='sbros')
        reg_new_partners = types.InlineKeyboardButton(text='РЕГИСТРАЦИЯ НОВОГО ПАРТНЕРА',callback_data='reg_new_partners')
        vienw_partners = types.InlineKeyboardButton(text='СТАТИСТИКА ВСЕХ ПАРТНЕРОВ', callback_data='vienw_partners')

        viye_zakup = types.InlineKeyboardButton(text='РЕФЕРАЛКИ', callback_data='viye_zakup')
        reg_zakup = types.InlineKeyboardButton(text='Регистрация метки', callback_data='reg_zakup')

        markup.add(bat_a, bat_b, bat_c, bat_d,bat_e,bat_j)
        markup.add(den_but, alex_but, yulya_but)  # Инфо о партнерах
        markup.add(bat_setin)
        markup.add(reg_new_partners)
        markup.add(vienw_partners)
        markup.add(viye_zakup)
        markup.add(reg_zakup)
        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)

    if id == MODERN_ID_5: #Админка для модераторов
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        markup.add(bat_a)
        await bot.send_message(message.chat.id, 'Выполнен вход в админ панель', reply_markup=markup)



# ПРОСМОТР ЭФФЕКТИВНОСТИ ЗАКУПОВ
@dp.callback_query_handler(text='viye_zakup')
async def viye_zakup(call: types.callback_query):
    answer = cheak_zakup()
    print(answer)
    for x in answer:
        await bot.send_message(chat_id=call.message.chat.id,text=f'<b>Метка: {x[0]}</b>\n'
                                                                 f'Всего пользователей:{x[1]}\n'
                                                                 f'Конечных пользователей: {x[2]}',parse_mode='html')

# СОЗДАНИЕ НОВОЙ МЕТКИ ДЛЯ ОТСЛЕЖИВАНИЯ
@dp.callback_query_handler(text='reg_zakup')
async def reg_zakup(call: types.callback_query, state: FSMContext):
    await bot.send_message(chat_id=call.message.chat.id,text='Отправьте новую метку (5 значную). Не используй только цифры!п')
    await utm.step1.set()

@dp.message_handler(state=utm.step1, content_types='text')
async def get_utm_name(message: types.Message, state: FSMContext):
    if len(message.text) == 5:
        try:
            reg_utm(message.text)
            await bot.send_message(chat_id=message.chat.id, text='Успешно')
        except:
            await bot.send_message(chat_id=message.chat.id, text='Неудача')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Отменено. Метка должна состоять из 5 символов')
    await state.finish()



#ПРОСМОТР ВСЕХ ПАРТНЕРОВ
@dp.callback_query_handler(text='vienw_partners')  #ПРОСМОТР ВСЕХ ПАРТНЕРОВ
async def vienw_partners(call: types.callback_query):
    q = cheach_all_par()
    if q != []:  # Если зарегистрирован в базе для просмотра
        for i in q:
            s = (info(i[0]))
            await bot.send_message(call.message.chat.id, f'Счетчик @{i[0]}: {s}')

#МЕНЮ НОВЫХ ПАРТНЕРОВ
@dp.callback_query_handler(text='reg_new_partners')  #МЕНЮ
async def check_all_partners(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(chat_id=call.message.chat.id,text = 'Перешлите сообщение от партнера',reply_markup=markup)
    await partners12.step1.set()


@dp.message_handler(state=partners12.step1, content_types='text')
async def get_id_partners(message: types.Message, state: FSMContext):
    try:
        id = message.forward_from.id
        await state.update_data(id_partners = id)
        await bot.send_message(chat_id=message.chat.id, text='ID получен! \n'
                                                             'Введите имя канала слитно без пробелов, через @')
        await partners12.step2.set()

    except:
        await bot.send_message(chat_id=message.chat.id, text='У партнера скрытый аккаунт!\n'
                                                             'Повторите попытку')


@dp.message_handler(state=partners12.step2, content_types='text')
async def get_channel_partners(message: types.Message, state: FSMContext):
    chennel = message.text
    if chennel[0] == '@':
        await bot.send_message(chat_id=message.chat.id, text='Канал зарегистрирован')
        text_id = (await state.get_data())['id_partners']
        reg_partners_schet(channel=chennel[1:],id = text_id)
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id, text='Повторите попытку')





@dp.message_handler(commands=['traf'])
async def cheak_traaf(message: types.Message):

    if message.chat.id == PARTNERS1 or message.chat.id == PARTNERS2: #ДЕНИС
        a = info_chyornaya_vdova()  # Вызов функции из файла sqlit
        await bot.send_message(message.chat.id, f'Счетчик подписок: {a}\n'
                                                     f'Канал : @chyornaya_vdova')

    if message.chat.id == PARTNERS5: #АЛЕКС
        a = info_good_film1()  # Вызов функции из файла sqlit
        await bot.send_message(message.chat.id, f'Счетчик подписок: {a}\n'
                                                     f'Канал : @good_film1')

    if message.chat.id == PARTNERS4: #ЮЛЯ
        a = info_films_online_everyday()  # Вызов функции из файла sqlit
        await bot.send_message(message.chat.id, f'Счетчик подписок: {a}\n'
                                                     f'Канал : @films_online_everyday')

#Трафик партнеров
@dp.callback_query_handler(text='chyornaya_vdova')  # ТРАФИК У ДЕНИСА
async def check_chyornaya_vdova(call: types.callback_query):
    a = info_chyornaya_vdova() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Счетчик подписок: {a}\n'
                                                 f'Канал : @chyornaya_vdova')

@dp.callback_query_handler(text='good_film1')  # ТРАФИК У АЛЕКСА
async def good_film1(call: types.callback_query):
    a = info_good_film1() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Счетчик подписок: {a}\n'
                                                 f'Канал : @good_film1')

@dp.callback_query_handler(text='films_online_everyday')  # ТРАФИК У ЮЛИ
async def films_online_everyday(call: types.callback_query):
    a = info_films_online_everyday() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Счетчик подписок: {a}\n'
                                                 f'Канал : @films_online_everyday')





# НАСТРОЙКА ТРАФИКА
@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ КАНАЛЫ⚙️', callback_data='change_trafik')
    markup_traf.add(bat_a)
    list = cheak_traf()
    await bot.send_message(call.message.chat.id, text=f'Список активный каналов на данный момент:\n\n'
                                                      f'1. @{list[0]}\n'
                                                      f'2. @{list[1]}\n'
                                                      f'3. @{list[2]}\n\n'
                                                      f'<b>Внимание! Первый по счету канал , должен быть обязательно с кино-тематикой</b>\n'
                                                      f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf)


@dp.callback_query_handler(text='change_trafik') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите новый список каналов\n<b>ПЕРВЫЙ КАНАЛ ДОЛЖЕН БЫТЬ ОБЯЗАТЕЛЬНО С КИНО-ТЕМАТИКОЙ!</b>\n\n'
                                                      'Список каналов вводи в строчку, пример:\n'
                                                      '@channel1 @channel2 @channel3',parse_mode='html',reply_markup=markup)
    await reg_trafik.traf1.set()


@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 3 and mas[0][0] == '@' and mas[1][0] == '@' and mas[2][0] == '@'):
        # Список новых каналов
        channel1 = mas[0][1:]
        channel2 = mas[1][1:]
        channel3 = mas[2][1:]

        obnovatrafika(channel1,channel2,channel3) # Внесение новых каналов в базу данных
        obnovlenie()
        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. ТЕбе необходимо снова зайти в админ панель и выбрать нужный пункт.'
                                                            'Сообщение со списком каналом мне отсылать сейчас бессмыслено - я тебя буду игнорить, поэтому делай по новой все')
        await state.finish()



@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    a = open('server.db','rb')
    await bot.send_document(chat_id=call.message.chat.id, document=a)


############################  DELITE CHANNEL  ###################################
@dp.callback_query_handler(text='delite_channel')
async def del_channel(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название канала для удаления в формате\n'
                                                 '@name_channel')
    await del_user.del_name.set()


@dp.message_handler(state=del_user.del_name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        await state.finish()
        del_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Удаление завершено')


############################  REG ONE CHANNEL  ###################################
@dp.callback_query_handler(text='new_channel')  # АДМИН КНОПКА Добавления нового трафика
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название нового канала в формате\n'
                                                 '@name_channel')
    await reg.name.set()


@dp.message_handler(state=reg.name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        reg_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Регистрация успешна')
        await state.finish()


################################    REG MANY CHANNELS    ###########################

@dp.callback_query_handler(text='new_channels')  # АДМИН КНОПКА Добавления новые телеграмм каналы
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь список каналов в формате\n'
                                                 '@name1 @name2 @name3 ')
    await reg.fname.set()


@dp.message_handler(state=reg.fname, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Каналы зарегистрированы')
    reg_channels(message.text)
    await state.finish()

#####################################################################################


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    a = info_members() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')


########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()


@dp.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()



@dp.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot\n\n'
                                                     'Пока можно добавить только одну кнопку')
    await st_reg.step_regbutton.set()


@dp.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr2 = message.text.split('-')

    k = -1  # Убираем пробелы из кнопок
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                arr2[k] = (i[1:-1])
            else:
                arr2[k] = (i[1:])

        else:
            if i[-1] == ' ':

                arr2[0] = (i[:-1])
            else:
                pass

    # arr2 - Массив с данными


    try:
        murkap = types.InlineKeyboardMarkup() #Клавиатура с кнопками
        bat = types.InlineKeyboardButton(text= arr2[0], url=arr2[1])
        murkap.add(bat)

        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but =arr2[0]) # Обновление Сета
        await state.update_data(url_but=arr2[1])  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_but = data['text_but']
        url_but = data['url_but']
        bat = types.InlineKeyboardButton(text=text_but, url=url_but)
        murkap.add(bat)
    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await mess.copy_to(i[0],reply_markup=murkap)
            good += 1
        except:
            bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################