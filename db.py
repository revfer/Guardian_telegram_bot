import sqlite3

con = sqlite3.connect('users_list.db', check_same_thread=False)
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Users_cod (User_id TEXT, Chat_id INT, payed INT DEFAULT 0)''')


def add_user(user_id, chat_id):
    users = cur.execute(f'SELECT Chat_id FROM Users_cod WHERE Chat_id == {chat_id}').fetchall()
    if len(users) == 0:
        cur.execute('INSERT INTO Users_cod (User_id, Chat_id) VALUES(?, ?)', (user_id, chat_id))
        con.commit()
    else:
        cur.execute('UPDATE Users_cod SET User_id=? WHERE Chat_id=?', (user_id, chat_id))
        con.commit()


def update_user_pay(chat_id, payed):
    cur.execute('UPDATE Users_cod SET payed=? WHERE Chat_id=?', (payed, chat_id))
    con.commit()


def is_payed(chat_id):
    is_ = cur.execute(f'SELECT payed FROM Users_cod WHERE Chat_id == {chat_id}').fetchone()
    # print(is_)
    if is_:
        if is_[0] == 1:
            return True
    return False


def get_user_data(chat_id):
    a = list(cur.execute(f'SELECT * FROM Users_cod WHERE Chat_id == {chat_id}').fetchone())
    if len(a) != 0:
        return a
    return None
