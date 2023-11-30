from sqlite3 import *

con = connect('shop.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS meal(id INTEGER PRIMARY KEY, name TEXT, price INTEGER, category TEXT)')
cur.execute('INSERT INTO meal VALUES (NULL, "Яичница глазунья", 100, "category_breakfast")')
cur.execute('INSERT INTO meal VALUES (NULL, "Омлет", 120, "category_breakfast")')
cur.execute('INSERT INTO meal VALUES (NULL, "Сырное ассорти", 410, "category_cold")')
cur.execute('INSERT INTO meal VALUES (NULL, "Брускетта с лососем", 240, "category_cold")')
cur.execute('INSERT INTO meal VALUES (NULL, "Брускетта со спаржей", 190, "category_cold")')
cur.execute('INSERT INTO meal VALUES (NULL, "Деревенский", 170, "category_salad")')
cur.execute('INSERT INTO meal VALUES (NULL, "Греческий", 280, "category_salad")')

cur.execute('CREATE TABLE IF NOT EXISTS basket(id_user INTEGER, id INTEGER)')

con.commit()
