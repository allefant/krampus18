import pet
import lab
import arena

def start_lab(dna):
    lab.start(dna)

def draw_lab():
    lab.redraw()

def start_arena(who, whose):
    arena.begin_animation(who, whose)
