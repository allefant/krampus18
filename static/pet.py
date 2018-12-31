import math
import re
from math import pi

class Ball:
    def __init__(self, pet):
        self.x = 0
        self.y = 0
        self.z = 0
        self.nx = 1
        self.ny = 1
        self.nz = 1
        self.r = 1
        self.ys = 1
        self.c = "magenta"
        pet.balls.append(self)

    def get_pos(b, i, n):
        x = b.x
        y = b.y
        z = b.z
        r = b.r / n
        if b.nx > 1: x += i * r
        if b.nx < -1: x -= i * r
        if b.ny > 1: y += i * r
        if b.ny < -1: y -= i * r
        if b.nz > 1: z += i * r
        if b.nz < -1: z -= i * r
        return x, y, z

class Pet:
    # name, bits, default
    bits = (
        ("behavior_primary", 3, 0),
        ("behavior_secondary", 3, 5),
        ("eye_count", 2, 2),
        ("eye_height", 4, 3),
        ("eye_space", 3, 3),
        ("eye_size", 3, 2),
        ("limb_count", 2, 1),
        ("limb_size", 3, 4),
        ("limb_n", 2, 1),
        ("nose_height", 4, 6),
        ("nose_size", 3, 4),
        ("nose_n", 2, 0),
        ("nose_color", 2, 3),
        ("nose_nostrils", 2, 2),
        ("ear_height", 4, 12),
        ("ear_size", 3, 4)
        )
    def __init__(self):
        self.name = "?"
        self.owner = 0
        self.pid = 0
        self.balls = []
        self.data = {}
        self.x = 0
        self.y = 0
        self.z = 0
        self.a = 0
        for name, bits, default in self.bits:
            self.data[name] = default

    def as_json(self):
        # we do not have the json module in transcrypt
        j = "{"
        for name, bits, default in self.bits: # we want it ordered
            value = self.data[name]
            if j != "{":
                j += ","
            j += '"' + name + '":'
            j += str(value)
        j += "}"
        return j

    def from_json(self, j):
        kv = re.findall("\"(.+?)\":(\\d+)", j)
        for k, v in kv:
            self.data[k] = int(v) # all values must be int

    def get_primary(self): return characters[self.data["behavior_primary"]]
    def get_secondary(self): return characters[self.data["behavior_secondary"]]
    
    def get_eye_count(self): return self.data["eye_count"]
    def get_eye_height(self): return (self.data["eye_height"] - 3) * math.pi / -32
    def get_eye_space(self): return (self.data["eye_space"] + 2) * math.pi / 32
    def get_eye_size(self): return 0.125 + self.data["eye_size"] * 2 / 32
    
    def get_limb_count(self): return 2 + self.data["limb_count"] * 2
    def get_limb_size(self): return 1 / 6 + self.data["limb_size"] / 20
    def get_limb_n(self): return 1 + self.data["limb_n"]
    
    def get_nose_size(self): return self.data["nose_size"] / 12
    def get_nose_n(self): return 1 + self.data["nose_n"]
    def get_nose_height(self): return (self.data["nose_height"] - 12) * math.pi / -32
    def get_nose_color(self): return ["fur", "dark", "bright", "pink"][self.data["nose_color"]]
    def get_nose_nostrils(self): return self.data["nose_nostrils"]

    def get_ear_height(self): return (self.data["ear_height"] - 4) * math.pi / -32
    def get_ear_size(self): return self.data["ear_size"] / 8

    def attach(pet, parent, lat, lon, radius, color, kw = {}):
        b = Ball(pet)
        b.x = math.sin(lon) * parent.r
        b.y = -math.cos(lon) * parent.r
        b.z = math.sin(lat) * parent.r
        b.x *= math.cos(lat)
        b.y *= math.cos(lat)
        b.y *= parent.ys
        b.x += parent.x
        b.y += parent.y
        b.z += parent.z
        b.r = radius
        b.c = color
        if "ys" in kw: b.ys = kw["ys"]
        if "nx" in kw: b.nx = kw["nx"]
        if "ny" in kw: b.ny = kw["ny"]
        if "nz" in kw: b.nz = kw["nz"]
        return b


    def make_balls(pet):
        pet.balls.clear()

        color_a = characters.index(pet.get_primary())
        color_b = characters.index(pet.get_secondary())
        color = colors[color_a * 8 + color_b]

        body = Ball(pet)
        body.c = color
        head = pet.attach(body, -math.pi / 2, 0, 1, color) 

        lat = pet.get_eye_height()
        lon = pet.get_eye_space() 
        es = pet.get_eye_size()
        if pet.get_eye_count() >= 2:
            eye1 = pet.attach(head, lat, lon, es, "white", {"ys" : 0.5})
            pet.attach(eye1, 0, 0, es * 3 / 4, "black", {"ys": 0.25})
            eye2 = pet.attach(head, lat, -lon, es, "white", {"ys" : 0.5})
            pet.attach(eye2, 0, 0, es * 3 / 4, "black", {"ys": 0.25})
        if pet.get_eye_count() == 1 or pet.get_eye_count() == 3:
            eye3 = pet.attach(head, lat, 0, es, "white", {"ys" : 0.5})
            pet.attach(eye3, 0, 0, es * 3 / 4, "black", {"ys": 0.25})

        limb_n = pet.get_limb_n()
        limb_size = pet.get_limb_size()
        limb_size *= limb_n
        if pet.get_limb_count() >= 2:
            pet.attach(body, 0, math.pi / 2, limb_size, color,  {"nx": limb_n})
            pet.attach(body, 0, -math.pi / 2, limb_size, color, {"nx": -limb_n})
        leg_lat = math.pi / 2 * 0.7
        if pet.get_limb_count() == 4 or pet.get_limb_count() == 8:
            pet.attach(body, leg_lat, math.pi / 2, limb_size, color, {"nz": limb_n})
            pet.attach(body, leg_lat, -math.pi / 2, limb_size, color, {"nz": limb_n})
        if pet.get_limb_count() == 6 or pet.get_limb_count() == 8:
            pet.attach(body, leg_lat, math.pi / 2 * 0.3, limb_size, color, {"nz": limb_n})
            pet.attach(body, leg_lat, -math.pi / 2 * 0.3, limb_size, color, {"nz": limb_n})

            pet.attach(body, leg_lat, math.pi / 2 * 1.7, limb_size, color, {"nz": limb_n})
            pet.attach(body, leg_lat, -math.pi / 2 * 1.7, limb_size, color, {"nz": limb_n})

        nose_size = pet.get_nose_size()
        nose_n = pet.get_nose_n()
        nose_size *= nose_n
        if nose_size > 0:
            ncol = color
            if pet.get_nose_color() == "pink": ncol = "pink"
            if pet.get_nose_color() == "dark":
                ncol = colors[7 * 8 + color_a]
            if pet.get_nose_color() == "bright":
                ncol = colors[6 * 8 + color_a]
            nose = pet.attach(head, pet.get_nose_height(), 0, nose_size, ncol, {"ny": -nose_n})
            s = nose_size / nose_n / 3
            if pet.get_nose_nostrils() == 1: pet.attach(nose, 0, 0, s, "black")
            if pet.get_nose_nostrils() >= 2:
                pet.attach(nose, 0, pi / 8 / nose_n, s, "black")
                pet.attach(nose, 0, pi / -8 / nose_n, s, "black")
            if pet.get_nose_nostrils() == 3:
                pet.attach(nose, -pi / 8 / nose_n, 0, s, "black")

        if pet.get_ear_size() > 0:
            es = pet.get_ear_size()
            eh = pet.get_ear_height()
            pet.attach(head, eh, pi / 2 * 1.2, es, color, {"ys": 0.75})
            pet.attach(head, eh, -pi / 2 * 1.2, es, color, {"ys": 0.75})

        
    def draw_y(pet, c, ox, oy, s, a):
        c.translate(ox, oy)
        c.rotate(a * math.pi / 180)
        for b in sorted(pet.balls, key = lambda x: -x.y):
            n = max(abs(b.nx), abs(b.ny), abs(b.nz))
            r = b.r / n
            for i in range(n):
                x, y, z = b.get_pos(i, n)
                pet.circle(c, b.c, x * s, z * s, r * s, r * s)
        c.setTransform(1, 0, 0, 1, 0, 0)

    def draw_z(pet, c, ox, oy, s, a):
        c.translate(ox, oy)
        c.rotate(a * math.pi / 180)
        c.scale(s, s)
        for b in sorted(pet.balls, key = lambda x: -x.z * 1000 + x.x + x.y):
            n = max(abs(b.nx), abs(b.ny), abs(b.nz))
            r = b.r / n
            for i in range(n):
                x, y, z = b.get_pos(i, n)
                pet.circle(c, b.c, x, - y, r, r * b.ys)
        c.setTransform(1, 0, 0, 1, 0, 0)

    def draw_x(pet, c, ox, oy, s, a):
        c.translate(ox, oy)
        c.rotate(a * math.pi / 180)
        for b in sorted(pet.balls, key = lambda x: x.x):
            n = max(abs(b.nx), abs(b.ny), abs(b.nz))
            r = b.r / n
            for i in range(n):
                x, y, z = b.get_pos(i, n)
                pet.circle(c, b.c, - y * s, z * s, r * b.ys * s, r * s)
        c.setTransform(1, 0, 0, 1, 0, 0)

    def circle(pet, c, color, x, y, rx, ry):
        c.fillStyle = color
        #c.strokeStyle = color
        c.beginPath()
        c.ellipse(x, y, rx, ry, 0, 0, math.pi * 2)
        c.fill()
        #c.stroke()

colors = [
        "crimson",  "orange",       "olive",    "silver",       "hotpink",     "darksalmon",   "pink",     "maroon",
        "darkorange","gold",        "greenyellow","cornsilk",   "tan",          "peachpuff",    "yellow",   "darkgoldenrod",
        "indianred","yellowgreen",  "limegreen","seagreen",     "cyan",         "thistle",      "springgreen",     "darkgreen",
        "salmon",   "springgreen",  "aquamarine",     "paleturquoise","skyblue", "lavender",    "azure",     "teal",
        "slateblue","cornsilk",     "paleturquoise",     "deepskyblue",  "dodgerblue",   "royalblue",    "lightskyblue",     "navy",
        "deeppink",  "burlywood",   "coral",     "beige",        "mediumpurple",         "orchid",       "plum",     "purple",
        "mistyrose","lemonchiffon", "honeydew", "mintcream",   "aliceblue",    "lavenderblush",         "white",    "gainsboro",
        "saddlebrown", "sienna",    "darkolivegreen","darkslategray",  "midnightblue",         "indigo","dimgray",     "black",
        ]
characters = ["fire", "electric", "nature", "ice", "water", "magic", "healer", "evil"]
