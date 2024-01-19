import sqlite3 as sql

connection = sql.connect("database.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")



cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
res = cursor.fetchall()
print(res)
cursor.execute("SELECT * FROM users")
res = cursor.fetchall()
print(res)

connection.close()


