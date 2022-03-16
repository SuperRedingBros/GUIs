from .colors import *
from colors import *
from typing import Any

__doc__="""

Guis

"""

def modint(interpreterdata, mods) -> None: ...
def init(modules) -> None: ...

renderer: str
darktext: str
seetext: str
intext: str
dw: int
dh: int
usefull: bool
internalkeyboard: bool
fontsize: int
gameDisplay: Any
s: Any
screendict: Any
randid: int
frame: bool

def clamp(num, min_value, max_value): ...
def rot_center(image, rect, angle): ...

drawx: int
drawy: int

def testinput(eventname, event, surface, globals) -> None: ...

class widget:
    def draworign(self, surfacein) -> None: ...
    def vfill(self): ...
    def hfill(self): ...
    def vfitchildren(self): ...
    cw: Any
    def hlargest(self): ...
    def hfitchildren(self): ...
    ch: Any
    def vlargest(self): ...
    def getstyle(self, key): ...
    mh: Any
    h: Any
    mw: Any
    w: Any
    angle: Any
    color: Any
    activecolor: Any
    inactivecolor: Any
    background: Any
    text: Any
    wrap: Any
    image: Any
    img: Any
    justification: Any
    fillnum: Any
    round: Any
    border: str
    padding: Any
    margin: Any
    slideminx: Any
    slidemaxx: Any
    slideminy: Any
    slidemaxy: Any
    slideh: Any
    slideho: Any
    slidew: Any
    slidewo: Any
    def styleize(self, style) -> None: ...
    def calc(self, input: str = ...): ...
    changed: bool
    def update(self) -> None: ...
    def prossesinputs(self, eventname, event, surface, globals) -> None: ...
    def drawBorder(self, surfacein) -> None: ...
    def redraw(self, surfacein, last) -> None: ...
    my: int
    mx: int
    y: int
    x: int
    children: Any
    child: str
    sibling: str
    parent: Any
    surface: Any
    frame: bool
    style: Any
    parentref: Any
    notifys: Any
    pygame: Any
    def __init__(self, id, parent: str = ..., style=...) -> None: ...

class mainWidget(widget):
    def prossesinputs(self, eventname, event, surface) -> None: ...
    def redraw(self, surfacein, last) -> None: ...
    x: int
    y: int
    w: int
    h: int
    id: str
    pygame: Any
    children: Any
    style: Any
    mainbackground: Any
    color: Any
    globals: Any
    changed: bool
    def __init__(self, pygame, background: str = ..., globals=..., style=...) -> None: ...

class textWidget(widget):
    def redraw(self, surfacein, last) -> None: ...
    parentref: Any
    font: Any
    changed: bool
    x: Any
    y: Any
    h: Any
    w: Any
    id: Any
    textRect: Any
    justification: str
    draws: int
    style: Any
    background: Any
    def __init__(self, id=..., parent: str = ..., x: int = ..., y: int = ..., fontsize: int = ..., background: str = ..., style=...) -> None: ...

class progressWidget(widget):
    changed: bool
    def redraw(self, surfacein, last) -> None: ...
    parentref: Any
    font: Any
    x: Any
    y: Any
    h: Any
    w: Any
    id: Any
    draws: int
    def __init__(self, id=..., parent: str = ..., x: int = ..., y: int = ..., style=...) -> None: ...

class vlistWidget(widget):
    ch: int
    cw: int
    def redraw(self, surfacein, last) -> None: ...
    font: Any
    changed: bool
    x: Any
    y: Any
    h: int
    w: int
    id: Any
    def __init__(self, id=..., parent: str = ..., x: int = ..., y: int = ..., style=...) -> None: ...

class hlistWidget(widget):
    cw: int
    ch: int
    def redraw(self, surfacein, last) -> None: ...
    font: Any
    changed: bool
    x: int
    y: int
    h: int
    w: int
    id: Any
    style: Any
    def __init__(self, id=..., parent: str = ..., style=...) -> None: ...

class buttonWidget(widget):
    mouseover: bool
    changed: bool
    ispressing: bool
    def prossesinputs(self, eventname, event, surface, globals) -> None: ...
    def redraw(self, surfacein, last) -> None: ...
    font: Any
    draws: int
    x: int
    y: int
    h: Any
    w: Any
    id: Any
    action: Any
    style: Any
    def __init__(self, id=..., parent: str = ..., action: str = ..., style=...) -> None: ...

class surfaceWidget(widget):
    def prossesinputs(self, eventname, event, surface, globals) -> None: ...
    def redraw(self, surfacein, last) -> None: ...
    name: Any
    x: Any
    y: Any
    w: Any
    h: Any
    parentref: Any
    mysurface: Any
    pygame: Any
    parent: Any
    color: Any
    def __init__(self, name, x, y, w, h, parent, color: str = ..., surface: str = ..., style=...) -> None: ...

class textBoxWidget(widget):
    def textbox(self, num): ...
    active: bool
    def activate(self) -> None: ...
    mouseover: bool
    changed: bool
    ispressing: bool
    mytext: Any
    def prossesinputs(self, eventname, event, surface, globals) -> None: ...
    textRect: Any
    def redraw(self, surfacein, last) -> None: ...
    font: Any
    draws: int
    x: Any
    y: Any
    h: Any
    w: Any
    id: Any
    color: Any
    activecolor: Any
    inactivecolor: Any
    action: str
    text: Any
    helptext: Any
    def __init__(self, id=..., parent: str = ..., x: int = ..., y: int = ..., color: str = ..., activecolor: str = ..., textcolor: str = ..., text: str = ..., helptext: str = ..., style=...) -> None: ...

class sliderWidget(widget):
    sliderx: Any
    slidery: Any
    mouseover: bool
    ispressing: bool
    def prossesinputs(self, eventname, event, surface, globals) -> None: ...
    changed: bool
    def redraw(self, surfacein, last) -> None: ...
    font: Any
    draws: int
    x: Any
    y: Any
    slideminx: int
    slideminy: int
    slidemaxx: int
    slidemaxy: int
    slidew: int
    slideh: int
    slidewo: int
    slideho: int
    h: Any
    w: Any
    id: Any
    action: str
    def __init__(self, id=..., parent: str = ..., x: int = ..., y: int = ..., action: Any | None = ..., style=...) -> None: ...

class checkWidget(widget):
    active: Any
    def activate(self) -> None: ...
    mouseover: bool
    changed: bool
    ispressing: bool
    def prossesinputs(self, eventname, event, surface, globals) -> None: ...
    img: Any
    def redraw(self, surfacein, last) -> None: ...
    font: Any
    draws: int
    h: Any
    w: Any
    id: Any
    action: str
    style: Any
    def __init__(self, id=..., parent: str = ..., style=...) -> None: ...

class selectWidget(widget):
    def redraw(self, surfacein, last) -> None: ...
    x: int
    y: int
    w: int
    h: int
    condition: Any
    def __init__(self, id, parent, condition: str = ..., style=...) -> None: ...

class imageWidget(widget):
    def redraw(self, surfacein, last) -> None: ...
    font: Any
    draws: int
    changed: bool
    h: Any
    w: Any
    id: Any
    ispressing: bool
    mouseover: bool
    active: bool
    def __init__(self, id=..., parent: str = ..., style=...) -> None: ...

class overlaywidget(widget):
    changed: bool
    def redraw(self, surfacein, last) -> None: ...

path: Any
sourcepath: Any

def DrawBorder(x, y, w, h, t, color) -> None: ...
def DrawText(text, x, y, font, color) -> None: ...
def Font(fontFace, size): ...
def renderdraw(param) -> None: ...
def hello() -> None: ...

smallFont: Any
mediumFont: Any
largeFont: Any
hugeFont: Any
dynamicFont: Any
dynamicFontS: Any
dynamicFontL: Any

def RedrawDelagate() -> None: ...

ispressing: bool

def Button(text, x, y, w, h, inactivecolor, activecolor, alttext, action: Any | None = ..., font=...) -> None: ...

gchr: str

def keyButton(text, x, y, w, h, inactivecolor, activecolor, alttext: str = ..., font=...) -> None: ...

looping: bool

def renderframe(events, display, skipevents: bool = ..., screen: Any | None = ...) -> None: ...
def render() -> None: ...

variablestr: str
img_file: Any
variabletest: int

def truncline(text, font, maxwidth): ...
def wrapline(text, font, maxwidth): ...
