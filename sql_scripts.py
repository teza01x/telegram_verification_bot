import sqlite3
from config import *


def user_exists(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_id FROM user_info WHERE user_id = ?", (user_id,))
    exists = bool(len(result.fetchall()))

    conn.close()

    return exists


def add_user(user_id, username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_info (user_id, user_name, user_email, user_insta, user_phone, user_verification, start_menu, status, username, referal) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, None, None, None, None, 0, None, 0, username, 0,))

    conn.commit()
    conn.close()


def check_start_menu_id(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT start_menu FROM user_info WHERE user_id = ?", (user_id,))
    id_menu = cursor.fetchone()[0]

    conn.close()

    return id_menu


def add_start_menu_id(user_id, menu_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET start_menu = ? WHERE user_id = ?", (menu_id, user_id,))

    conn.commit()
    conn.close()


def get_user_info(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, user_email, user_insta, user_phone FROM user_info WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()[0]

    conn.close()

    return data


def status_update(user_id, status):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET status = ? WHERE user_id = ?", (status, user_id,))

    conn.commit()
    conn.close()


def status_check(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM user_info WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def name_entry(user_id, user_name):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET user_name = ? WHERE user_id = ?", (user_name, user_id,))

    conn.commit()
    conn.close()


def mail_entry(user_id, user_mail):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET user_email = ? WHERE user_id = ?", (user_mail, user_id,))

    conn.commit()
    conn.close()


def insta_entry(user_id, user_insta):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET user_insta = ? WHERE user_id = ?", (user_insta, user_id,))

    conn.commit()
    conn.close()


def phone_entry(user_id, user_phone):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET user_phone = ? WHERE user_id = ?", (user_phone, user_id,))

    conn.commit()
    conn.close()


def add_user_app(user_id, username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO apps (user_id, user_name, user_email, user_insta, user_phone, status, message_id, username, key_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, None, None, None, None, 0, None, username, None))

    conn.commit()
    conn.close()


def user_send_app(user_id, user_name, user_email, user_insta, user_phone, status):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE apps SET user_name = ?, user_email = ?, user_insta = ?, user_phone = ?, status = ? WHERE user_id = ?", (user_name, user_email, user_insta, user_phone, status, user_id,))

    conn.commit()
    conn.close()


def change_app_status(user_id, status):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE apps SET status = ? WHERE user_id = ?", (status, user_id,))

    conn.commit()
    conn.close()


def check_app_status(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM apps WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def user_message_id(user_id, message_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE apps SET message_id = ? WHERE user_id = ?", (message_id, user_id,))

    conn.commit()
    conn.close()


def get_username(message_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM apps WHERE message_id = ?", (message_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def verification_status(user_id, user_verification):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET user_verification = ? WHERE user_id = ?", (user_verification, user_id,))

    conn.commit()
    conn.close()


def check_verification(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_verification FROM user_info WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def get_user_id(message_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM apps WHERE message_id = ?", (message_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def set_user_key(user_email, key_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE apps SET key_id = ? WHERE user_email = ?", (key_id, user_email,))

    conn.commit()
    conn.close()


def check_user_key(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT key_id FROM apps WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def set_referal_code(user_id, referal):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_info SET referal = ? WHERE user_id = ?", (referal, user_id,))

    conn.commit()
    conn.close()


def check_referal_code(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT referal FROM user_info WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def get_inviter_inst_by_key(key_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_insta FROM apps WHERE key_id = ?", (key_id,))
    data = cursor.fetchone()

    conn.close()

    return data


def make_admin(owner_id, admin_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE admin SET admin_id = ? WHERE owner_id = ?", (referal, user_id,))

    conn.commit()
    conn.close()


def find_admins_id_by_email(user_email):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM apps WHERE user_email = ?", (user_email,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def get_admin_id(owner_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_id FROM admin WHERE owner_id = ?", (owner_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def notification_for_ver_users():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    query = "SELECT user_id FROM user_info WHERE user_verification = 1"
    cursor.execute(query)

    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return user_ids


def get_verification_user_data():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, user_email, user_insta, user_phone, username, key_id FROM apps WHERE status = ?", (4,))
    data = cursor.fetchall()

    conn.close()

    result = list()
    for i in data:
        lst = list()
        for j in i:
            lst.append(j)
        result.append(lst)

    return result


