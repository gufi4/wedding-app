import sqlite3
conn = sqlite3.connect('wedding_bot.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM guests')
for row in cursor.fetchall():
    print(row)
conn.close()
