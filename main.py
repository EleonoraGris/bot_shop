from aiogram import *
from aiogram.dispatcher.filters import Text
from sqlite3 import *

bot = Bot(token='6504900113:AAH2LJeQko932Z7aswK6g4Oet1eG3XTdK5E')
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def hello(mes):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Меню', 'Корзина', 'Помощь']
    key.add(*buttons)
    await bot.send_message(mes.from_user.id, 'Привет!!!', reply_markup=key)
    await bot.send_sticker(mes.from_user.id, sticker='CAACAgIAAxkBAAEKqXdlQ2HQenEMEK2o2gGjQTLVWRz6XwACzQ4AAg8aqEi8AuOsRnFu3DME')
 
@dp.message_handler(Text(equals='Помощь'))
async def help(mes):
    await bot.send_message(mes.from_user.id, 'ну и чем я тебе помогу')

@dp.message_handler(Text(equals='Меню'))
async def menu(mes):
    key_category = types.InlineKeyboardMarkup(row_width=1)
    buttons_category = [
        types.InlineKeyboardButton('Завтраки', callback_data='category_breakfast'),
        types.InlineKeyboardButton('Холодные закуски', callback_data='category_cold'),
        types.InlineKeyboardButton('Салаты', callback_data='category_salad')
    ]
    key_category.add(*buttons_category)

    f = open('menu.png', 'rb')
    await bot.send_photo(mes.from_user.id, photo=f)
    await bot.send_message(mes.from_user.id, 'Посмотрите наше меню и выберите блюдо', reply_markup=key_category)


@dp.callback_query_handler(Text(startswith='category'))
async def category(call):
    if call.data == 'category_breakfast':
        await bot.send_message(call.from_user.id, '🍳 Завтраки:')
    if call.data == 'category_cold':
        await bot.send_message(call.from_user.id, '🥪 Холодные закуски:')
    if call.data == 'category_salad':
        await bot.send_message(call.from_user.id, '🥗 Cалаты:')
    con = connect('shop.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM meal WHERE category=="{call.data}"')
    all_meals = cur.fetchall()
    
    for i in all_meals:
        key = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton('Добавить в корзину', callback_data=f'add_{i[0]}')
        ]
        key.add(*buttons)
        await bot.send_message(call.from_user.id,  i[1]+' - '+str(i[2])+'руб', reply_markup=key)

    con.commit()

@dp.callback_query_handler(Text(startswith='add'))
async def add_basket(call):
    data = call.data
    id = data.split('_')[1]
    con = connect('shop.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM meal WHERE id=={id}')
    meal = cur.fetchone()
    print(meal)
    cur.execute(f'INSERT INTO basket VALUES({call.from_user.id}, {id})')
    con.commit()
    await bot.answer_callback_query(call.id, 'Успешно добавлено', show_alert=True)

@dp.message_handler(Text(equals='Корзина'))
async def basket(mes):
    id_user = mes.from_user.id
    con = connect('shop.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM basket WHERE id_user=={id_user}')
    bask_user = cur.fetchall()
    await bot.send_message(mes.from_user.id, '🛒 Корзина:')
    sum=0
    for i in bask_user:
        cur.execute(f'SELECT * FROM meal WHERE id=={i[1]}')
        meal = cur.fetchone()
        sum = sum + meal[2]
        key = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton('Удалить из корзины', callback_data=f'del_{meal[0]}')]
        key.add(*buttons)
        await bot.send_message(mes.from_user.id, meal[1]+' - '+str(meal[2])+'руб', reply_markup=key)
        con.commit()
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton('Оплатить',  callback_data='pay', url='https://ru.wiktionary.org/wiki/%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B8%D1%82%D1%8C'))
    await bot.send_message(mes.from_user.id, f'💸 Итого: {sum}руб', reply_markup=key)
    

@dp.callback_query_handler(Text(startswith='del'))
async def del_meal(call):
    id = call.data.split('_')[1]
    await bot.delete_message(call.from_user.id, call.message.message_id)
    con = connect('shop.db')
    cur = con.cursor()
    cur.execute(f'DELETE FROM basket WHERE id={id}   ')
    con.commit()


if __name__  == "__main__":
    executor.start_polling(dp)
