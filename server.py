#!/usr/bin/env python3
import database
import time
import json
import math
import random

"""
ideas:
    - nose size = throw radius
    - limb size = speed
    - ear size = evade chance / defense
    - eye size = hit chance / attack
    - primary = 100% attack (or heal)
    - secondary = 50% attack and 50% defense

0     1         2       3    4      5      6       7
fire, electric, nature, ice, water, magic, healer, evil
"""

elements_table = [
 2, 4, 4, 8, 8, 2, 2, 4,
 8, 2, 2, 8, 8, 2, 2, 4,
 4, 4, 4, 4, 4, 4, 2, 4,
 4, 4, 4, 4, 8, 2, 2, 4,
 8, 2, 4, 2, 4, 2, 2, 4,
 4, 4, 2, 4, 4, 8, 2, 4,
 0, 0, 0, 0, 0, 0, 0, 0,
 2, 2, 2, 2, 2, 2, 2, 4, 
    ]

def element_damge(atp, dep, ats, des):
    x = elements_table[atp * 8 + dep]
    y = elements_table[ats * 8 + des]
    return x + y // 2

class Server:

    def start(self):
        database.access_db()
        self.active = {}
        self.t0 = time.time()
        self.t1 = self.t0
        average = 0
        i = 0
        while True:
            self.tick()
            self.t1 += 1
            dt = self.t1 - time.time()
            if dt < 0.5:
                print("sleep %.2f" % dt)
            if dt > 0:
                time.sleep(dt)
                average += dt
            database.server_heartbeat(1)
            i += 1
            if i % 60 == 0:
                print("average sleep in last 60 seconds: %.2f" % (average / 60))
                average = 0

    def tick(self):
        arenas = database.get_open_arenas()
        for aid, name, restart, arena_round in arenas:
            if name in self.active and not restart:
                self.active[name].tick()
            else:
                a = Arena(aid, name, arena_round)
                a.start(restart)
                self.active[name] = a

class Arena:

    def __init__(self, aid, name, r):
        self.aid = aid
        self.name = name
        self.pets = {}
        self.w = 100
        self.h = 100
        self.boss = 0
        self.collider = 0 # pid of colliding pet
        self.round = r
        self.boss_defeat_t = None

    def start(self, restart):
        print("starting arena", self.aid, self.name, "round", self.round)
        pos = database.get_pos_in_arena(aid = self.aid)
        for args in pos:
            pet = Pet(*args)
            if pet.owner != 0 and pet.pid not in self.pets:
                pet.reset = True
            self.pets[pet.pid] = pet
            if pet.owner == 0:
                self.boss = pet.pid

        dna = database.get_dna_in_arena(self.name)
        for pid, owner, name, d in dna:
            self.pets[pid].setup_dna(d)

        if self.boss == 0:
            print("creating boss for", self.aid, self.name)
            self.create_boss()

        if restart:
            update = []
            i = 0
            n = len(self.pets) - 1
            for pet in self.pets.values():
                pet.target = 0
                if pet.owner == 0:
                    pet.x = 90
                    pet.y = 50
                    pet.a = 90
                    pet.hp = 1000
                else:
                    pet.x = 10
                    pet.y = 10 + i * 80 / ((n - 1) if n > 1 else 2)
                    pet.a = 270
                    pet.hp = 100
                update.append((pet.pid, pet.x, pet.y, pet.z, pet.a, pet.target, pet.hp))
                i += 1
            database.set_pos_in_arena(update)
            database.restart_arena(self.name, 0, self.round)

    def find_closest_pet(self, boss):
        minq = None
        minp = None
        for pet in self.pets.values():
            if pet.owner == 0: continue
            if pet.hp <= 0: continue
            if pet.x is None: continue
            dx = pet.x - boss.x
            dy = pet.y - boss.y
            q = dx * dx + dy * dy
            if minq is None or q < minq:
                minq = q
                minp = pet
        return minp

    def get_update(self):
        update = []
        for pet in self.pets.values():
            update.append((pet.pid, pet.x, pet.y, pet.z, pet.a, pet.target, pet.hp))
        return update

    def tick(self):
        pos = database.get_pos_in_arena(aid = self.aid)
        redo = False
        want_target = 0
        
        existing = set()
        coli = random.randint(1, len(pos))
        i = 0
        for pid, owner, x, y, z, a, target, hp in pos:
            i += 1
            if owner is None: owner = 0
            if target is None: target = 0
            if pid not in self.pets:
                redo = True
                continue
            if i == coli:
                self.collider = pid
            existing.add(pid)
            if x is None: continue
            pet = self.pets[pid]
            if owner == 0: # boss
                if target != 0:
                    tpet = self.pets.get(target, None)
                    if tpet:
                        dx = tpet.x - x
                        dy = tpet.y - y
                        ta = math.atan2(dy, dx)
                        a = (ta * 180) / math.pi - 90
            else:
                target = 0
                if self.boss != 0 and hp > 0:
                    tpet = self.pets[self.boss]
                    dx = tpet.x - x
                    dy = tpet.y - y
                    ta = math.atan2(dy, dx)
                    a = (ta * 180) / math.pi - 90
                    d = math.sqrt(dx * dx + dy * dy)
                    if d > pet.attack_distance:
                        x += math.cos(ta) * pet.speed
                        y += math.sin(ta) * pet.speed
                    else:
                        target = self.boss

                if self.collider and hp > 0:
                    # will collide with itself but we do not care, it
                    # gives us some random movement
                    cpet = self.pets[self.collider]
                    cx = cpet.x - x
                    cy = cpet.y - y
                    if cx * cx + cy * cy < 5 * 5:
                        c = math.sqrt(cx * cx + cy * cy)
                        if c < 0.1: c = 0.1
                        x += random.randint(-1, 1) - cx / c * (5 - c)
                        y += random.randint(-1, 1) - cy / c * (5 - c)

            pet.update(x, y, z, a, target, hp)

        # fight
        for pet in self.pets.values():
            if not pet.target: continue
            tpet = self.pets.get(pet.target, None)
            if not tpet: continue
            pet.attack(tpet)
        
        if self.boss != 0:
            boss = self.pets[self.boss]
            if boss.hp <= 0:
                boss.target = 0
                if not self.boss_defeat_t:
                    self.boss_defeat_t = time.time()
                    print("boss is dead for", self.name, "advancing to round", self.round + 1)
                elif time.time() - self.boss_defeat_t > 10:
                    database.restart_arena(self.name, 1, self.round + 1)
            else:
                target = self.find_closest_pet(boss)
                if target:
                    boss.target = target.pid

        if self.pets:
            update = self.get_update()
            database.set_pos_in_arena(update)

            for pid in list(self.pets.keys()):
                if pid not in existing:
                    self.pets.pop(pid)
                    print("Lost", pid, "in", self.name)

        if redo:
            self.start(False)

    def create_boss(self):
        x, y, z, a = 90, 50, 0, 90
        dna = '{"behavior_primary":5,"behavior_secondary":5,"eye_count":1,"eye_height":8,"eye_space":3,"eye_size":5,"limb_count":1,"limb_size":4,"limb_n":6,"nose_height":6,"nose_size":6,"nose_n":6,"nose_color":3,"nose_nostrils":2,"ear_height":10,"ear_size":6}'
        args = database.create_boss(self.aid, dna, x, y, z, a), 0, x, y, z, a, 0
        pet = Pet(*args)
        self.pets[pet.pid] = pet
        pet.dna = dna
        self.boss = pet.pid

class Pet:
    def __init__(pet, pid, owner, x, y, z, a, target, hp):
        pet.pid = pid
        pet.owner = owner if owner else 0
        pet.name = "unknown"
        pet.reset = False
        pet.update(x, y, z, a, target, hp)

    def update(pet, x, y, z, a, target, hp):
        if pet.reset:
            pet.reset = False
            pet.x = 10
            pet.y = random.randint(10, 18 + 80)
            pet.z = 0
            pet.a = 270
            pet.hp = 100
        else:
            if x < 0: x = 0
            if x > 100: x = 100
            if y < 0: y = 0
            if y > 100: y = 100
            pet.x = x
            pet.y = y
            pet.z = z
            pet.a = a
            pet.hp = hp
        pet.target = target if target else 0

    def setup_dna(pet, d):
        pet.dna = json.loads(d)
        pet.attack_distance = (1 + pet.dna["nose_size"]) * (1 + pet.dna["nose_n"]) / 32 * 80
        pet.speed = (1 + pet.dna["limb_count"]) * (1 + pet.dna["limb_size"]) * (1 + pet.dna["limb_n"]) / 128 * 16
        visual_strength = [0, 1, 1.5, 1.75][pet.dna["eye_count"]]
        pet.attack_power = visual_strength * (1 + pet.dna["eye_size"])
        pet.defense_power = pet.dna["ear_size"]
        pet.primary = pet.dna["behavior_primary"]
        pet.secondary = pet.dna["behavior_secondary"]

    def attack(pet, other):
        if other.hp <= 0:
            pet.target = 0
            return
        attack_points = pet.attack_power
        if attack_points == 0: return
        defense_points = other.defense_power
        p = attack_points / (attack_points + defense_points)
        r = random.random()
        if p > r:
            other.hp -= element_damge(pet.primary, other.primary, pet.secondary, other.secondary)
            if other.hp < 0: other.hp = 0

if __name__ == "__main__":
    server = Server()
    server.start()
