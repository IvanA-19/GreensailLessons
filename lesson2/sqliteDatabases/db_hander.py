import sqlite3


db = sqlite3.connect("users.db", check_same_thread=False)

cursor = db.cursor()

# Создадим таблицу users
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
name TEXT_FIELD,
last_name TEXT_FIELD,
age INT,
email TEXT_FIELD,
user_ID INT);""")

# Внесем в таблицу users две новых записи
cursor.execute(f"SELECT user_ID FROM users WHERE user_ID={1}")
if cursor.fetchone() is None:
    cursor.execute(f"INSERT INTO users(name, last_name, age, email, user_ID) VALUES ({"John"}, {"Taylor"}, "
                   f"{32}, {"test123@mail.ru"}, {1})")
    db.commit()

cursor.execute(f"SELECT user_ID FROM users WHERE user_ID={2}")
if cursor.fetchone() is None:
    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)", ["Kris", "Bain", 20, "test345@gmail.com", 2])
    db.commit()

# Теперь выберем все данные из таблицы и выведем их на экран в виде списка
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
