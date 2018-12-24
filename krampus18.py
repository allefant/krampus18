import htmltag
import login
from flask import session, escape

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
        with h.tag("title"):
            h.content("Krampus Hack 2018")
        with h.tag("script", type = "module", defer = ""):
            h.content("import * as lab from \"./static/__target__/lab.js\"; window.lab = lab;")
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
    with h.tag("html"):
        header()
        with h.tag("body"):
            with h.tag("h1"):
                h.content("Lab")
            with h.tag("div.left"):
                editor()
            with h.tag("canvas", width = "512px", height = "512px"):
                h.content("here be dragons")
    return r

def editor():
    with h.tag("a", href = "/"):
        h.content("Back")
    with h.tag("a", href = "/arena"):
        h.content("To Arena")
    with h.tag("h2"):
        h.content("DNA editing")
    with h.tag("h3"):
        h.content("Gene 1 (Behavior)")
        h.tag2("span", id = "g1")
    #with h.tag("table"):
    #    for j in range(8):
    #        with h.tag("tr"):
    #            for i in range(8):
    #                with h.tag("td", style = "background:" + colors[i + j * 8]):
    #                    h.content(colors[i + j * 8][:8])
    select("primary", "fire", "electric", "nature", "ice", "water", "magic", "healer", "evil", default = "fire")
    select("secondary", "fire", "electric", "nature", "ice", "water", "magic", "healer", "evil", default = "magic")
    with h.tag("h3"):
        h.content("Gene 2 (Eye)")
        h.tag2("span", id = "g2")
    select("eyes_count", 0, 1, 2, 3, default = 2)
    slider("eyes_height", -3, 12, default = 0)
    slider("eyes_space", 2, 9, default = 5)
    select("eyes_size", 1, 2, 3, 4, 5, 6, 7, 8, default = 4)
    with h.tag("h3"):
        h.content("Gene 3 (Limb)")
        h.tag2("span", id = "g3")
    select("legs_count", 2, 4, 6, 8, default = 4)
    slider("legs_size", 0, 7, default = 3)
    select("legs_n", 1, 2, 3, 4, default = 2)
    with h.tag("h3"):
        h.content("Gene 4 (Nose)")
        h.tag2("span", id = "g4")
    slider("nose_height", -12, 3, default = -3)
    slider("nose_size", 0, 7, default = 4)
    select("nose_n", 1, 2, 3, 4, default = 1)
    select("nose_color", "fur", "dark", "bright", "pink", default = "pink")
    select("nostrils", 0, 1, 2, 3, default = 2)
    with h.tag("h3"):
        h.content("Gene 5 (Ear)")
        h.tag2("span", id = "g5")
    slider("ear_height", -4, 11, default = 8)
    slider("ear_size", 0, 7, default = 4)

def nopref(name):
    if "_" in name:
        x = name.find("_")
        return name[x + 1:]
    return name

def select(name, *args, **kw):
    with h.tag("div.block"):
        h.content(nopref(name))
        h.tag2("br")
        with h.tag("select", id = name, onchange = "lab.redraw();"):
            for arg in args:
                option(arg, arg == kw.get("default", None))

def slider(name, v1, v2, default):
    with h.tag("div.block"):
        h.content(nopref(name))
        h.tag2("br")
        h.tag2("input", id = name, type = "range", min = v1, max = v2, value = default, onchange = "lab.redraw();")

def option(v, selected = False):
    atts = {"value" : v}
    if selected:
        atts["selected"] = "selected"
    with h.tag("option", **atts):
        h.content(v)

def arena():
    init()
    with h.tag("html"):
        header()
        with h.tag("body"):
            with h.tag("h1"):
                h.content("Arena")
            with h.tag("a", href = "/"):
                h.content("Back")
            with h.tag("a", href = "/lab"):
                h.content("To Lab")
    return r

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
