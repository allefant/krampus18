#!/usr/bin/env python3
#encoding: utf8

import pymysql

class C:
    def sql(self, query, args = None):
        self.cursor.execute(query, args)
        r = self.cursor.fetchall()
        self.db.commit()
        return r

def access_db():
    global c
    c = C()
    c.db = pymysql.connect(host = "localhost", user = "krampus18",
        passwd = "krampushack", db = "krampus18")
    c.cursor = c.db.cursor()

def exit_db():
    c.cursor.close()
    c.db.close()

def list_arenas():
    return c.sql("SELECT id, open, owner FROM arena")

def login(name, access_phrase):
    if not name:
        return "name"
    r = check_existing(name, access_phrase)
    if r:
        return r
    try:
        r = c.sql("""
            INSERT INTO player (name, access_phrase)
            VALUES (%s, %s)""", (name, access_phrase))
        return "new"
    except pymysql.err.IntegrityError as e:
        r = check_existing(name, access_phrase)
        if r:
            return r
        return "error"

def check_existing(name, access_phrase):
    r = c.sql("SELECT id, access_phrase FROM player WHERE name=%s", (name,))
    if r:
        if r[0][1] == access_phrase:
            return "login"
        else:
            return "phrase"
    return None

if __name__ == "__main__":
    access_db()
    print(list_arenas())
    print(login("", ""))
    exit_db()
