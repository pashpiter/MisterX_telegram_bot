import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(
    user_id: int, user_name: str, user_surname: str, username: str
) -> bool:
    """Добавление пользователя в базу"""
    info = cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    if info.fetchone() is None:
        cursor.execute(
            'INSERT INTO Users (user_id, user_name, user_surname, username) '
            'VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username)
        )
        conn.commit()
        print(cursor.fetchall())
        return True
