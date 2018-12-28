from pet import Pet

class State:
    def __init__(self):
        self.start = None
        self.t = 0
FPS = 20
state = State()

pets = []

def redraw():
    canvas = document.getElementsByTagName("canvas")[0]
    w = canvas.width
    h = canvas.height
    c = canvas.getContext('2d')
    c.fillStyle = 'silver'
    c.fillRect(0, 0, w, h)
    c.strokeStyle = 'black'
    c.strokeRect(0, 0, w, h)

    c.fillStyle = "yellow"
    x = state.t * w / FPS / 10
    y = 0
    c.fillRect(x, y, w / 16, h / 16)

    for pet in pets:
        pet.draw_y(c, x, y, w / 16) 

def step(timestamp):
    if not state.start:
        state.start = timestamp
        state.t = 0
    progress = timestamp - state.start
    if progress >= state.t * 1000 / FPS:
        redraw()
        state.t += 1
    
    window.requestAnimationFrame(step)

def begin_animation(who, whose):
    canvas = document.getElementsByTagName("canvas")[0]

    r = __new__(XMLHttpRequest())
    def onreadystatechange():
        if r.readyState == 4 and r.status == 200:
            window.requestAnimationFrame(step)
            j = JSON.parse(r.responseText)
            pet = Pet()
            pet.name = j[0][0]
            pet.from_json(j[0][1])
            pet.make_balls()
            pets.append(pet)
    r.onreadystatechange = onreadystatechange
    r.open("POST", "/arena")
    r.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
    r.send("name=" + whose)

