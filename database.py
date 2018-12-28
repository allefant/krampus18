#!/usr/bin/env python3
#encoding: utf8

import pymysql
import config

class C:
    def sql(self, query, args = None):
        self.cursor.execute(query, args)
        r = self.cursor.fetchall()
        self.db.commit()
        return r

def access_db():
    global c
    c = C()
    c.db = pymysql.connect(host = config.DBHOST, user = config.DBUSER,
        passwd = config.DBPASSWD, db = config.DBDB)
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

def save_pet(name, dna):
    r = c.sql("SELECT id FROM pet WHERE owner = (SELECT id FROM player WHERE name=%s)", (name, ))
    if not r:
        c.sql("INSERT INTO pet (owner, dna) VALUES ((SELECT id FROM player WHERE name=%s), %s)", (name, dna))
    else:
        c.sql("UPDATE pet SET dna = %s, arena = NULL, target_pet = NULL WHERE id = %s", (dna, r[0][0]))

def get_pet_dna(name):
    r = c.sql("SELECT dna FROM pet WHERE owner = (SELECT id FROM player WHERE name=%s)", (name, ))
    if r:
        return r[0][0]
    return "{}"

def create_arena(who):
    r = c.sql("SELECT id FROM arena WHERE owner = (SELECT id FROM player WHERE name = %s)", (who, ))
    if r: return
    c.sql("INSERT INTO arena (owner) VALUES ((SELECT id FROM player WHERE name=%s))", (who, ))

def enter_arena(who, whose):
    if who == whose: # auto-create arena when someone enters their own arena
        create_arena(who)
    c.sql("""
    UPDATE pet SET arena = (SELECT id FROM arena WHERE owner = (SELECT id FROM player WHERE name = %s))
WHERE owner = (SELECT id FROM player WHERE name = %s)
    """, (whose, who))

def get_dna_in_arena(name):
    r = c.sql("""SELECT b.name, a.dna FROM pet a, player b WHERE
        a.arena = (SELECT id FROM arena WHERE owner = (SELECT id FROM player WHERE name = %s)) AND
        a.owner = b.id""", (name, ))
    return r

if __name__ == "__main__":
    access_db()
    #print(list_arenas())
    #print(login("", ""))
    #save_pet("test2", "{\"eye_size\" : 3}")
    enter_arena("al", "al")
    enter_arena("test", "al")
    print(get_dna_in_arena("al"))
    exit_db()
