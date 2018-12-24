#!/usr/bin/env python3
from contextlib import contextmanager

class Html:
    voids = """
    area
    base
    br
    col
    embed
    hr
    img
    input
    link
    meta
    param
    source
    track
    wbr
    !doctype
    """.split()
    
    def __init__(self, printer):
        self.printer = printer
        self.i = 0
    
    def write_tag(self, tag_name, close_it, **attributes):
        # "class" is a reserved python keyword so we provide an easier:
        # div.main is the same as <div class="main">
        if "." in tag_name:
            tag_name, class_name = tag_name.split(".", 1)
            class_name = class_name.replace(".", " ")
            attributes["class"] = class_name
        s = ""
        if attributes:
            for k, v in attributes.items():
                if v is not None and v != "":
                    s += " " + k + "=" + '"' + str(v) + '"'
                else:
                    s += " " + k
        if close_it:
            if tag_name.lower() in Html.voids:
                close = ">"
            else:
                close = "></" + tag_name + ">"
        else:
            close = ">"
        self.printer("<" + tag_name + s + close)
        return tag_name

    @contextmanager
    def tag(self, tag_name, **attributes):
        tag_name = self.write_tag(tag_name, False, **attributes)
        self.i += 1
        yield
        self.i -= 1
        self.printer("</" + tag_name + ">")

    def tag2(self, tag_name, **attributes):
        # since html5 no special / needed anymore
        self.write_tag(tag_name, True, **attributes)

    def style(self, element, **attributes):
        s = ""
        if attributes:
            for k, v in attributes.items():
                s += "    " + k + ": " + v + ";\n"
        self.printer(element + " {")
        self.printer(s + "}")

    def content(self, text):
        self.printer(str(text))

if __name__ == "__main__":
    # example use
    import html
    h = html.Html(lambda x: print(x))
    h.tag2("!DOCTYPE", html = "")
    h.tag2("meta", charset = "utf8")
    with h.tag("html"):
        with h.tag("head"):
            with h.tag("title"):
                h.content("I am the title")
            with h.tag("style"):
                h.style("h1", color = "red")
        with h.tag("body"):
            with h.tag("h1"):
                h.content("I am red")
            with h.tag("p.a.b.c"):
                h.content("Paragraph text.")
                h.tag2("br")
                with h.tag("a", href = "https://google.com"):
                    h.content("a link")
