import sqlite3
from sqlite3 import Error
import json
from flask import Flask, request


class Items:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
            if self.conn is not None:
                self.conn.cursor().execute("""CREATE TABLE IF NOT EXISTS multi (            
                                            id integer PRIMARY KEY,
                                            media text NOT NULL,
                                            title text NOT NULL,
                                            author text,
                                            year date);""")

            self.cur = self.conn.cursor()
        except Error as e:
            print(e)

    def all(self):
        self.cur.execute("SELECT * FROM multi")
        return self.cur.fetchall()

    def get(self, id):
        self.cur.execute(f"SELECT * FROM multi WHERE id={id}")
        return self.cur.fetchone()

    def create(self, data):
        sql = '''INSERT INTO multi(media, title, author, year)
                    VALUES(?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid

    def save_all(self):
        with open("multimedia.db", "w") as f:
            json.dump(self.items, f)

    def update(self, id, data):
        sql = f''' UPDATE multi
                    SET media = ?, title = ?, author = ?, year = ?
                    WHERE id = {id[0]}'''
        print(id)

        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)

    def delete(self, conn, id):
        """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """

        cur = conn.cursor()
        cur.execute('DELETE FROM multi WHERE id=?', (id,))
        conn.commit()
        print("Deleted")


db_file = "multimedia.db"
items = Items(db_file)
