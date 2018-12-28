import htmltag
import login
from flask import session, escape, request
import database
import json

def init():
    global h
    global r
    r = ""
    def add(x):
        global r
        r += x + "\n"
    h = htmltag.Html(add)
    h.tag2("!DOCTYPE", html = "")
    h.tag2("meta", charset = "utf8")
    return h

def get_html():
    return r

def header():
    with h.tag("head"):
        title()
        style()

def title():
    with h.tag("title"):
        h.content("Krampus Hack 2018")

def client(run):
    with h.tag("script", type = "module", defer = ""):
        h.content("import * as client from \"./static/__target__/client.js\"; window.client = client;" + run)

def style():
    with h.tag("style"):
        h.style("body", background = "silver")
        h.style("canvas", **{"vertical-align" : "top"})
        h.style("div.block", display = "inline-block")
        h.style("div.left", display = "inline-block")
        h.style("a", **{"-webkit-appearance" : "button", "text-decoration": "none",
            "color": "initial"})
        h.style("p", width = "40em")
        h.style("input", margin = "0px")

def lab():
    init()

    dna = "{}"
    if "username" in session:
        username = session["username"]
        if username:
            # this should be asynchronous, but whatever
            database.access_db()
            dna = database.get_pet_dna(username)
    
    with h.tag("html"):
        with h.tag("head"):
            title()
            client("client.start_lab('" + dna + "');")
            style()
        with h.tag("body"):
            with h.tag("h1"):
                h.content("Lab")
            with h.tag("div.left"):
                editor()
            with h.tag("canvas", width = "512px", height = "512px"):
                h.content("here be dragons")
                
    return r

def editor():
    with h.tag("form", method = "post", action = "/save"):
        h.tag2("input", type = "hidden", name = "dna", id = "dna")
        h.tag2("input", type = "submit", value = "Back")
    with h.tag("h2"):
        h.content("DNA editing")
    with h.tag("h3"):
        h.content("Gene 1 (Behavior)")
        h.tag2("span", id = "g1")
    
    select("behavior_primary", "fire", "electric", "nature", "ice", "water", "magic", "healer", "evil")
    select("behavior_secondary", "fire", "electric", "nature", "ice", "water", "magic", "healer", "evil")
    with h.tag("h3"):
        h.content("Gene 2 (Eye)")
        h.tag2("span", id = "g2")
    select("eye_count", 0, 1, 2, 3)
    slider("eye_height", 15)
    slider("eye_space", 7)
    select("eye_size", 1, 2, 3, 4, 5, 6, 7, 8)
    with h.tag("h3"):
        h.content("Gene 3 (Limb)")
        h.tag2("span", id = "g3")
    select("limb_count", 2, 4, 6, 8)
    slider("limb_size", 7)
    select("limb_n", 1, 2, 3, 4)
    with h.tag("h3"):
        h.content("Gene 4 (Nose)")
        h.tag2("span", id = "g4")
    slider("nose_height", 15)
    slider("nose_size", 7)
    select("nose_n", 1, 2, 3, 4)
    select("nose_color", "fur", "dark", "bright", "pink")
    select("nose_nostrils", 0, 1, 2, 3)
    with h.tag("h3"):
        h.content("Gene 5 (Ear)")
        h.tag2("span", id = "g5")
    slider("ear_height", 15)
    slider("ear_size", 7)

def nopref(name):
    if "_" in name:
        x = name.find("_")
        return name[x + 1:]
    return name

def select(name, *args, **kw):
    with h.tag("div.block"):
        h.content(nopref(name))
        h.tag2("br")
        with h.tag("select", id = name, onchange = "client.draw_lab();"):
            for arg in args:
                option(arg)

def slider(name, v):
    with h.tag("div.block"):
        h.content(nopref(name))
        h.tag2("br")
        h.tag2("input", id = name, type = "range", min = 0, max = v, onchange = "client.draw_lab();")

def option(v):
    atts = {"value" : v}
    #if selected:
    #    atts["selected"] = "selected"
    with h.tag("option", **atts):
        h.content(v)

def arena():
    init()

    if "username" in session:
        username = session["username"]
        if username:
            database.access_db()
            database.enter_arena(username, username)
    
    with h.tag("html"):
        with h.tag("head"):
            title()
            client("client.start_arena(\"" + username + "\", \"" + username + "\");")
            style()
        with h.tag("body"):
            with h.tag("h1"):
                h.content("Arena")
            with h.tag("a", href = "/"):
                h.content("Back")
            with h.tag("canvas", width = "512px", height = "512px"):
                h.content("here be dragons")
    return r

def arena_post():
    name = request.form["name"]
    database.access_db()
    pets = database.get_dna_in_arena(name)
    return json.dumps(pets)

def main():
    init()
    with h.tag("html"):
        header()
        with h.tag("body"):
            with h.tag("h1"):
                h.content("Krampus Hack 2018")
            with h.tag("a", href = "/arena"):
                h.content("To Arena")
            with h.tag("a", href = "/lab"):
                h.content("To Lab")
            with h.tag("h2"):
                h.content("Multiplayer")
            username = login.get_username(h)
            if username:
                with h.tag("h3"):
                    h.content("Join Game")
                with h.tag("p"):
                    h.content("Join someone else's game if you know their name.")
                h.tag2("input", name = "player", value = "name of friend")
                with h.tag("button"): h.content("Join Game")
                with h.tag("h3"):
                    h.content("Start Game")
                with h.tag("p"):
                    h.content("Start a new game and tell other players to join " + username + ".")
                with h.tag("button"): h.content("Start Game")
            with h.tag("h2"):
                h.content("Happy Holidays Amarillion!")
            with h.tag("p"):
                h.content("""
In this game you play a mad <b>scientist</b> who discovered how to edit the genome of his magical pet. Initially a <b>cute animal</b> it soon is transformed into
a fighting beast battling monsters together with <b>multiple players</b>.
                """)
    return r

if __name__ == "__main__":
    print(main())
