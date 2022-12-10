from aiogram.dispatcher.filters import Text 
from aiogram import *
from sqlite3 import *
from random import *

bot = Bot(token='5221530880:AAHy1CgawjSuvy6x2ZKg_-q5ovXCgPKGJ3Q')
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(mes: types.Message):
    coon = connect('shop.db')
    cur = coon.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS user(user_id INTEGER, balance INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS bag(user_id INTEGER, id_meal INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS menu(id INTEGER PRIMARY KEY, meal TEXT, price INTEGER, category TEXT)')
    
    
    cur.execute('INSERT INTO menu VALUES(null, "Яичница глазунья", 100, "breakfast")')
    cur.execute('INSERT INTO menu VALUES(null, "Воздушный омлет", 120, "breakfast")')
    cur.execute('INSERT INTO menu VALUES(null, "Скрэмбл с авокадо", 310, "breakfast")')
    cur.execute('INSERT INTO menu VALUES(null, "Домашние сырники Американо", 180, "breakfast")')
    cur.execute('INSERT INTO menu VALUES(null, "Каша овсяная с ягодами", 100, "breakfast")')
    cur.execute('INSERT INTO menu VALUES(null, "Бенедикт с малосолной семгой", 370, "breakfast")')
    cur.execute('INSERT INTO menu VALUES(null, "Фирменный брекфаст", 240, "breakfast")')
    cur.execute('INSERT INTO menu VALUES(null, "Бельгийские вафли с семгой и авокадо", 290, "breakfast")')
    cur.execute('INSERT INTO menu VALUES(null, "Сырное ассорти", 410, "coldsnack")')
    cur.execute('INSERT INTO menu VALUES(null, "Брускетта с лососем", 240, "coldsnack")')
    cur.execute('INSERT INTO menu VALUES(null, "Брускетта со спаржей", 190, "coldsnack")')
    cur.execute('INSERT INTO menu VALUES(null, "Брускетта с креветками", 200, "coldsnack")')
    cur.execute('INSERT INTO menu VALUES(null, "Деревенский", 170, "salad")')
    cur.execute('INSERT INTO menu VALUES(null, "Греческий", 280, "salad")')
    cur.execute('INSERT INTO menu VALUES(null, "Цезарь с курицей", 290, "salad")')
    

    button = ['Меню','Моя корзина','Забронировать']
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key.add(*button)
    await mes.answer('Зайдите в меню, что бы выбрать, что покушать', reply_markup=key)
    coon.commit()

@dp.message_handler(Text(equals='Меню'))
async def menu(mes:types.Message):
    photo = open('menu.png', 'rb')
    await bot.send_photo(mes.from_user.id, photo)

    buttons = [
        types.InlineKeyboardButton('Завтраки', callback_data= 'category_breakfast'),
        types.InlineKeyboardButton('Холодные закуски', callback_data= 'category_coldsnacks'),
        types.InlineKeyboardButton('Салаты', callback_data= 'category_salad'),
        types.InlineKeyboardButton('Суп', callback_data= 'category_soup'),
        types.InlineKeyboardButton('Горячие закуски', callback_data= 'category_hotsnacks'),
        types.InlineKeyboardButton('Паста', callback_data= 'category_pasta'),
        types.InlineKeyboardButton('Горячие блюда', callback_data= 'category_hotmeals'),
        types.InlineKeyboardButton('Гарниры', callback_data= 'category_sidedish'),
        types.InlineKeyboardButton('Бургеры и Сэдвичи', callback_data= 'category_burgersandsandwiches'),
        types.InlineKeyboardButton('Пицца', callback_data= 'category_pizza'),
        types.InlineKeyboardButton('Роллы', callback_data= 'category_rolls')
        ]
    category = types.InlineKeyboardMarkup().add(*buttons)
    await mes.answer('Выберите категорию',
                     reply_markup=category)

@dp.callback_query_handler(Text(startswith='category'))
async def all_meal(cal:types.callback_query):
    coon = connect('shop.db')
    cur = coon.cursor()
    action = cal.data.split('_')[1]

    if action=='breakfast':
        cur.execute(f'Select id, meal, price FROM menu WHERE category="breakfast" ')
        c = cur.fetchall()
        for id, name, price in c:
            buttons = [
                types.InlineKeyboardButton('add', callback_data=f'add_{id}'),
                types.InlineKeyboardButton('info', callback_data=f'info_{id}')
            ]
            key = types.InlineKeyboardMarkup().add(*buttons)
            await bot.send_message(cal.from_user.id, f'{name} - {price} руб', reply_markup=key)
    

@dp.callback_query_handler(Text(startswith='info'))
async def all_meal(cal:types.callback_query):
    action = cal.data.split('_')[1]
    if action=='1':
        await cal.answer('яйца', show_alert = True)
        await cal.answer()


@dp.callback_query_handler(Text(startswith='add'))
async def all_meal(cal:types.callback_query):
    action = cal.data.split('_')[1]
    con = connect('shop.db')
    cur = con.cursor()
    cur.execute(f'INSERT INTO bag VALUES({cal.from_user.id}, {action})')
    con.commit()
    await cal.answer('ХАВЧЕГ ДОБАВЛЕН')


@dp.message_handler(Text(equals='Моя корзина'))
async def menu(mes:types.Message):
    con = connect('shop.db')
    cur = con.cursor()
    cur.execute('SELECT id_meal FROM bag')
    eda = cur.fetchall()
    textmes=''
    print(eda[0][0])
    button = types.InlineKeyboardButton('Завершить заказ', callback_data=1)
    key = types.InlineKeyboardMarkup().add(button)
    total_amount=0
    for i in eda:
        cur.execute(f'SELECT meal, price FROM menu WHERE id={i[0]}')
        f = cur.fetchone()
        textmes+=f'{f[0]}-{f[1]} RUB\n'
        total_amount+=f[1]
    await mes.answer(textmes)
    await mes.answer(f"Общая стоимость: {total_amount}", reply_markup= key)
    



@dp.callback_query_handler(text='b1')
async def meal(mes: types.callback_query):
    buttons = [
        types.InlineKeyboardButton('Add'),
        types.InlineKeyboardButton('info', callback_data='random_value')
        ]
    conn = connect('shop.db')
    cur = conn.cursor()
    cur.execute(f'SELECT meal, price FROM menu_breakfast')
    meal = cur.fetchall()
    for name, price in meal:
        await bot.send_photo(mes.from_user.id, f'{name} - {price} руб')
    
    conn.commit()

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
 await call.message.answer(str(randint(1, 10)))
 await call.answer(text="ИНГРЕДИЕНТЫ: картофель вареный морковка яйца сваренные вкрутую колбаса вареная огурцы маринованные (можно свежие) горошек зеленый консервированный майонез листья петрушки и укропа по желаниюсоль, свежемолотый черный перец", show_alert=True)

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()