from html.parser import HTMLParser

try:
    from . import guis
    from . import css
except:
    import guis
    import css

import pygame
pygame.init()
from pygame.locals import *
import js2py

#add = js2py.eval_js('hello()')

def hello():
    print("Hello")

class document(object):
    def getElementById(self,id):
        return screen.find(id)

javascript = js2py.EvalJs({})


# Renderer
dw = 980
dh = 980
usefull = False
fontsize = 32
drawx = 0
drawy = 0
draw = 0

# Setup Screen

def setup(display):
    global gameDisplay
    gameDisplay = display

if __name__ == '__main__':
    if usefull:
        gameDisplay = pygame.display.set_mode((dw, dh), pygame.FULLSCREEN,pygame.RESIZABLE )
        s = pygame.display.get_window_size()
        dw = s[0]
        dh = s[1]
    else:
        gameDisplay = pygame.display.set_mode((dw, dh),pygame.RESIZABLE)
    s = pygame.display.get_window_size()
    dw = s[0]
    dh = s[1]
    pygame.display.set_caption('GUI Tests')


gdata = []
gattrs = []

parent =""
parents =""
screen =""

inloop = False
looping = True


# elementlists
"""
    <hr> line like this ------------------------------------------
    <ol> ordered list
    <video> video player
    <abbr> Mabye
    <bdo> Maybe
    <input>
    <label>
    <map>
    <select>
    <sub>
    <sup>
    <textarea>

"""

parenttype = ""

textlist = ("p","li","span")
smalllist = ("small","micro")
notextlist = ("script","title")
newlines = ("break","br")
noformatlist = ("pre","code","kbd","samp")
fields = ("fieldset","ZMSJJS")
headings = ("h6","h5","h4","h3","h2","h1")
italics = ("address","cite","em","i")
vlistlist = ("body","div","ul","ol","article",
"aside","dl","figure","footer","form"
"header","main","section","table","tfoot")
hlistlist = ("nav","hlist","dt","figcaption","dfn")
images = ("img","image")
links = ("a","filelink")
scripts = ("script","python")
canvases = ("canvas","drawcanvas")
dd = ["dd"]
buttons = ("button","inputbutton")
bold = ("b","strong")
quotes = ("q","quote")

class linkWidget(guis.widget):
    def link(self):
        openfile(self.data["href"])

    def prossesinputs(self,eventname,event,surface,globals):
        super(linkWidget,self).prossesinputs(eventname,event,surface,globals)
        if eventname == "Mousemove":
            ex = event.pos[0]
            ey = event.pos[1]
            #print(event.pos)
            #print((self.x,self.y,self.w,self.changed) )
            #print(self)
            o = surface.get_abs_offset()
            #print(o)
            if self.x+self.w+o[0] > ex > self.x+o[0] and self.y+self.changed+o[1] > ey > self.y+o[1]:
                #print("HI")
                self.mouseover = True
                self.changed = True
            else:
                if self.changed:
                    self.changed = True
                self.mouseover = False
        elif eventname == "Mousedown" and self.mouseover:
            if not self.ispressing:
                #print("Action"+str(self.action))
                self.link()
            self.ispressing = True
        elif eventname == "Mouseup":
            self.ispressing = False
        elif eventname == "Mouseleave":
            self.ispressing = False

    """A Button Widget"""

    def __init__(self,id=guis.randid,parent="main",action="",style={},data={}):
        self.action = action
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()",
        "Background":"self.dbackground"
        }
        super(linkWidget, self).__init__(id,parent,style,data)
        self.dbackground = self.inactivecolor

def render():
    global inloop
    inloop = True
    global looping
    while looping:
        global variablestr
        global variabletest
        clock.tick(60)
        renderframe( pygame.event.get(),gameDisplay,False,screen )
        screen.update()
        pygame.display.update()
        pygame.event.pump()

def renderframe(events,display,skipevents=False,screen=None):
    #print("frame")
    global dw
    global dh
    global looping
    if not skipevents:
        for event in events:
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.KEYDOWN:
                screen.prossesinputs("Keydown",event,display)
                if event.key == K_3:
                    print([screen])
            if event.type == pygame.KEYUP:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.prossesinputs("Mousedown",event,display)
            if event.type == pygame.MOUSEMOTION:
                screen.prossesinputs("Mousemove",event,display)
            if event.type == pygame.MOUSEBUTTONUP:
                screen.prossesinputs("Mouseup",event,display)
            if event.type == pygame.FINGERDOWN:
                pass
            if event.type == pygame.FINGERUP:
                pass
            if event.type == pygame.VIDEORESIZE:
                s = pygame.display.get_window_size()
                dw = s[0]
                dh = s[1]
                display.fill((0,0,0))
                pygame.display.update()
            if  event.type == WINDOWLEAVE:
                screen.prossesinputs("Mouseleave",event,display,globals())
    screen.redraw(display,"none")
    #pygame.display.update()

def openfile(file):
    file = open(file,"r")
    #print(globals())
    #print(file)
    parser = GUIsHTMLParser()
    if "screen" in globals():
        screen.children = []
    if "parent" in globals():
        parent.children = []
    if "parents" in globals():
        parents = []
    treepointer = []
    parser.feed(file.read())
    if not inloop:
        render()
    #render()

def dictify(list):
    out = {}
    for x in list:
        out[x[0]] = x[1]
    return out

class GUIsHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print(tag)
        global gattrs
        global parent
        global lparent
        global parenttype
        gattrs = attrs
        attrs = dictify(gattrs)
        cssstyle = {}
        parenttype = tag
        lparent = parent
        add = True
        if "id" in attrs:
            id = attrs["id"]
        else:
            id = tag
        if "style" in attrs:
            cssstyle = css.csstodict(attrs["style"])
        if "width" in attrs:
            cssstyle["W"] = attrs["width"]
        if "height" in attrs:
            cssstyle["H"] = attrs["height"]
        if tag in links:
            style = {
            "Background":"None",
            "ActiveColor":"blue",
            "InactiveColor":"lblue"
            }
            style.update(cssstyle)
            parent = linkWidget(
            id=tag, action="self.link()",
            parent=parent,style=style,
            data=attrs)
            style = {"Text":"self.parentref.data['Text']","Color":"self.parentref.dbackground"}
            style.update(cssstyle)
            #print(attrs)
            t = guis.textWidget(id=id, parent=parent,style=style,data=attrs)
            #print(t.style)
        if tag in vlistlist:
            style = {}
            style.update(cssstyle)
            parent = guis.vlistWidget(id=id, parent=parent,style=style)
        if tag in hlistlist:
            style = {}
            style.update(cssstyle)
            parent = guis.hlistWidget(id=id, parent=parent,style=style)
        if tag in fields:
            style = {"Border":{
            "color":"black",
            "width":2,
            "round":1
            }
            }
            style.update(cssstyle)
            parent = guis.vlistWidget(id=id, parent=parent,style=style)
        if tag in textlist:
            style = {}
            style.update(cssstyle)
            parent = guis.wraplistWidget(id=id,parent=parent,style=style,data=attrs,wrapwidth=dw)
        if tag == "blockquote":
            style = {"Padding":(32,0,0,0)}
            style.update(cssstyle)
            parent = guis.wraplistWidget(id=id,parent=parent,style=style,data=attrs)
        if tag in smalllist:
            style = {"Font":{
            "File":"./assets/Xolonium-Bold.ttf",
            "Scale":10,
            "Italics":False,
            "Underline":False
            }}
            style.update(cssstyle)
            parent = guis.wraplistWidget(id=id,parent=parent,style=style,data=attrs)
        if tag in newlines:
            style = {"Text":"","Color":"black"}
            attrs["Break"] = True
            guis.textWidget(id=id,parent=parent,style=style,data=attrs)
            add = False
        if tag in noformatlist:
            style = {"Color":"black"}
            style.update(cssstyle)
            #print(style)
            parent = guis.hlistWidget(id=id,parent=parent,style=style,data=attrs)
            #print(parent)
        if tag in italics:
            style = {
            "Font":{
            "File":"./assets/Xolonium-Bold.ttf"
            ,"Scale":20,
            "Italics":True,
            "Underline":False
            }}
            style.update(cssstyle)
            #print(style)
            parent = guis.wraplistWidget(id=id,parent=parent,style=style,data=attrs)
            #print(parent)
        if tag in headings:
            style = {
            "Text":"","Font":{
            "File":"./assets/Xolonium-Bold.ttf",
            "Scale":int((headings.index(tag)+5)*4),
            "Italics":False,
            "Underline":False
            }}
            style.update(cssstyle)
            #print(style)
            parent = guis.textWidget(id=id,parent=parent,style=style,data=attrs)
            #print(parent)
        if tag in images:
            style = {
            "Image":"self.data['src']"
            }
            style.update(cssstyle)
            #print(style)
            parent = guis.imageWidget(id=id,parent=parent,style=style,data=attrs)
            #print(parent)
        if tag in canvases:
            style = {}
            style.update(cssstyle)
            #print(style)
            parent = guis.canvasWidget(id=id,parent=parent,style=style,data=attrs)
            #print(parent)
        if tag in dd:
            style = {"Text":"'   '+str(self.data['Text'])"}
            style.update(cssstyle)
            #print(style)
            parent = guis.textWidget(id=id,parent=parent,style=style,data=attrs)
        if tag in buttons:
            style = {}
            style.update(cssstyle)
            parent = guis.buttonWidget(id=id,parent=parent,action="",style=style,data=attrs)
        if tag in quotes:
            style = {"Text":'"'}
            style.update(cssstyle)
            guis.textWidget(id=id,parent=parent,style=style,data=attrs)
            add = False
        if tag in scripts:
            add = False
        if add:
            parents.append(parent)
        #print([ p.id for p in parents])

    def handle_endtag(self, tag):
        global parent
        remove = True
        #print(tag)
        parent.data["Text"] = gdata
        if "id" in gattrs:
            id = gattrs["id"]
        else:
            id = tag
        if tag in scripts:
            #print(tag,scripts)
            #print(gdata)
            javascript.eval(gdata)
            remove = False
        if tag in quotes:
            style = {"Text":'"'}
            #print(parent)
            guis.textWidget(id=id,parent=parent,style=style,data={})
            remove = False
            #parents.pop(-1)
        #print([ p.id for p in parents])
        if remove:
            parents.pop(-1)
            if len(parents) >0:
                parent = parents[-1]
            #print([ p.id for p in parents])

    def handle_data(self, data):
        global gdata
        global parent
        gdata = data
        data = data.replace("\n","")
        cssstyle = {}
        if "style" in gattrs:
            cssstyle = css.csstodict(gattrs["style"])

        #print(parenttype)
        if parenttype not in notextlist:
            if not data.isspace():
                s = data.split("\n")
                for x in s:
                    style = {"Text":x}
                    style.update({"Wrap":"dw"})
                    style.update(cssstyle)
                    guis.textWidget(id=data,parent=parent,style=style,data={"Testing"})
        #print(parent)

    def __init__(self):
        global parents
        global screen
        global parent
        global doc
        parent = guis.mainWidget(background="white",style={})
        parents = []
        screen = parent
        doc = screen
        #print(javascript.context["document"])
        #print(javascript)
        javascript.context["document"] = screen
        super(GUIsHTMLParser,self).__init__()

clock = pygame.time.Clock()

if __name__ == "__main__":
    openfile("./testhtml/test.html")
    pygame.quit()
    quit()
