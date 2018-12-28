import math
from pet import Ball, colors, characters, Pet
pi = math.pi

def start(dna):
    pet = Pet()
    pet.from_json(dna)
    update_form(pet)
    redraw()

def redraw():
    canvas = document.getElementsByTagName("canvas")[0]
    w = canvas.width
    h = canvas.height
    c = canvas.getContext('2d')

    pet = read_pet_from_form()

    pet.make_balls()

    dna = document.getElementById("dna")
    dna.value = pet.as_json()

    c.fillStyle = 'silver'
    c.fillRect(0, 0, w, h)
    c.strokeStyle = 'black'
    c.strokeRect(0, 0, w, h)

    cx = w / 2
    cy = h / 4
 
    s = 0.2
    pet.draw_y(c, w / 4, h / 4, 0.5 * w * s)
    pet.draw_z(c, w * 3 / 4, h / 4, 0.5 * w * s)
    pet.draw_x(c, w / 4, h * 3 / 4, 0.5 * w * s)

    encode(pet)

def read_pet_from_form():
    pet = Pet()
    for name, bits, value in pet.bits:
        pet.data[name] = get(name)
        #console.log(name, pet.data[name])
    return pet

def update_form(pet):
    for name, bits, value in pet.bits:
        update(name, pet.data[name])

def encode(pet):
    set_code(pet, "g1", 0, 2)
    set_code(pet, "g2", 2, 6)
    set_code(pet, "g3", 6, 9)
    set_code(pet, "g4", 9, 14)
    set_code(pet, "g5", 14, 16)

def set_code(pet, name, ca, cb):
    code = 0
    bits = 0
    for cname, b, cdef in pet.bits[ca:cb]:
        c = pet.data[cname]
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

def get(elem):
    tag = document.getElementById(elem)
    if tag.nodeName == "SELECT":
        return tag.selectedIndex
    return int(tag.value)

def update(elem, value):
    tag = document.getElementById(elem)
    if tag.nodeName == "SELECT":
        tag.selectedIndex = value
    else:
        tag.value = value
