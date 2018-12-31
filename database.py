#!/usr/bin/env python3
#encoding: utf8

import pymysql
import config

c = None

class C:
    def sql(self, query, args = None):
        self.cursor.execute(query, args)
        r = self.cursor.fetchall()
        self.db.commit()
        return r

def access_db():
    global c
    if c is not None: return
    c = C()
    c.db = pymysql.connect(host = config.DBHOST, user = config.DBUSER,
        passwd = config.DBPASSWD, db = config.DBDB)
    c.cursor = c.db.cursor()

def exit_db():
    global c
    c.cursor.close()
    c.db.close()
    c = None

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

def create_boss(aid, dna, x, y, z, a, hp):
    c.sql("INSERT INTO pet (arena, dna, x, y, z, a, hp) VALUES (%s, %s, %s, %s, %s, %s, %s)", (aid, dna, x, y, z, a, hp))
    r = c.sql("SELECT LAST_INSERT_ID()")
    return r[0][0]

def update_boss(pid, dna):
    c.sql("UPDATE pet SET dna = %s WHERE id = %s", (dna, pid))

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

def restart_arena(whose, yes, r):
    c.sql("UPDATE arena SET restart = %s, round = %s WHERE owner = (SELECT id FROM player WHERE name = %s)", (yes, r, whose))

def get_dna_in_arena(name):
    r = c.sql("""SELECT p.id, p.owner, o.name, p.dna FROM pet p LEFT JOIN player o ON p.owner = o.id
     WHERE p.arena = (SELECT id FROM arena WHERE owner = (SELECT id FROM player WHERE name = %s))""", (name, ))
    return r

def get_players_names(players):
    r = c.sql("SELECT name FROM player WHERE id IN %s", (players, ))
    return r

def get_pos_in_arena(name = None, aid = None):
    if name is not None:
        arena = "arena = (SELECT id FROM arena WHERE owner = (SELECT id FROM player WHERE name = %s))"
    else:
        arena = "arena = %s"
        name = aid
    r = c.sql("SELECT id, owner, x, y, z, a, target_pet, hp FROM pet WHERE " + arena, (name, ))
    return r

def set_pos_in_arena(update):
    rows = ["(" + (",".join(["'%s'" % v for v in row])) + ")" for row in update]
    s = ",".join(rows)
    sql = """INSERT INTO pet (id, x, y, z, a, target_pet, hp)
        VALUES %s
        ON DUPLICATE KEY UPDATE
        x = VALUES(x), y = VALUES(y), z = VALUES(z), a = VALUES(a), target_pet = VALUES(target_pet),
        hp = VALUES(hp)
        """ % s
    #print(sql)
    c.sql(sql)

def get_open_arenas():
    r = c.sql("SELECT id, (SELECT name FROM player WHERE id=owner), restart, round FROM arena WHERE open=%s", (1, ))
    return r

def get_arena_round(name):
    r = c.sql("SELECT round FROM arena WHERE owner=(SELECT id FROM player WHERE name=%s)", (name, ))
    if not r: return 0
    return r[0][0]

def server_heartbeat(sid):
    c.sql("INSERT INTO server (id, t) VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE t = VALUES(t)", (sid, ))

def server_get_t(sid):
    return c.sql("SELECT t FROM server WHERE id = %s", (sid, ))[0][0]

if __name__ == "__main__":
    access_db()
    #print(list_arenas())
    #print(login("", ""))
    #save_pet("test2", "{\"eye_size\" : 3}")
    #enter_arena("al", "al")
    #enter_arena("test", "al")
    #print(get_pos_in_arena(name = "al"))
    #pos = get_pos_in_arena(aid = 2)
    #print(pos)
    dna = get_dna_in_arena("al")
    for d in dna:
        print(d)
    #set_pos_in_arena(pos)
    #print(get_open_arenas())
    #print(create_boss(1, '{}'));
    #restart_arena("al", 1, 2)
    exit_db()
