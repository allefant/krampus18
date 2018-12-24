import math
pi = math.pi
c = None
balls = []
class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.nx = 1
        self.ny = 1
        self.nz = 1
        self.r = 1
        self.ys = 1
        self.c = "magenta"
        balls.append(self)

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

def redraw():
    global c
    canvas = document.getElementsByTagName("canvas")[0]
    w = canvas.width
    h = canvas.height
    c = canvas.getContext('2d')
    c.fillStyle = 'silver'
    c.fillRect(0, 0, w, h)
    c.strokeStyle = 'black'
    c.strokeRect(0, 0, w, h)

    cx = w / 2
    cy = h / 4

    balls.clear()

    color_a = characters.index(gets("primary"))
    color_b = characters.index(gets("secondary"))
    color = colors[color_a * 8 + color_b]

    body = Ball()
    body.c = color
    head = attach(body, -math.pi / 2, 0, 1, color) 

    eyes = get("eyes_count")
    lon = math.pi * get("eyes_space") / 32
    lat = math.pi * -get("eyes_height") / 32

    legs = get("legs_count")
    legs_n = get("legs_n")
    legs_size = 1 / 6 + (get("legs_size")) / 20
    legs_size *= legs_n

    nose_size = get("nose_size") / 12
    nose_n = get("nose_n")
    nose_size *= nose_n
   
    es = 0.125 + 0.125 * (get("eyes_size") - 1) * 3 / 8
    if eyes >= 2:
        eye1 = attach(head, lat, lon, es, "white", {"ys" : 0.5})
        attach(eye1, 0, 0, es * 3 / 4, "black", {"ys": 0.25})
        eye2 = attach(head, lat, -lon, es, "white", {"ys" : 0.5})
        attach(eye2, 0, 0, es * 3 / 4, "black", {"ys": 0.25})
    if eyes == 1 or eyes == 3:
        eye3 = attach(head, lat, 0, es, "white", {"ys" : 0.5})
        attach(eye3, 0, 0, es * 3 / 4, "black", {"ys": 0.25})

    if legs >= 2:
        attach(body, 0, math.pi / 2, legs_size, color,  {"nx": legs_n})
        attach(body, 0, -math.pi / 2, legs_size, color, {"nx": -legs_n})
    leg_lat = math.pi / 2 * 0.7
    if legs == 4 or legs == 8:
        attach(body, leg_lat, math.pi / 2, legs_size, color, {"nz": legs_n})
        attach(body, leg_lat, -math.pi / 2, legs_size, color, {"nz": legs_n})
    if legs == 6 or legs == 8:
        attach(body, leg_lat, math.pi / 2 * 0.3, legs_size, color, {"nz": legs_n})
        attach(body, leg_lat, -math.pi / 2 * 0.3, legs_size, color, {"nz": legs_n})

        attach(body, leg_lat, math.pi / 2 * 1.7, legs_size, color, {"nz": legs_n})
        attach(body, leg_lat, -math.pi / 2 * 1.7, legs_size, color, {"nz": legs_n})

    if nose_size > 0:
        ncol = color
        if gets("nose_color") == "pink": ncol = "pink"
        if gets("nose_color") == "dark":
            ncol = colors[7 * 8 + color_a]
        if gets("nose_color") == "bright":
            ncol = colors[6 * 8 + color_a]
        nose = attach(head, pi * -get("nose_height") / 32, 0, nose_size, ncol, {"ny": -nose_n})
        s = nose_size / nose_n / 3
        if get("nostrils") == 1: attach(nose, 0, 0, s, "black")
        if get("nostrils") >= 2:
            attach(nose, 0, pi / 8 / nose_n, s, "black")
            attach(nose, 0, pi / -8 / nose_n, s, "black")
        if get("nostrils") == 3:
            attach(nose, -pi / 8, 0, s, "black")

    if get("ear_size") > 0:
        attach(head, -get("ear_height") * pi / 32, pi / 2 * 1.2, get("ear_size") / 8, color, {"ys": 0.75})
        attach(head, -get("ear_height") * pi / 32, -pi / 2 * 1.2, get("ear_size") / 8, color, {"ys": 0.75})
 
    s = 0.2
    draw_y(w / 4, h / 4, 0.5 * w * s)
    draw_z(w * 3 / 4, h / 4, 0.5 * w * s)
    draw_x(w / 4, h * 3 / 4, 0.5 * w * s)

    encode()

def encode():

    color_a = characters.index(gets("primary"))
    color_b = characters.index(gets("secondary"))
    code = [(color_a, 3), (color_b, 3)]
    set_code("g1", code)

    code = [(get("eyes_count"), 2),
        (get("eyes_height") + 3, 4),
        (get("eyes_space") - 2, 3),
        (get("eyes_size") - 1, 3)]
    set_code("g2", code)

    code = [(getindex("legs_count"), 2),
        (get("legs_size"), 3),
        (get("legs_n") - 1, 2)]
    set_code("g3", code)

    code = [
        (get("nose_height") + 12, 4),
        (get("nose_size"), 3),
        (get("nose_n") - 1, 2),
        (getindex("nose_color"), 2),
        (get("nostrils"), 2)]
    set_code("g4", code)

    code = [
        (get("ear_height") + 4, 4),
        (get("ear_size"), 3)]
    set_code("g5", code)

def set_code(name, codes):
    code = 0
    bits = 0
    for c, b in codes:
        code += c << bits
        bits += b
    letters = ["<b style='color:red'>A</b>",
        "<b style='color:green'>G</b>",
        "<b style='color:blue'>C</b>",
        "<b style='color:yellow'>T</b>"]

    dna = ""
    for i in range((bits + 1) // 2):
        dna += letters[(code >> (2 * i)) & 3]
    g = document.getElementById(name)
    g.innerHTML = dna

def attach(parent, lat, lon, radius, color, kw = {}):
    b = Ball()
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

def draw_y(ox, oy, s):
    for b in sorted(balls, key = lambda x: -x.y):
        n = max(abs(b.nx), abs(b.ny), abs(b.nz))
        r = b.r / n
        for i in range(n):
            x, y, z = get_pos(b, i, n)
            circle(b.c, ox + x * s, oy + z * s, r * s, r * s)

def draw_z(ox, oy, s):
    for b in sorted(balls, key = lambda x: -x.z):
        n = max(abs(b.nx), abs(b.ny), abs(b.nz))
        r = b.r / n
        for i in range(n):
            x, y, z = get_pos(b, i, n)
            circle(b.c, ox + x * s, oy - y * s, r * s, r * b.ys * s)

def draw_x(ox, oy, s):
    for b in sorted(balls, key = lambda x: x.x):
        n = max(abs(b.nx), abs(b.ny), abs(b.nz))
        r = b.r / n
        for i in range(n):
            x, y, z = get_pos(b, i, n)
            circle(b.c, ox - y * s, oy + z * s, r * b.ys * s, r * s)

def circle(color, x, y, rx, ry):
    c.fillStyle = color
    #c.strokeStyle = color
    c.beginPath()
    c.ellipse(x, y, rx, ry, 0, 0, math.pi * 2)
    c.fill()
    #c.stroke()

def get(elem):
    return int(document.getElementById(elem).value)
    
def gets(elem):
    return document.getElementById(elem).value

def getindex(elem):
    return document.getElementById(elem).selectedIndex

redraw()
