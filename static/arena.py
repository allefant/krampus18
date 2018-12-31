from pet import Pet, colors
import math

class State:
    def __init__(self):
        self.start = None
        self.t = 0
        self.name = ""
        self.turn = 0
        self.server = 0 # 0 = unknown, 1 = ok, -1 = down
        self.round = 0
        self.check_round_t = None
        self.redo = False
FPS = 20
state = State()

pets = []
pets_by_id = {}
next_position = {}
next_target = {}
next_hp = {}

def redraw(t):
    canvas = document.getElementsByTagName("canvas")[0]
    w = canvas.width
    h = canvas.height
    c = canvas.getContext('2d')

    draw_frame(c, w, h)

    if len(pets) == 0:
        c.fillStyle = "red"
        c.textAlign = "center"
        c.fillText("`" + state.name + "´ does not seem to exist", w / 2, h / 4)

    s = w / 100

    for pet in pets:
        x, y, z, a = get_position(pet, t)
        pet.draw_z(c, x * s, y * s, w / 32, a)

    for pet in pets:
        x, y, z, a = get_position(pet, t)

        if pet.pid in next_target and next_target[pet.pid] != 0:
            pet2 = pets_by_id[next_target[pet.pid]]
            if pet2 is not None:
                x2, y2, z2, a2 = get_position(pet2, t)
                if x2 >= 0:
                    col = pet.data["behavior_primary"]
                    c.strokeStyle = colors[col + 8 * col]
                    c.beginPath()
                    # we don't use 1000 so we don't overshoot
                    xp = x + (x2 - x) * t / 1200
                    yp = y + (y2 - y) * t / 1200
                    xp2 = x + (x2 - x) * t / 1100
                    yp2 = y + (y2 - y) * t / 1100
                    c.moveTo(xp * s, yp * s)
                    c.lineTo(xp2 * s, yp2 * s)
                    c.lineWidth = 2 * s
                    c.stroke()
                    c.lineWidth = 1

    c.textAlign = "center"
    h = c.measureText("00").width
    for pet in pets:
        x, y, z, a = get_position(pet, t)
        c.fillStyle = "black"
        c.fillText(pet.name, x * s, y * s - w / 32 * 2)
        color = "green"
        if pet.hp < 25: color = "firebrick"
        elif pet.hp < 50: color = "darkorange"
        elif pet.hp < 80: color = "gold"
        c.fillStyle = color
        c.fillText(pet.hp, x * s, y * s - w / 32 * 2 - h)

    if state.server == -1:
        c.fillStyle = "red"
        c.textAlign = "center"
        c.fillText("Looks like the server may be down.", w / 2, 20)
        c.fillText("Email krampus18@allefant.com and I'll restart it when I wake up!", w / 2, 40)

def get_position(pet, t):
    if not pet: return -100, -100, 0, 0
    pos = next_position.get(pet.pid, None)
    if pos is None: return -100, -100, 0, 0
    x, y, z, a = pos
    x = pet.x + (x - pet.x) * t / 1000
    y = pet.y + (y - pet.y) * t / 1000
    z = pet.z + (z - pet.z) * t / 1000
    da = a - pet.a
    if da > 180: da -= 360
    if da < -180: da += 360
    a = pet.a + (da) * t / 1000
    return x, y, z, a

def draw_frame(c, w, h):
    c.fillStyle = 'silver'
    c.fillRect(0, 0, w, h)
    c.strokeStyle = 'black'
    c.strokeRect(0, 0, w, h)

    c.save()
    c.font = "48px sans"
    th = c.measureText("W").width
    c.fillStyle = "lightgray"
    c.textAlign = "center"
    c.fillText("Round " + str(state.round) if state.round > 0 else "...", w / 2, th)
    c.restore()

    c.fillStyle = "yellow"
    x = state.t * w / FPS / 10
    x %= (w * 2 + h * 2)
    y = 0
    if x > w:
        y = x - w
        x = w
        if y > h:
            x = w - (y - h)
            y = h
            if x < 0:
                y = h + x
                x = 0
    c.fillRect(x - w / 200, y - h / 200, w / 100, h / 100)

def resync(t):
    for pet in pets:
        pos = next_position.get(pet.pid, None)
        if pos:
            x, y, z, a = pos
            pet.x = pet.x + (x - pet.x) * t / 1000
            pet.y = pet.y + (y - pet.y) * t / 1000
            pet.z = pet.z + (z - pet.z) * t / 1000
            pet.a = pet.a + (a - pet.a) * t / 1000
        pet.hp = next_hp.get(pet.pid, pet.hp)
    read_position(state.name)

def step(timestamp):
    if not state.start:
        state.start = timestamp
        state.t = 0
        state.turn = 0
    progress = timestamp - state.start
    if progress >= state.t * 1000 / FPS:
        p = 1000 + progress - state.turn * 1000
        if p > 5000:
            # if we fell too far behind just reset
            state.t = 0
            state.turn = 0
            state.start = timestamp
        redraw(p)
        state.t += 1

    if progress >= state.turn * 1000:
        p = 1000 + progress - state.turn * 1000
        resync(p)
        state.turn += 1
    
    window.requestAnimationFrame(step)

def api_call(url, data, on_receive):
    r = __new__(XMLHttpRequest())
    def onreadystatechange():
        if r.readyState == 4 and r.status == 200:
            j = JSON.parse(r.responseText)
            on_receive(j)
    r.onreadystatechange = onreadystatechange
    r.open("POST", url)
    r.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
    r.send(data)

def read_round():
    def on_receive(j):
        if state.round > 0 and state.round != j[0]:
            state.redo = True
        state.round = j[0]
    api_call("/arena/round", "name=" + state.name, on_receive)

def now():
    return __new__(Date()).getTime()

def read_position(whose):
    def on_receive(j):
        redo = False
        existing = set()
        for pid, owner, x, y, z, a, target, hp in j:
            next_position[pid] = x, y, z, a
            next_target[pid] = target
            next_hp[pid] = hp
            existing.add(pid)

            if owner is None and hp <= 0 and not state.check_round_t:
                state.check_round_t = now() + 1000 * 7

            if pid not in pets_by_id:
                redo = True
                console.log("gained new pet", pid)

        for i in range(len(pets) - 1, -1, -1):
            if pets[i].pid not in existing:
                console.log("lost pet", pets[i].pid)
                pets_by_id.pop(pets[i].pid)
                pets.pop(i)

        if redo or state.redo: # if a new one joins we need its DNA...
            begin_animation(state.who, state.name)
            state.redo = False

    api_call("/arena/pos", "name=" + state.name, on_receive)

    t = now()
    if t > state.check_t:
        state.check_t += 1000 * 10 # 10 seconds
        check_server()

    if state.round == 0 and not state.check_round_t:
        state.check_round_t = now() + 1000 * 1

    if state.check_round_t and t > state.check_round_t:
        state.check_round_t = None
        read_round()

def check_server():
    def on_receive(j):
        if j[0] == state.server_t: # server did not advance at all
            state.server = -1
        else:
            state.server = 1
        state.server_t = j[0]
    api_call("/arena/t", "name=" + state.name, on_receive)

def begin_animation(who, whose, server_t):
    canvas = document.getElementsByTagName("canvas")[0]
    state.name = whose
    state.who = who
    state.server_t = server_t
    state.check_t = __new__(Date()).getTime() + 1000 * 5
    state.server = 0

    def on_receive(j):
        window.requestAnimationFrame(step)
        for pid, owner, name, dna in j:
            if pid not in pets_by_id:
                pet = Pet()
                pet.pid = pid
                pet.owner = owner if owner else 0
                pet.name = name if name else "boss"
                pets_by_id[pet.pid] = pet
                pets.append(pet)
            else:
                pet = pets_by_id[pid]
                
            pet.from_json(dna)
            pet.make_balls()
                
    api_call("/arena/dna", "name=" + whose, on_receive)

