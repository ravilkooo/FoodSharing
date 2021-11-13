import math
import sqlite3
import time

from flask import url_for


class FShDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_guest_menu(self):
        sql = '''SELECT * FROM guestmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД " + str(e))
        return []

    def add_user(self, name, surname, email, hash_password):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('add_user(): Пользователь с таким email уже существует')
                return False
            else:
                tm = math.floor(time.time())
                self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, '', ?, ?, NULL)", (name, surname, email, hash_password))
                self.__db.commit()
        except sqlite3.Error as e:
            print("add_user(): Ошибка добавления в БД " + str(e))
            return False
        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id ==  {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("get_user(): Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("get_user(): Ошибка чтения из БД " + str(e))
        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email LIKE  '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("get_user_by_mail(): Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("get_user_by_mail(): Ощибка чтения из БД: "+str(e))
        return False

    def get_role(self, user_id):
        try:
            self.__cur.execute(f"SELECT role_id FROM users_roles WHERE user_id == {user_id} LIMIT 1")
            role_id = self.__cur.fetchone()
            if not role_id:
                print("get_role(): Пользователь не найден")
                return False
            self.__cur.execute(f"SELECT role FROM roles WHERE id == {role_id['role_id']} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("get_role(): Роль не найдена")
                return False
            return res['role']
        except sqlite3.Error as e:
            print("get_role(): Ошибка чтения из БД: "+str(e))
        return False

    def update_user_avatar(self, avatar, user_id):
        if not avatar:
            return False
        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute("UPDATE users SET avatar = ? WHERE id == ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: "+str(e))
            return False
        return True

