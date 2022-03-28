#-----------------------------------------------------------------------------------------#
# 2021 Tommy Reding
#-----------------------------------------------------------------------------------------#

try:
    from . import colors
    from .colors import *
except:
    from colors import *

try:
    from . import css
except:
    import css

from .widget import *

import math
import pygame
from pygame.locals import *
import json as jsonmod
import random
import glob
import importlib
import sys
import os
import pathlib
import difflib
import zipfile
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import pylab
import traceback
import inspect

def modint(interpreterdata,mods):
    pass

def init(modules):
    pass


# Renderer
dw = 250
dh = 250
usefull = False
fontsize = 32
drawx = 0
drawy = 0
draw = 0

#Data
randid = 1
frame = False
dragging = None

parser = css.cssparser()

parser.feed("""

    textWidget {
        Background: red;
    }

    textWidget + textWidget {
        Background: limegreen;
    }

    vlistWidget,textWidget {
        Color: blue;
    }

    .class ~ textWidget {
        Color: lightblue;
    }

    radioWidget {
        Background: lgrey;
    }

    radioWidget:hover {
        Background: grey;
    }

    radioWidget:active {
        Background: yellow;
    }

    p::first-line {
        color: yellow;
    }

    div > p {
        padding: 32px;
    }

    p + p  p{
        color: green;
    }

    #img + p {
        color: limegreen;
    }
    """)
parser.parse()

globallink = {}

#-----------------------------------------------------------------------------------------#
#Generic
#-----------------------------------------------------------------------------------------#

def clamp(num, min_value, max_value):
        num = max(min(num, max_value), min_value)
        return num

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

def truncline(text, font, maxwidth):
        real=len(text)
        stext=text
        l=font.size(text)[0]
        cut=0
        a=0
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)
            done=0
        return real, done, stext

def wrapline(text, font, maxwidth):
    done=0
    wrapped=[]
    while not done:
        nl, done, stext=truncline(text, font, maxwidth)
        wrapped.append(stext)
        text=text[nl:]
    return wrapped

def DrawBorder(x, y, w, h, t, color, surf):
    pygame.draw.rect(surf, color, (x, y, w, t)) # top
    pygame.draw.rect(surf, color, (x, y, t, h)) # left
    pygame.draw.rect(surf, color, (x, y + h - t , w, t)) # bottom
    pygame.draw.rect(surf, color, (x + w - t , y, t, h)) # right

#-----------------------------------------------------------------------------------------#
#Widgets
#-----------------------------------------------------------------------------------------#
allstyles = (
"ABSX","ABSY","Color","W","H",
"Angle","Maxangle","Flip","ActiveColor","InactiveColor",
"Background","Text","Wrap","Wrapwidth","Image",
"Justification","FillValue","Round",
"Display","ovy","ovx",
"Padding","Margin","Border","Slider","Gradient","Font"
)

# Base Classes  2

class widget(object):

# Start Helpers
    def countchildren(self):
        n = 0
        c = self.children
        if len(c)>0:
            for x in c:
                n+=x.countchildren()
        else:
            n=1
        return n

    def lookup(self,lparser=None):
        if parser != None:
            data = lparser.get(self)
            for d in data:
                if d != []:
                    self.style.update(d[1])

    def __str__(self):
        return "ID: "+str(self.id)+"\nStyle: "+str(self.style)+"\nParent: "+str(self.parent)

    def add(self,parent):
        if not (parent == None):
            if isinstance(parent,widget):
                self.parentref = parent
            #print(self.parentref)
                self.parentref.children.append(self)
        else:
            self.parentref = None

    def find(self,query):
        for x in self.children:
            if x.id == query:
                return x
            else:
                v = x.find(query)
                if v != None:
                    return v
        for x in self.popouts:
            if x.out:
                if x.id == query:
                    return x
                else:
                    v = x.find(query)
                    if v != None:
                        return v
        return None

    def hasParentOfQuery(self,query):
        v=self.matchesQuery(query)
        if type(v)==tuple:
            b,n = v
        if b:
            return b
        else:
            if self.parentref!=None:
                return self.parentref.hasParentOfQuery(query)
            else:
                return False

    def matchesQuery(self,query):
        good = True
        v=query
        prio=0
        if v!="":
            if v[0] not in css.selectors:
                if v == self.type:
                    prio+=1
                else:
                    good = False
            else:
                if v[0]=="#":
                    if v[1:] == self.id:
                        prio+=1
                    else:
                        good = False
                elif v[0]==".":
                    if v[1:] in self.classes:
                        prio+=1
                    else:
                        good = False
                elif v[0]==":":
                    r = self.testState(v[1:])
                    if r:
                        prio+=1
                    else:
                        good=False
                elif v[0:1]=="::":
                    pass
        return good,prio

    def copy(self,newid=randid,newparent=None):
        global randid
        randid+=1
        if newparent == None:
            newparent = self.parentref
        o = type(self)(id=newid, parent=newparent, style=self.style)
        for c in self.children:
            c.copy(randid,o)
        return o

    def lastSibling(self):
        if self.parentref != None:
            list = self.parentref.children
            if self in list:
                i = list.index(self)
                if i!=0:
                    return self.parentref.children[i-1]
                else:
                    return None
            else:
                return None
        else:
            return None

    def nextSibling(self):
        if self.parentref != None:
            list = self.parentref.children
            if self in list:
                i = list.index(self)
                if len(list)>=i+2:
                    return self.parentref.children[i+1]
                else:
                    return None
            else:
                return None
        else:
            return None

    def testState(self,state):
        if state=="hover":
            ex,ey = pygame.mouse.get_pos()
            b = (
            self.rx+self.w+self.x > ex > self.rx+self.x
            and
            self.ry+self.h+self.y > ey > self.ry+self.y
            )
            #print(b)
            return b
        elif state=="slidehover":
            ex,ey = pygame.mouse.get_pos()
            b = (
            self.rx+self.x+self.hlargest() > ex > self.rx+self.x
            and
            self.ry+self.y+self.vlargest() > ey > self.ry+self.y
            )
            print(ex,ey)
            return b
        elif state=="active":
            ex,ey = pygame.mouse.get_pos()
            b = ((
            (
            self.rx+self.w+self.x > ex > self.rx+self.x
            and
            self.ry+self.h+self.y > ey > self.ry+self.y
            )
            and
            pygame.mouse.get_pressed()[0]
            )
            or self.active
            )
            return b

# End Helpers
# Start Style

    def vfill(self):
        h = self.parentref.h/len(self.parentref.children)
        return h

    def hfill(self):
        w = self.parentref.w/len(self.parentref.children)
        return w

    def vfitchildren(self):
        h=0
        for x in self.children:
            h += x.calc(x.h)
        return h

    def hlargest(self):
        #print(self.id)
        #print(self.w)
        w=0
        for x in self.children:
            #print(x.w)
            if w < x.calc(x.w):
                w = x.calc(x.w)
        #print(w)
        return w

    def hfitchildren(self):
        #print(self.id)
        w=0
        for x in self.children:
            w += x.calc(x.w)
        return w

    def vlargest(self):
        h=0
        for x in self.children:
            if h < x.calc(x.h):
                h = x.calc(x.h)
        #print(self.h)
        return h

    def getstyle(self,key):
        #print(self.skip)
        if key in self.style:
            return self.style[key]
        else:
            if self.parentref != None and key not in self.ignore:
                    return self.parentref.getstyle(key)
            else:
                    return None

    def stylecalc(self,style):
        for k in style:
            v = style[k]
            #print(k)
            if isinstance(v,str):
                try:
                    if self.getstyle(v) != None:
                        v = self.getstyle(v)
                        #print("Style: "+str(v))
                        style[k] = compile( v ,filename="style: "+str(v),mode="eval")
                except Exception as e:
                    print(e)
                    pass
        #print(style)
        self.styleize(style)

    def styleize(self,style):
        for k in allstyles:
            if k not in self.ignore:
                x = self.getstyle(k)
                if x != None:
                    x = self.calc(x)
                    if type(x) == dict:
                        for sk in x:
                            x[sk] = self.calc(x[sk])
                        #print(k,x)
                    setattr(self, k.lower(),x)
        if "Image" in style:
            i = str(self.calc(style["Image"]))
            if i != None and i != self.limg:
                i = i.replace("./",str(path)+"/")
                try:
                    self.image = str(i)
                    #print(self.image)
                    self.img = pygame.image.load(self.image)
                    self.limg = i
                except:
                    print("Invalid Image: "+str(self.parentref.calc(i)))
                    pass
        elif self.parentref != None:
            i = self.parentref.getstyle("Image")
            if i != None and i != self.limg:
                i = i.replace("./",str(path)+"/")
                try:
                    if self.parentref.getstyle("Image") != None:
                        self.image = self.calc(i)
                        self.img = pygame.image.load(self.image)
                        self.limg = i
                except:
                    print("Invalid Image: "+str(i))
                    pass
        if "Gradient" in style:
            Gradient = style["Gradient"]
            #print(Gradient)
            if None != Gradient:
                self.gradient["base"] = self.calc(Gradient["base"])
                self.gradient["end"] = self.calc(Gradient["end"])
                self.gradient["types"] = self.calc(Gradient["types"])
                self.gradient["vert"] = self.calc(Gradient["vert"])
                self.gradient["flip"] = self.calc(Gradient["flip"])
                self.gradient["inverse"] = self.calc(Gradient["inverse"])
            else:
                pass
        elif self.parentref != None:
            Gradient = self.parentref.getstyle("Gradient")
            if None != Gradient:
                self.gradient["base"] = self.calc(self.parentref.getstyle("Gradient")["base"])
                self.gradient["end"] = self.calc(self.parentref.getstyle("Gradient")["end"])
                self.gradient["types"] = self.calc(self.parentref.getstyle("Gradient")["types"])
                self.gradient["vert"] = self.calc(self.parentref.getstyle("Gradient")["vert"])
                self.gradient["flip"] = self.calc(self.parentref.getstyle("Gradient")["flip"])
                self.gradient["inverse"] = self.calc(self.parentref.getstyle("Gradient")["inverse"])
            else:
                pass

    def wraplargestw(self):
        w = 0
        for x in self.children:
            if w < self.wrapwidth or self.wrapwidth<0:
                w += x.w
        return w

    def wraplargesth(self):
        #print(h)
        return self.wrapedhight

    def wrapfitw(self):
        #print(h)
        return self.wrapedhight

# End Style

    def calc(self, input="",lglobals=None):
        if lglobals==None:
            lglobals = globals().copy()
            lglobals.update(globallink)
        list = []
        try:
            v = eval(input,lglobals,locals())
            return v
        except Exception as e:
            #print(e,input)
            return input

    def update(self):
        self.changed = True
        for x in self.children:
            #print(x)
            x.update()
        for x in self.popouts:
            #print(x)
            if x.out:
                x.update()

    def prossesinputs(self,eventname,event,surface,lglobals=None):
        self.lookup(parser)
        if lglobals == None:
            lglobals = globals()
        self.changed = True
        #self.styleize(self.style)
        for x in self.notifys:
            exec(x,lglobals,locals())
        for x in self.children:
            x.prossesinputs(eventname,event,surface,lglobals)
        for x in self.popouts:
            if x.out:
                x.prossesinputs(eventname,event,surface,lglobals)

    def drawInterior(self,surfacein):
        #print(self.background)
        #print(self.getstyle("Border"))
        #print(drawx,drawy,self.w,self.h)
        if self.background != None:
            #print(self.background)
            try:
                pygame.draw.rect(
                surfacein,self.background,
                pygame.Rect(
                (drawx)
                ,(drawy)
                ,self.w
                ,self.h
                )
                ,
                border_top_left_radius=self.round[0],
                border_bottom_left_radius=self.round[3],
                border_top_right_radius=self.round[1],
                border_bottom_right_radius=self.round[2]
                )
            except Exception as e:
                print(e)
                pass

        if self.gradient != None:
            #print(self.background)
            if self.gradient!=self.lastgradient:
                self.lastgradient = self.gradient
                if "background" in self.gradient["types"]:
                    try:
                        x = 0 if self.x<0 else self.x
                        y = 0 if self.y<0 else self.y
                        w = dw-self.x if (self.w+self.x)>dw else self.w
                        h = dh-self.y if (self.h+self.y)>dh else self.h
                        surf = surfacein.subsurface((x,y,w,h))
                        rect = surf.get_rect()
                        colors.gradientizecolor(surf,
                        self.gradient["base"],
                        self.gradient["end"],
                        togradient=self.background,
                        rect=rect,
                        vertical=self.gradient["vert"],
                        flip=self.gradient["flip"]
                        ,forward=self.gradient["inverse"])
                        rect[0] = rect[0]+self.x
                        rect[1] = rect[1]+self.y
                        self.gradientsurfint = surf.copy()
                        if (not surf.get_locked() and not surfacein.get_locked()):
                            surfacein.blit(surf,rect)
                            pass
                    except Exception as e:
                        #print(e,traceback.format_exc(limit=5, chain=True))
                        pass
            else:
                if "background" in self.gradient["types"]:
                    if hasattr(self,"gradientsurfint"):
                        rect = self.gradientsurfint.get_rect()
                        rect[0] = rect[0]+self.x
                        rect[1] = rect[1]+self.y
                        if not surfacein.get_locked():
                            surfacein.blit(self.gradientsurfint,rect)
                        pass

    def drawBorder(self,surfacein):
        global drawx
        global drawy
        #print(self.border)
        #print(surfacein)
        #print(self.getstyle("Border"))
        #print(drawx,drawy,self.w,self.h,self.margin,self.padding)
        if self.border != None:
            DrawBorder(drawx
            ,drawy, self.w+self.padding[0]+self.padding[2]+(self.border["width"]*2)
            , self.h+self.padding[1]+self.padding[3]+(self.border["width"]*2)
            , self.border["width"], self.border["color"], surfacein)



        """
        pygame.draw.rect(
        surfacein,self.border["color"],
        pygame.Rect(
        (drawx)
        ,(drawy)
        ,self.w+self.padding[0]+self.padding[2]+(self.border["width"]*2)
        ,self.h+self.padding[1]+self.padding[3]+(self.border["width"]*2)
        ),
        self.border["width"]
        ,
        border_top_left_radius=self.round[0],
        border_bottom_left_radius=self.round[3],
        border_top_right_radius=self.round[1],
        border_bottom_right_radius=self.round[2]
        )
        """


        if self.gradient != None:
            #print(self.background)
            if "border" in self.gradient["types"]:
                try:
                    x = 0 if self.x<0 else self.x
                    y = 0 if self.y<0 else self.y
                    w = dw-self.x if (self.w+self.x)>dw else self.w
                    h = dh-self.y if (self.h+self.y)>dh else self.h
                    surf = surfacein.subsurface((x,y,w,h))
                    surf = surf.copy()
                    colors.gradientizewhite(surf, self.gradient["base"], self.gradient["end"],
                    vertical=self.gradient["vert"],flip=self.gradient["flip"]
                    ,forward=self.gradient["inverse"])
                    rect = surf.get_rect()
                    rect[0] = rect[0]+self.x
                    rect[1] = rect[1]+self.y
                    if (not surf.get_locked() and not surfacein.get_locked()):
                        surfacein.blit(surf,rect)
                        pass
                except Exception as e:
                    print(e)
                    pass

    def draworign(self,surfacein):
        pygame.draw.rect(surfacein,(255,0,255),(self.x-5,self.y-5,10,10))

    def drawPopouts(self,surfacein):
        for x in self.popouts:
            if x.out:
                x.absy = drawy
                x.absx = drawx
                #print(x.absy)
                x.redrawpopout(surfacein)

#Box Model

    def redraw(self,surfacein):
        global drawx
        global drawy
        orx=drawx
        ory=drawy
        self.styleize(self.style)
        self.entermargins()
        self.enterpadding()
        self.shiftBorder()
        self.drawInterior(surfacein)
        self.padcontent()
        self.redrawInBox(surfacein)
        self.unpadcontent()
        self.unshiftBorder()
        self.drawBorder(surfacein)
        self.exitpadding()
        self.exitmargins()
        drawy=ory
        drawx=orx

    def shiftBorder(self):
        global drawx
        global drawy
        if (self.border["width"])>0:
            drawx+=(self.border["width"])
            drawy+=(self.border["width"])
            self.x+=(self.border["width"])
            self.y+=(self.border["width"])

    def unshiftBorder(self):
        global drawx
        global drawy
        if (self.border["width"])>0:
            drawx-=(self.border["width"])
            drawy-=(self.border["width"])
            self.x-=(self.border["width"])
            self.y-=(self.border["width"])

    def entermargins(self):
        global drawx
        global drawy
        drawx+=self.margin[0]
        drawy+=self.margin[1]
        self.x+=self.margin[0]
        self.y+=self.margin[1]

    def exitmargins(self):
        global drawx
        global drawy
        drawx+=self.margin[2]
        drawy+=self.margin[3]
        self.x+=self.margin[2]
        self.y+=self.margin[3]
        self.w+=self.margin[0]
        self.h+=self.margin[1]
        self.w+=self.margin[2]
        self.h+=self.margin[3]
        if (self.border["width"])>0:
            self.w+=(self.border["width"])
            self.h+=(self.border["width"])
            self.w+=(self.border["width"])
            self.h+=(self.border["width"])

    def enterpadding(self):
        self.w+=self.padding[0]
        self.h+=self.padding[1]
        self.w+=self.padding[2]
        self.h+=self.padding[3]

    def padcontent(self):
        global drawx
        global drawy
        self.w-=self.padding[0]
        self.h-=self.padding[1]
        self.w-=self.padding[2]
        self.h-=self.padding[3]
        drawx+=self.padding[0]
        drawy+=self.padding[1]
        self.x+=self.padding[0]
        self.y+=self.padding[1]

    def unpadcontent(self):
        global drawx
        global drawy
        drawx-=self.padding[0]
        drawy-=self.padding[1]
        self.x-=self.padding[0]
        self.y-=self.padding[1]

    def exitpadding(self):
        global drawx
        global drawy
        self.w+=self.padding[0]
        self.h+=self.padding[1]
        self.w+=self.padding[2]
        self.h+=self.padding[3]
        if (self.border["width"])>0:
            drawx+=(self.border["width"])
            drawy+=(self.border["width"])
            self.x+=(self.border["width"])
            self.y+=(self.border["width"])

    def redrawInBox(self,surfacein):
        global drawy
        global drawx
        #print(self.id,(self.x,self.y,self.w,self.h),(drawx,drawy))
        for x in self.children:
            x.y = drawy
            x.x = drawx
            x.redraw(surfacein)
        self.drawPopouts(surfacein)

    def __init__(self, id=randid, parent=None,style={},data={}):
        global randid
        randid += 1
        self.h = 0
        self.w = 0
        self.wrapedhight = 0
        self.wrapedwidth = 0
        self.y = 0
        self.ovy = "visible"
        self.ovx = "visible"
        self.x = 0
        self.id = id
        self.out = False
        self.children = []
        self.child = ""
        self.sibling = ""
        self.parent = parent
        self.skip = []
        self.type = str(type(self).__name__ )
        #print(self.type)
        self.frame = False
        self.ispressing = False
        self.mouseover = False
        self.active = False
        self.changed = True
        self.limg = None
        self.dbackground = (0,0,0)
        self.wrap = 32
        self.image = "./assets/pythonicon.png"
        self.imgr = (0,0,0,0)
        self.absx = 0
        self.absy = 0
        self.lastgradient = "Blahb"
        self.display="vlist"
        if hasattr(self,"style"):
            self.style.update(style)
        else:
            self.style = style
        if hasattr(self,"classes"):
            self.classes.extend(style)
        else:
            self.classes = []
        if hasattr(self,"data"):
            self.data.update(data)
        else:
            self.data = data
        if not hasattr(self,"ignore"):
            self.ignore = {}
        self.border = {
        "color":"white",
        "width":-1,
        "round":0
        }
        self.round = (-1,-1,-1,-1)
        self.padding = (0,0,0,0)
        self.margin = (0,0,0,0)
        self.color = (255,255,255)
        self.activecolor = (255,255,255)
        self.inactivecolor = (255,255,255)
        self.background = None
        self.text = ""
        self.justification = ""
        self.angle = 0
        fontpath = pathlib.PurePath(path,"assets/Xolonium-Bold.ttf")
        self.font = {"File":fontpath,"Scale":20,
        "Italics":False,
        "Underline":False}
        self.lastfont = {}
        self.flip = False
        self.gradient = {
        "base":(0,0,0),
        "end":(0,0,0),
        "types":"",
        "inverse":False,
        "vert":True,
        "flip":False
        }
        #print(parent)
        self.add(parent)
        self.radiovalue = ""
        self.notifys = []
        self.popouts = []
        self.rx = 0
        self.ry = 0
        self.lookup(parser)
        self.styleize(style)
        self.stylecalc(self.style)

class widgetCollection(widget):

    def create(self,id,parent):
        pass

    def __init__(self,id,parent):
        self.create(id,parent)

# Main / Surface   4

class mainWidget(widget):
    def redraw(self,surfacein):
        #print("main")
        global drawy
        drawy = 0
        global drawx
        drawx = 0
        global frame
        #print(drawx,drawy)
        #print(self.style)
        s = pygame.display.get_window_size()
        global dw,dh
        dw = s[0]
        dh = s[1]
        frame = not frame
        if self.changed:
            if self.mainbackground != None:
                surfacein.fill(self.mainbackground)
            else:
                surfacein.fill(black)
        super(mainWidget, self).redrawInBox(surfacein)
        #print(drawx,drawy)

    def __init__(self,pygame=pygame,background=None,inglobals=globals(),style={},data={}):
        global globallink
        globallink.update(inglobals)
        self.children = []
        self.popouts = []
        self.mainbackground = self.calc(background)
        self.globals = inglobals
        self.changed = True
        self.style = {
        "H":"self.vlargest()",
        "W":"self.hlargest()",
        "Color":(0,0,0),
        "ABSX":"drawx",
        "ABSY":"drawy",
        "ActiveColor":(200,200,200),
        "InactiveColor":(155,155,155),
        "Background":None,
        "Justification":"left top",
        "Image":"./assets/pythonicon.png",
        "Padding":(0,0,0,0),
        "Margin":(0,0,0,0),
        "Border":{
        "color":"white",
        "width":-1,
        "round":0
        },
        "Text":"",
        "Angle":0,
        "Wrap":-1,
        "Round":(0,0,0,0),
        "Gradient":{
        "base":(0,0,0),
        "end":(0,0,0),
        "types":"",
        "inverse":False,
        "vert":True,
        "flip":False
        },
        "Flip":False,
        "Font":{
        "File":"./assets/Xolonium-Bold.ttf"
        ,"Scale":20,
        "Italics":False,
        "Underline":False}
        }
        super(mainWidget, self).__init__("main"+str(randid),None,style)

class surfaceWidget(widget):

    def prossesinputs(self,eventname,event,surface,globals):
        for x in self.children:
            x.prossesinputs(eventname,event,self.mysurface,globals)

    def redrawInBox(self,surfacein):
        #if self.mysurface == "" or self.recalc:
            #print((self.surfx,self.surfy,self.w,self.h))
        self.mysurface = surfacein.subsurface(
        (self.x,self.y,self.w,self.h))
        super(surfaceWidget, self).redrawInBox(self.mysurface)

    def __init__(self,name,parent,
    surface=None,style={},data={}):
        self.name = name
        self.mysurface = pygame.display.get_surface()
        self.parent = parent
        super(surfaceWidget, self).__init__(name,parent,style)

class noneWidget(widget):

    def prossesinputs(self,eventname,event,surface):
        pass
        #super(noneWidget, self).prossesinputs(eventname, event, surface, self.globals)

    def redraw(self,surfacein):
        pass
        #super(noneWidget, self).redraw(surfacein)

    def __init__(self,id):
        self.children = []
        style = {
        "H":"self.vlargest()",
        "W":"self.hlargest()",
        "X":0,
        "Y":0,
        "Color":(255,255,255),
        "ActiveColor":(200,200,200),
        "InactiveColor":(155,155,155),
        "Background":None,
        "Justification":"left top",
        "Padding":(0,0,0,0),
        "Margin":(0,0,0,0),
        "Border":{
        "color":"white",
        "width":-1,
        "round":0
        },
        "Text":"",
        "Image":"./assets/pythonicon.png",
        "Angle":0,
        "Wrap":72,
        "Round":(0,0,0,0),
        "Gradient":{
        "base":(0,0,0),
        "end":(0,0,0),
        "types":"",
        "inverse":False,
        "vert":True,
        "flip":False
        },
        "Flip":False
        }
        self.changed = True
        super(noneWidget, self).__init__(id,None,style)

class popoutWidget(widget):

    def redrawpopout(self,surfacein):
        global drawy
        global drawx
        #print(self.absy)
        #print(self.absx)
        #print(self.style)
        self.styleize(self.style)
        for x in self.children:
            x.redraw(surfacein)

    def redraw(self,surfacein):
        pass

    def add(self,parent):
        if parent != None:
            if isinstance(parent,widget):
                self.parentref = self.parent
                self.parentref.popouts.append(self)
                if self.parentref.child == "":
                    self.parentref.child = self
                else:
                    loopingl = True
                    v = self.parentref.child
        else:
            self.parentref = None

    def __init__(self,id,parent,style,data={}):
        self.children = []
        self.popouts = []
        self.style = {
        "H":"self.vlargest()",
        "W":"self.hlargest()",
        "Color":(255,255,255),
        "ActiveColor":(200,200,200),
        "InactiveColor":(155,155,155),
        "Background":None,
        "Justification":"left top",
        "Padding":(0,0,0,0),
        "Margin":(0,0,0,0),
        "Border":{
        "color":"white",
        "width":-1,
        "round":0
        },
        "Text":"",
        "Image":"./assets/pythonicon.png",
        "Angle":0,
        "Wrap":72,
        "Round":(0,0,0,0),
        "Gradient":{
        "base":(0,0,0),
        "end":(0,0,0),
        "types":"",
        "inverse":False,
        "vert":True,
        "flip":False
        },
        "Flip":False
        }
        self.changed = True
        super(popoutWidget, self).__init__(id,parent,style,data)

# Display / HUD    6

class textWidget(widget):
    def textboxh(self,num):
        h = self.wraplargesth()
        if h > num:
            return h
        else:
            return num

    def textboxw(self,num):

        w = self.wraplargestw()
        if w > num:
            return w
        else:
            return num

    def redrawInBox(self,surfacein):
        global drawy
        global drawx
        self.styleize(self.style)

        if self.lasttext != self.text:
            self.chars=[]
            self.children=[]
            for c in self.text:
                cw=charWidget(id=self.id,parent=self)
                cw.text=c
                self.chars.append(cw)
            self.lasttext = self.text
            yoffset = 0
            gh = 0
            gw = 0
            lw = 0
            drawy -= self.y
            drawx -= self.x
            self.wrapedhight = 0
            self.wrapedwidth = 0
            self.tsurf = pygame.Surface((dw,dh))
            self.tsurf = self.tsurf.convert_alpha()
            self.tsurf.fill((0,0,0,0))
            for x in self.chars:
                if (( not self.wrapwidth <= 0 and self.wrapwidth < lw)
                or "Break" in x.data or ( "EndBreak" in x.data)):
                    drawy += gh
                    #print("S")
                    self.wrapedhight += gh
                    if gw>self.wrapedwidth:
                        self.wrapedwidth = gw
                    drawx = 0
                    gh = x.h
                    lw = 0
                    #drawy = drawy+yoffset
                x.y = drawy
                x.x = drawx
                #print(x)
                x.redraw(self.tsurf)
                if "Break" not in x.data:
                    gw += x.w
                    lw += x.w
                if gh < x.h:
                    gh = x.h
                if gw < x.w:
                    gw = x.w
                drawx += x.w
            surfacein.blit(self.tsurf,(drawx,drawy,self.w,self.h))
            self.wrapedhight += gh
        else:
            if hasattr(self, "tsurf"):
                surfacein.blit(self.tsurf,(drawx,drawy,self.w,self.h))
            else:
                self.lasttext=None
        drawx = self.x#+self.w
        drawy = self.y
        #print(self.w)
        self.drawPopouts(surfacein)
    """docstring for Text Object."""

    def __init__(self,id=randid,parent="main",style={},data={},wrapwidth=-1):
        self.style = {
        "W":"self.wraplargestw()",
        "H":"self.wraplargesth()",
        "Wrapwidth":"self.wrap"
        }
        self.chars=[]
        self.wrap = wrapwidth
        #self.wrapwidth = "self.wrap"
        self.textRect=(0,0,0,0)
        self.lasttext=""
        super(textWidget, self).__init__(id,parent,style,data)

class charWidget(widget):

    def textboxh(self,num):
        if self.textRect[3] > num:
            return self.textRect[3]
        else:
            return num

    def textboxw(self,num):
        if self.textRect[2] > num:
            return self.textRect[2]
        else:
            return num

    """A Text Widget"""
    def redrawInBox(self,surfacein):
        #self.draworign(surfacein)
        if self.font != self.lastfont:
            filepath = self.font["File"].replace("./",str(path)+"/")
            dynamicFont = Font(filepath, self.font["Scale"])
            self.realfont = dynamicFont
            self.realfont.underline = self.font["Underline"]
            self.realfont.italic = self.font["Italics"]
        #fullTextRect = pygame.Rect(0,0,0,0)
        if self.changed and self.text!=self.lasttext:
            global drawx
            global drawy
            #print(str(self)+str(drawx))
            #print(drawy)
            self.lasttext=self.text
            drawx += self.padding[0]+self.margin[0]
            drawy += self.padding[1]+self.margin[1]
            #print(self.text)
            #textSurface = ""
            offset = [0,0]
            #print(t)
            #pygame.draw.rect(surfacein, (255,0,0), (self.x,self.y,self.w,self.h))
            #print(t)
            self.surf = self.realfont.render(self.text, True, self.color)
            textRect = self.surf.get_rect()
            textRect.center = (drawx, drawy)
            #print(textRect)
            j = self.calc(self.justification)
            if "left" in j :
                    textRect = textRect.move(textRect[2]/2,0)
            elif "center" in j:
                    textRect = textRect.move(self.w/2,0)
            elif "right" in j :
                    textRect = textRect.move(self.w-textRect[2]/2,0)
            if "top" in j :
                    textRect = textRect.move(0,textRect[3]/2)
            elif "middle" in j:
                    textRect = textRect.move(0,self.h/2)
                    #textRect = textRect.move(0,-1*textRect[3])
            elif "bottom" in j :
                textRect = textRect.move(0,self.h)
            #pygame.draw.rect(surfacein, (255,0,0), textRect)
            #self.surf.blit(tSurface, textRect)
            #if fullTextRect[3] < tRect[3]:
            #fullTextRect[3] += tRect[3]
            #print(textRect)
            #self.changed = False
            #textRect = textSurface.get_rect()
            #print(fullTextRect)
            self.textRect = textRect
            drawx += self.padding[2]+self.margin[2]
            drawy += self.padding[3]+self.margin[3]
            self.changed=False
        #self.draworign(surfacein)
        #print(drawx)
        #print(self.text)
        super(charWidget, self).redrawInBox(surfacein)
        #print(drawx)
        #print(self.color)
        textRect = self.surf.get_rect()
        textRect.center = (self.x, self.y)
        j = self.calc(self.justification)
        if "left" in j :
                textRect = textRect.move(textRect[2]/2,0)
        elif "center" in j:
                textRect = textRect.move(self.w/2,0)
        elif "right" in j :
                textRect = textRect.move(self.w-textRect[2]/2,0)
        if "top" in j :
                textRect = textRect.move(0,textRect[3]/2)
        elif "middle" in j:
                textRect = textRect.move(0,self.h/2)
                #textRect = textRect.move(0,-1*textRect[3])
        elif "bottom" in j :
            textRect = textRect.move(0,self.h)
        self.textRect = textRect
        if self.gradient != None:
            if "text" in self.gradient["types"]:
                surfTextRect = self.textRect
                surfTextRect = surfTextRect.move(self.x,self.y)
                try:
                    #print(surfTextRect)
                    #print(self.surf)
                    surf = self.surf.subsurface(surfTextRect)
                    colors.gradientizewhite(surf, self.gradient["base"], self.gradient["end"],
                    vertical=self.gradient["vert"],flip=self.gradient["flip"]
                    ,forward=self.gradient["inverse"])
                    rect = surf.get_rect()
                    rect = rect.move(self.x, self.y)
                    #print(rect)
                    #print(surfacein)
                    surfacein.blit(surf,rect)
                except Exception as e:
                    print(e)
                    surfacein.blit(self.surf,self.textRect)
                #print(rect)
            else:
                surfacein.blit(self.surf,self.textRect)
        else:
            surfacein.blit(self.surf,self.textRect)

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.textRect = (0,0,0,0)
        self.style = {
        "H":"self.textRect[3]",
        "W":"self.textRect[2]"
        }
        self.lasttext=""
        self.ignore=["Text","Border","Round","Background","Padding","Margin"]
        super(charWidget, self).__init__(id,parent,style,data)

class oldtextWidget(widget):

    def textboxh(self,num):
        if self.textRect[3] > num:
            return self.textRect[3]
        else:
            return num

    def textboxw(self,num):
        if self.textRect[2] > num:
            return self.textRect[2]
        else:
            return num

    """A Text Widget"""
    def redrawInBox(self,surfacein):
        #self.draworign(surfacein)
        fullTextRect = pygame.Rect(0,0,0,0)
        if self.changed == True:
            global drawx
            global drawy
            #print(str(self)+str(drawx))
            #print(drawy)
            surf = pygame.Surface((dw,dh))
            self.surf = surf.convert_alpha()
            self.surf.fill((0,0,0,0))
            drawx += self.padding[0]+self.margin[0]
            drawy += self.padding[1]+self.margin[1]
            #print(self.text)
            if int(self.wrap)>0:
                t = wrapline(self.text,self.realfont,int(self.wrap))
            else:
                t = [self.text]
            #textSurface = ""
            offset = [0,0]
            #print(t)
            #pygame.draw.rect(surfacein, (255,0,0), (self.x,self.y,self.w,self.h))
            #print(t)
            for x in t:
                if type(self.color) != dict :
                    tSurface = self.realfont.render(x, True, self.color)
                else:
                    tSurface = self.realfont.render(x, True, (0,0,0))
                textRect = tSurface.get_rect()
                tRect = tSurface.get_rect()
                textRect.center = (drawx+offset[0], drawy+offset[1])
                #print(textRect)
                j = self.calc(self.justification)
                if "left" in j :
                    textRect = textRect.move(textRect[2]/2,0)
                elif "center" in j:
                    textRect = textRect.move(self.w/2,0)
                elif "right" in j :
                    textRect = textRect.move(self.w-textRect[2]/2,0)
                if "top" in j :
                    textRect = textRect.move(0,textRect[3]/2)
                elif "middle" in j:
                    textRect = textRect.move(0,self.h/2)
                    #textRect = textRect.move(0,-1*textRect[3])
                elif "bottom" in j :
                    textRect = textRect.move(0,self.h)
                #pygame.draw.rect(surfacein, (255,0,0), textRect)
                self.surf.blit(tSurface, textRect)
                offset[1] += tRect[3]
                if fullTextRect[2] < tRect[2]:
                    fullTextRect[2] = tRect[2]
                #if fullTextRect[3] < tRect[3]:
                fullTextRect[3] += tRect[3]
                #print(textRect)
                #self.changed = False
            #textRect = textSurface.get_rect()
            #print(fullTextRect)
            self.textRect = fullTextRect
            drawx += self.padding[2]+self.margin[2]
            drawy += self.padding[3]+self.margin[3]
        #self.draworign(surfacein)
        #print(drawx)
        #print(drawy)
        super(textWidget, self).redrawInBox(surfacein)
        #print(drawx)
        #print(self.color)
        if self.gradient != None:
            if "text" in self.gradient["types"]:
                surfTextRect = self.textRect
                surfTextRect = surfTextRect.move(self.x,self.y)
                try:
                    #print(surfTextRect)
                    #print(self.surf)
                    surf = self.surf.subsurface(surfTextRect)
                    colors.gradientizewhite(surf, self.gradient["base"], self.gradient["end"],
                    vertical=self.gradient["vert"],flip=self.gradient["flip"]
                    ,forward=self.gradient["inverse"])
                    rect = surf.get_rect()
                    rect = rect.move(self.x, self.y)
                    #print(rect)
                    #print(surfacein)
                    surfacein.blit(surf,rect)
                except Exception as e:
                    print(e)
                    surfacein.blit(self.surf,fullTextRect)
                #print(rect)
            else:
                surfacein.blit(self.surf,fullTextRect)
        else:
            surfacein.blit(self.surf,fullTextRect)

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.textRect = (0,0,0,0)
        self.style = {
        "H":"self.textRect[3]",
        "W":"self.textRect[2]"
        }
        super(textWidget, self).__init__(id,parent,style,data)

class hprogressWidget(widget):
    """A Progress Bar Widget"""
    def redrawInBox(self,surfacein):
        super(hprogressWidget, self).redrawInBox(surfacein)
        if self.color != None:
            if self.flip:
                    rect = pygame.Rect(
                    self.x+self.w-(self.w*self.fillvalue),
                    self.y,
                    self.w*self.fillvalue
                    ,self.h)
            else:
                    rect = pygame.Rect(self.x,self.y,
                    self.w*self.fillvalue,self.h)
            pygame.draw.rect(surfacein,self.color, rect,0,
                border_top_left_radius=self.round[0],
                border_bottom_left_radius=self.round[3],
                border_top_right_radius=self.round[1],
                border_bottom_right_radius=self.round[2]
                )

class vprogressWidget(widget):
    """A Progress Bar Widget"""
    def redrawInBox(self,surfacein):
        super(vprogressWidget, self).redrawInBox(surfacein)
        if self.color != None:
                #print( str( (self.h)-(self.h*self.fillvalue)+(self.h*self.fillvalue) ) )
                #print(self.y)
                if self.flip:
                    rect = pygame.Rect(
                    self.x,
                    (self.y)+self.h-(self.h*self.fillvalue),
                    self.w,
                    (self.h*self.fillvalue)
                    )
                else:
                    rect = pygame.Rect(
                    self.x,
                    self.y,
                    self.w,
                    (self.h*self.fillvalue)
                    )
                pygame.draw.rect(surfacein,self.color,rect
                ,0,
                border_top_left_radius=self.round[0],
                border_bottom_left_radius=self.round[3],
                border_top_right_radius=self.round[1],
                border_bottom_right_radius=self.round[2]
                )

class arcProgressWidget(widget):
    def redrawInBox(self,surfacein):
        super(arcProgressWidget, self).redrawInBox(surfacein)
        if self.flip: inc = -1
        else: inc = 1
        imgc = self.img
        imgc = pygame.transform.scale(imgc, (int(self.w/3), int(self.h/2)))
        #print(self.angle)
        #print(inc,self.fillvalue,self.maxangle)
        angle = (inc*self.fillvalue*self.maxangle)-self.angle
        imgc,imgr = rot_center(imgc, imgc.get_rect(), angle)
        imgr.center = (self.w/2,self.h/2)
        surfacein.blit(imgc,(self.x+imgr[0],self.y+imgr[1]))

    def __init__(self,id,parent,style,data={}):
        path = pathlib.Path(__file__).parent.resolve()
        imgpath = pathlib.PurePath(path,"assets/pointersmall.png")
        self.arrowblack = imgpath
        altimgpath = pathlib.PurePath(path,"assets/pointersmallwhite.png")
        self.arrowwhite = altimgpath
        self.style ={
        "Round":(25,25,0,0),
        "Image":imgpath
        }
        super(arcProgressWidget, self).__init__(id=id,
        parent=parent,
        style=style,data=data)

# Orginization  11

class listWidget(widget):

    def prossesinputs(self, eventname, event, surface, globals):
        super(listWidget, self).prossesinputs(eventname, event, surface, globals)
        self.scrollx.prossesinputs(eventname, event, surface, globals)
        self.scrolly.prossesinputs(eventname, event, surface, globals)

    def u_dwrapscrollredraw(self,surfacein):
        global drawy
        global drawx
        x = 0 if self.x<0 else self.x
        y = 0 if self.y<0 else self.y
        w = dw-self.x if (self.w+self.x)>dw else self.w
        h = dh-self.y if (self.h+self.y)>dh else self.h
        surf = surfacein.subsurface((x,y,w,h))
        drawx = 0
        drawy = 0
        xoffset = 0
        gh = 0
        gw = 0
        self.wrapedhight = 0
        self.wrapedwidth = 0
        lw=0
        lh=0
        scx=self.scrollx
        scy=self.scrolly
        bx = self.barx
        by = self.bary
        ofx = (scx.rx/( self.w - bx.w))*(self.wrapfitw()-self.w)
        ofy = (scy.ry/( self.h - by.h))*(self.vlargest()-self.h)
        drawx -= ofx
        drawy -= ofy
        for x in self.children:
            if (( not self.wrapwidth <= 0 and self.wrapwidth <= drawy)
            or "Break" in x.data or ( "EndBreak" in x.data)):
                xoffset += gw
                self.wrapedhight = gh
                self.wrapedwidth += gw
                drawy = 0 - ofy
                gw = x.w
            drawx = xoffset+ofx
            x.y = drawy
            x.x = drawx
            #print(x.y)
            x.redraw(surf)
            if "Break" not in x.data:
                gh += x.h
            if gh < x.h:
                gh = x.h
            if gw < x.w:
                gw = x.w
            #drawy += x.h
            drawy += x.h
        #print(self.w)
        #print(by.h,len(self.children),self.wrapedhight,by.h*len(self.children))
        self.wrapedwidth += gw
        drawx = self.x
        drawy = self.y + self.h
        if self.wrapedwidth>self.w :
            scx.y = drawy
            scx.x = drawx#+self.w
            scx.w = self.w
            bx.w = ( ( ( self.w / self.wrapfitw() ) ) * self.w )
            scx.redraw(surfacein)
        drawx=self.x
        drawy=self.y
        self.drawPopouts(surfacein)

    def u_dwrapredraw(self,surfacein):
        global drawy
        global drawx
        xoffset = 0
        gh = 0
        gw = 0
        self.wrapedhight = 0
        self.wrapedwidth = 0
        for x in self.children:
            if (( not self.wrapwidth < 0 and self.wrapwidth < drawy+self.y)
            or "Break" in x.data or ( "EndBreak" in x.data)):
                xoffset += gw
                self.wrapedhight = gh
                self.wrapedwidth += gw
                drawy = self.y
            drawx = self.x+xoffset
            x.y = drawy
            x.x = drawx
            #print(x)
            x.redraw(surfacein)
            if "Break" not in x.data:
                gh += x.h
            if gh < x.h:
                gh = x.h
            if gw < x.w:
                gw = x.w
            #drawy += x.h
            drawy += x.h
        drawx = self.x
        #print(self.w)
        drawx=self.x
        drawy=self.y#+self.h
        self.wrapedhight += gh
        self.drawPopouts(surfacein)

    def r_lwrapscrollredraw(self,surfacein):
        global drawy
        global drawx
        #print(self.id,(self.x,self.y,self.w,self.h),(drawx,drawy))
        x = 0 if self.x<0 else self.x
        y = 0 if self.y<0 else self.y
        w = dw-self.x if (self.w+self.x)>dw else self.w
        h = dh-self.y if (self.h+self.y)>dh else self.h
        surf = surfacein.subsurface((x,y,w,h))
        drawx = 0
        drawy = 0
        yoffset = 0
        gh = 0
        gw = 0
        lw=0
        lh=0
        scx=self.scrollx
        scy=self.scrolly
        bx = self.barx
        by = self.bary
        ofx = (scx.rx/( self.w - bx.w))*(self.hlargest()-self.w)
        ofy = (scy.ry/( self.h - by.h))*(self.wraplargesth()-scy.h)
        drawx -= ofx
        drawy -= ofy
        self.wrapedhight = 0
        self.wrapedwidth = 0

        for x in self.children:
            if (( not self.wrapwidth <= 0 and self.wrapwidth <= drawx)
            or "Break" in x.data or ( "EndBreak" in x.data)):
                yoffset += gh
                self.wrapedhight += gh
                self.wrapedwidth = gw
                drawx = 0 - ofx
                gh = x.h
            drawy = yoffset-ofy
            x.y = drawy
            x.x = drawx
            #print(x.y)
            x.redraw(surf)
            if "Break" not in x.data:
                gw += x.w
            if gh < x.h:
                gh = x.h
            if gw < x.w:
                gw = x.w
            #drawy += x.h
            drawx += x.w
        #print(self.w)
        self.wrapedhight += gh
        drawx = self.x + self.w
        drawy = self.y
        if self.wrapedhight>self.h :
            scy.y = drawy
            scy.x = drawx#+self.w
            scy.h = self.h
            by.h = ( ( ( scy.h / self.wraplargesth() ) ) * scy.h )
            scy.redraw(surfacein)
        drawx=self.x
        drawy=self.y
        if self.wrapedhight>self.h :
            self.w+=scy.w
        self.drawPopouts(surfacein)

    def r_lwrapredraw(self,surfacein):
        global drawy
        global drawx
        yoffset = 0
        gh = 0
        gw = 0
        itx = 0
        self.wrapedhight = 0
        self.wrapedwidth = 0
        for x in self.children:
            drawy = self.y+yoffset
            x.y = drawy
            x.x = drawx
            #print(x)
            x.redraw(surfacein)
            if "Break" not in x.data:
                gw += x.w
            if gh < x.h:
                gh = x.h
            if gw < x.w:
                gw = x.w
            #drawy += x.h
            drawx += x.w
            itx += x.w
            #print(itx)
            if (( not self.wrapwidth < 0 and self.wrapwidth <= itx)
            or "Break" in x.data or ( "EndBreak" in x.data)):
                yoffset += gh
                self.wrapedhight += gh
                self.wrapedwidth = gw
                drawx = self.x
                gh = x.h
                itx = 0
        drawx = self.x
        #print(self.w)
        drawx=self.x
        drawy=self.y#+self.h
        self.wrapedhight += gh
        self.drawPopouts(surfacein)

    def hscrollredraw(self,surfacein):
        global drawy
        global drawx
        x = 0 if self.x<0 else self.x
        y = 0 if self.y<0 else self.y
        w = dw-self.x if (self.w+self.x)>dw else self.w
        h = dh-self.y if (self.h+self.y)>dh else self.h
        surf = surfacein.subsurface((x,y,w,h))
        drawx = 0
        drawy = 0
        lw=0
        lh=0
        scx=self.scrollx
        scy=self.scrolly
        bx = self.barx
        by = self.bary
        ofx = (scx.rx/( self.w - bx.w))*(self.hfitchildren()-self.w)
        ofy = (scy.ry/( self.h - by.h))*(self.vlargest()-self.h)
        drawx -= ofx
        drawy -= ofy
        for x in self.children:
            drawy = 0 -ofy
            x.y = drawy
            x.x = drawx
            x.redraw(surf)
            lw+=x.w
            if x.h>lh:
                lh=x.h
            drawx = lw-ofx
        drawx = self.x
        drawy = self.y + self.h
        if lw>self.w or self.ovx=="scroll":
            scx.y = drawy# + self.h
            scx.x = drawx
            scx.w = self.w
            bx.w = ( ( ( self.w / self.hfitchildren() ) ) * self.w )
            #print(bx.w,len(self.children),self.w,bx.w*len(self.children))
            scx.redraw(surfacein)
        drawx = self.x + self.w
        drawy = self.y
        if lh>self.h :
            scy.y = drawy
            scy.x = drawx#+self.w
            scy.h=self.h
            by.h = ( ( ( self.h / self.vlargest() ) ) * self.h )
            scy.redraw(surfacein)
        drawx = self.x
        drawy = self.y
        if lw>self.w or self.ovx=="scroll":
            self.h+=self.scrollx.h
        if lh>self.h :
            self.w+=self.scrolly.w
        self.drawPopouts(surfacein)

    def hredraw(self,surfacein):
        global drawy
        global drawx
        if self.ovx == "hidden":
            surf = surfacein.subsurface(
            (self.x,self.y,self.w,self.h))
        else:
            surf = surfacein
        for x in self.children:
            drawy=self.y
            x.y = drawy
            x.x = drawx
            x.redraw(surf)
            drawx += x.w
        drawx = self.x
        drawy = self.y
        self.drawPopouts(surfacein)

    def vscrollredraw(self,surfacein):
        global drawy
        global drawx
        x = 0 if self.x<0 else self.x
        y = 0 if self.y<0 else self.y
        w = dw-self.x if (self.w+self.x)>dw else self.w
        h = dh-self.y if (self.h+self.y)>dh else self.h
        surf = surfacein.subsurface((x,y,w,h))
        lw=0
        lh=0
        scx=self.scrollx
        scy=self.scrolly
        bx = self.barx
        by = self.bary
        drawx = 0
        drawy = 0
        ofx = (scx.rx/( self.w - bx.w))*(self.hlargest()-self.w)
        ofy = (scy.ry/( self.h - by.h))*(self.vfitchildren()-self.h)
        #print(bx.h,len(self.children),self.h,bx.h*len(self.children), self.vfitchildren(),ofy)
        drawx -= ofx
        drawy -= ofy
        for x in self.children:
            drawx = 0 -ofx
            x.y = drawy
            x.x = drawx
            x.redraw(surf)
            if x.w>lw:
                lw=x.w
            lh+=x.h
            drawy = lh-ofy
        drawx = self.x + self.w
        drawy = self.y
        if lh>self.h or self.ovy=="scroll":
            scy.y = drawy
            scy.x = drawx#+self.w
            scy.h=self.h
            by.h = ( ( ( self.h / self.vfitchildren() ) ) * self.h )
            scy.redraw(surfacein)
        drawx = self.x
        drawy = self.y + self.h
        if lw>self.w :
            scx.y = drawy#+self.h
            scx.x = drawx
            scx.w=self.w
            bx.w = ( ( ( self.w / self.hlargest() ) ) * self.w )
            scx.redraw(surfacein)
        drawx = self.x
        drawy = self.y
        if lw>self.w :
            self.h+=self.scrollx.h
        if lh>self.h or self.ovy=="scroll":
            self.w+=self.scrolly.w
        self.drawPopouts(surfacein)

    def vredraw(self,surfacein):
        global drawy
        global drawx
        if self.ovy == "hidden":
            surf = surfacein.subsurface(
            (self.x,self.y,self.w,self.h))
        else:
            surf = surfacein
        for x in self.children:
            drawx = self.x
            x.y = drawy
            x.x = drawx
            x.redraw(surf)
            drawy += x.h
        drawx = self.x
        drawy = self.y
        self.drawPopouts(surfacein)

    def redrawInBox(self,surfacein):
        #||scroll|auto|initial|inherit
        if self.display=="vlist":
            if self.ovy=="auto"or self.ovy=="scroll":
                self.vscrollredraw(surfacein)
            else:
                self.vredraw(surfacein)

        if self.display=="hlist":
            if self.ovx=="auto" or self.ovx=="scroll":
                self.hscrollredraw(surfacein)
            else:
                self.hredraw(surfacein)

        if self.display=="u-dwrap":
            if self.ovx=="auto" or self.ovx=="scroll" or self.ovy=="auto" or self.ovy=="scroll":
                self.u_dwrapscrollredraw(surfacein)
            else:
                self.u_dwrapredraw(surfacein)

        if self.display=="r-lwrap":
            if self.ovx=="auto" or self.ovx=="scroll" or self.ovy=="auto" or self.ovy=="scroll":
                self.r_lwrapscrollredraw(surfacein)
            else:
                self.r_lwrapredraw(surfacein)

    def styleize(self,style):
        super(listWidget, self).styleize(style)

    def __init__(self, id, parent, style, data):
        self.scrollx = sliderWidget(id=id+"-scrollx", parent=None, style={
        "Background":"dgrey",
        "H":8,
        "InactiveColor":"grey",
        "ActiveColor":"lgrey",
        "Slider":{
            "x":0,
            "w":"(self.owner.w)",
            "h":0,
            "y":0,
            "dw":0,
            "wo":0,
            "dh":0,
            "ho":0,
            "inc":1,
            "drawinc":5,
            "notch":[]
        }}, data={"Test"})
        self.scrollx.owner=self
        self.scrolly = sliderWidget(id=id+"-scrolly", parent=None, style={
        "Background":"dgrey",
        "W":8,
        "InactiveColor":"grey",
        "ActiveColor":"lgrey",
        "Slider":{
            "x":0,
            "w":0,
            "h":"(self.owner.h)",
            "y":8,
            "dw":0,
            "wo":8,
            "dh":8,
            "ho":12,
            "inc":1,
            "drawinc":5,
            "notch":[]
        }}, data={"Test"})
        self.scrolly.owner=self
        self.barx = emptyWidget(id=id+"-BarX", parent=self.scrollx, style={
        "Text":"",
        "Color":"black",
        "H":8,
        "W":None,
        "Background":"grey",
        "Round":(5,5,5,5)
        })
        self.bary = emptyWidget(id=id+"-BarY", parent=self.scrolly, style={
        "Text":"",
        "Color":"black",
        "W":8,
        "H":32,
        "Background":"grey",
        "Round":(5,5,5,5)
        })

        super(listWidget, self).__init__(id,parent,style,data)

class vlistWidget(listWidget):

    """docstring for Vertical List."""

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.style = {
        "H":"self.vfitchildren()",
        "W":"self.hlargest()"
        }
        super(vlistWidget, self).__init__(id,parent,style,data)
        self.display = "vlist"

class hlistWidget(listWidget):
    """docstring for List."""

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.style = {
        "W":"self.hfitchildren()",
        "H":"self.vlargest()"
        }
        super(hlistWidget, self).__init__(id,parent,style,data)
        self.display = "hlist"

class wraplistWidget(listWidget):
    """docstring for List."""

    def __init__(self,id=randid,parent="main",style={},data={},wrapwidth=-1):
        self.style = {
        "W":"self.wraplargestw()",
        "H":"self.wraplargesth()"
        }
        self.wrapwidth = wrapwidth
        super(wraplistWidget, self).__init__(id,parent,style,data)

class absDrawWidget(widget):
    def redrawInBox(self,surfacein):
        global drawy
        global drawx
        self.styleize(self.style)

        for x in self.children:
            x.y = x.absy
            x.x = x.absx
            drawy = x.absy
            drawx = x.absx
            x.redraw(surfacein)

        self.drawPopouts(surfacein)
    """docstring for List."""

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()"
        }
        super(absDrawWidget, self).__init__(id,parent,style,data)

class overlayWidget(widget):
    def redrawInBox(self, surfacein):
        global drawy
        global drawx
        self.styleize(self.style)
        for x in self.children:
            x.y = drawy
            x.x = drawx
            x.redraw(surfacein)
            drawx = self.x
            drawy = self.y
        drawx = self.x
        drawy = self.y

        #super(overlayWidget, self).redraw(surfacein)

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()"
        }
        super(overlayWidget, self).__init__(id,parent,style,data)

class selectWidget(widget):

    def vfitchildren(self):
        return self.vlargest()

    def hlargest(self):
        #print(self.id)
        #print(self.w)
        try:
            v = eval(self.condition)
        except Exception as e:
            #print(e)
            v = "All"
        if v == "All":
            #print(v)
            for x in self.children:
                #print(x.w)
                if self.w < x.w:
                    self.w = x.w
        elif v != None:
            if len(self.children)>v:
                self.w = self.children[v].w
        else:
            self.w = 0
        #print(self.w)
        return self.w

    def hfitchildren(self):
        #print(self.id)
        return hlargest()

    def vlargest(self):
        h=self.h
        try:
            v = eval(self.condition)
        except Exception as e:
            #print(e)
            v = "All"
        if v == "All":
            #print(v)
            for x in self.children:
                if h < x.h:
                    h = x.h
        elif v != None:
            if len(self.children)>v:
                h = self.children[v].h
        else:
            h = 0
        #print(self.h)
        return h

    def prossesinputs(self,eventname,event,surface,lglobals=None):
        if self.condition != None:
            try:
                v = eval(self.condition)
            except Exception as e:
                #print(e)
                v = "All"
            if v == "All":
                #print(v)
                super(selectWidget, self).prossesinputs(eventname,event,surface,lglobals)
            elif v != None:
                if len(self.children)>v:
                    x = self.children[v]
                    x.prossesinputs(eventname,event,surface,lglobals)

    def redrawInBox(self,surfacein):
        if self.condition != None:
            try:
                v = eval(self.condition)
            except Exception as e:
                #print(e)
                v = "All"
            if v == "All":
                #print(v)
                super(selectWidget, self).redrawInBox(surfacein)
            else:
                if len(self.children)>v:
                    x = self.children[v]
                    self.children[v].redraw(surfacein)
                    self.w = x.w
                    self.h = x.h
        else:
                self.w = 0
                self.h = 0
            #print(self.h)
        #super(selectWidget, self).redrawInBox(surfacein)

    def __init__(self, id,parent,condition="",style={},data={}):
        self.condition = condition
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()"
        }
        super(selectWidget, self).__init__(id,parent,style,data)
        #print(self.h)

class drawSwitchWidget(selectWidget):
    def __init__(self, id, parent, value="", style={}):
        self.value = value
        condition = "0 if self.calc(self.value) else 1"
        super(drawSwitchWidget, self).__init__(id, parent, condition, style={})

class dragWidget(widget):

    def prossesinputs(self,eventname,event,surface,globals):
        global dragging
        super(dragWidget,self).prossesinputs(eventname,event,surface,globals)
        if eventname == "Mousemove":
            ex = event.pos[0]
            ey = event.pos[1]
            #print(event.pos)
            #print((self.x,self.y,self.w,self.h) )
            o = surface.get_abs_offset()
            #print(o)
            #print(self.h)
            if self.ispressing:
                #print(self.lx,self.ly)
                self.dx = ex+self.lx
                self.dy = ey+self.ly
            else:
                self.dx = self.x
                self.dy = self.y
            if self.testState("hover"):
                #print("HI")
                self.mouseover = True
            else:
                #if self.changed:
                #    self.changed = True
                self.mouseover = False
        elif eventname == "Mousedown" and self.mouseover:
            ex = event.pos[0]
            ey = event.pos[1]
            self.lx = self.x-ex
            self.ly = self.y-ey
            self.ispressing = True
            dragging = self
        elif eventname == "Mouseup":
            self.ispressing = False
        elif eventname == "Mouseleave":
            self.ispressing = False

    def redrawInBox(self,surfacein):
        global drawx
        global drawy
        self.styleize(self.style)
        if self.spawned == True:
            self.x = drawx
            self.y = drawy
            self.dx = drawx
            self.dy = drawy
            self.spawned = False
        for x in self.children:
            x.y = self.dy
            x.x = self.dx
            drawx = self.dx
            drawy = self.dy
            x.redraw(surfacein)
        drawx = self.x
        drawy = self.y

    def __init__(self, id,parent,style={},data={}):
        self.dy = 0
        self.dx = 0
        self.lx = 0
        self.ly = 0
        self.spawned = True
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()"
        }
        super(dragWidget, self).__init__(id,parent,style,data)

class dragSnaplessWidget(dragWidget):

    def prossesinputs(self,eventname,event,surface,globals):
        global dragging
        super(dragWidget,self).prossesinputs(eventname,event,surface,globals)
        if eventname == "Mousemove":
            ex = event.pos[0]
            ey = event.pos[1]
            #print(event.pos)
            o = surface.get_abs_offset()
            if self.ispressing:
                self.dx = ex+self.lx
                self.dy = ey+self.ly
            if (
            self.w+o[0]+self.dx > ex > o[0]+self.dx
            and
            self.h+o[1]+self.dy > ey > o[1]+self.dy):
                #print("HI")
                self.mouseover = True
            else:
                #if self.changed:
                #    self.changed = True
                self.mouseover = False
        elif eventname == "Mousedown" and self.mouseover:
            ex = event.pos[0]
            ey = event.pos[1]
            self.lx = self.dx-ex
            self.ly = self.dy-ey
            self.ispressing = True
        elif eventname == "Mouseup":
            self.ispressing = False
        elif eventname == "Mouseleave":
            self.ispressing = False

class dropWidget(widget):

    def prossesinputs(self,eventname,event,surface,globals):
        global dragging
        super(dropWidget,self).prossesinputs(eventname,event,surface,globals)
        if eventname == "Mouseup":
            o = surface.get_abs_offset()
            ex = event.pos[0]
            ey = event.pos[1]
            if (
            self.w+o[0]+self.x > ex > o[0]+self.x
            and
            self.h+o[1]+self.y > ey > o[1]+self.y
            and dragging != None
            ):
                dragging.parentref.children.remove(dragging)
                dragging.parentref = self
                self.children.append(dragging)
                dragging.dx = self.x
                dragging.dy = self.y
                dragging = None
            self.ispressing = False

    def redrawInBox(self,surfacein):
        try:
            v = eval(self.condition)
        except:
            v = "All"
        if v == "All":
            super(dropWidget, self).redrawInBox(surfacein)
        elif len(self.children)>v:
            self.children[v].redraw(surfacein)

    def __init__(self, id,parent,style={},data={}):
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()"
        }
        super(dropWidget, self).__init__(id,parent,style,data)

class floatyBoxWidget(dragSnaplessWidget,popoutWidget):
    def prossesinputs(self,eventname,event,surface,globals):
        global dragging
        super(dragWidget,self).prossesinputs(eventname,event,surface,globals)
        if eventname == "Mousemove":
            ex = event.pos[0]
            ey = event.pos[1]
            #print(event.pos)
            #print((self.x,self.y,self.w,self.h) )
            o = surface.get_abs_offset()
            if self.ispressing:
                self.dx = ex+self.lx
                self.dy = ey+self.ly
            if (
            self.w+o[0]+self.dx > ex > o[0]+self.dx
            and
            self.h+o[1]+self.dy > ey > o[1]+self.dy):
                #print("HI")
                self.mouseover = True
            else:
                #if self.changed:
                #    self.changed = True
                self.mouseover = False
        elif eventname == "Mousedown" and self.mouseover:
            ex = event.pos[0]
            ey = event.pos[1]
            self.lx = self.dx-ex
            self.ly = self.dy-ey
            self.ispressing = True
        elif eventname == "Mouseup":
            self.ispressing = False
        elif eventname == "Mouseleave":
            self.ispressing = False

    def redraw(self,surfacein):
        pass

    def redrawpopout(self,surfacein):
        global drawy
        global drawx
        self.styleize(self.style)
        drawy = self.dy
        drawx = self.dx
        for x in self.children:
            x.y = self.dy
            x.x = self.dx
            drawy = self.dy
            drawx = self.dx
            x.redraw(surfacein)

# Inputs    8

class buttonWidget(widget):
    def prossesinputs(self,eventname,event,surface,globals):
        super(buttonWidget,self).prossesinputs(eventname,event,surface,globals)
        if eventname == "Mousemove":
            ex = event.pos[0]
            ey = event.pos[1]
            #print(event.pos)
            #print((self.x,self.y,self.w,self.h) )
            #print(self)
            o = surface.get_abs_offset()
            #print(o)  self.x+self.w+o[0] > ex > self.x+o[0] and self.y+self.h+o[1] > ey > self.y+o[1]
            if self.testState("hover"):
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
                exec(self.action,globals,locals())
            self.ispressing = True
        elif eventname == "Mouseup":
            self.ispressing = False
        elif eventname == "Mouseleave":
            self.ispressing = False

    """A Button Widget"""
    def redrawInBox(self,surfacein):
        #self.draworign(surfacein)
            #print(mouse)
            #print( (self.x,self.y,self.w,self.h) )
            #print( (self.x,self.y,self.w,self.h) )
            #print("H"+str(self.h))
            #print(self.w)
        if self.changed:
                if self.mouseover or self.active:
                    self.dbackground = self.activecolor
                else:
                    self.dbackground = self.inactivecolor
        super(buttonWidget, self).redrawInBox(surfacein)

    def __init__(self,id=randid,parent="main",action="",style={},data={}):
        self.action = action
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()",
        "Background":"self.dbackground"
        }
        super(buttonWidget, self).__init__(id,parent,style,data)
        self.dbackground = self.inactivecolor

class switchWidget(buttonWidget):
    def switch(self):
        self.active = not self.active

    """A Switch Widget"""

    def __init__(self,id=randid,parent="main",action="",style={},data={}):
        self.action = "self.switch()"
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()",
        "Background":"self.dbackground"
        }
        super(buttonWidget, self).__init__(id,parent,style,data)
        self.dbackground = self.inactivecolor

class textBoxWidget(widget):
    def textbox(self,num):
        if self.textRect[2] > num:
            return self.textRect[2]
        else:
            return num

    def activate(self):
        self.active = True

    def prossesinputs(self,eventname,event,surface,globals):
        #print( "event")
        super(textBoxWidget,self).prossesinputs(eventname,event,surface,globals)
        if eventname == "Mousemove":
            ex = event.pos[0]
            ey = event.pos[1]
            #print(event.pos)
            #sssssprint((self.x,self.y,self.w,self.h) )
            o = surface.get_abs_offset()
            #print(o)

            if self.x+self.w+o[0] > ex > self.x+o[0] and self.y+self.h+o[1] > ey > self.y+o[1]:
                #print("HI")
                self.mouseover = True
                self.changed = True
            else:
                if self.changed:
                    self.changed = True
                    #self.active = False
                self.mouseover = False
        elif eventname == "Mousedown" and self.mouseover:
            if not self.ispressing:
                #print("Action"+str(self.action))
                exec(self.action)
            self.ispressing = True
        elif eventname == "Mousedown" and not self.mouseover:
            self.active = False
        elif eventname == "Mouseup":
            self.ispressing = False
        elif eventname == "Keydown":
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.mytext = self.mytext[0:-1]
                elif event.key == pygame.K_TAB:
                    self.mytext += "   "
                elif event.key == pygame.K_DELETE:
                    self.mytext = ""
                elif event.key == pygame.K_ESCAPE:
                    self.active = False
                else:
                    self.mytext += str(event.unicode)
        elif eventname == "Mouseleave":
            self.ispressing = False
        #self.styleize(self.style)

    """A Text Input Box Widget"""
    def redrawInBox(self,surfacein):
        #action = self.action
        #print( (self.x,self.y,self.w,self.h) )
        #print( (self.x,self.y,self.w,self.h) )
        #print("H"+str(self.h))
        #print(self.w)
        #textRect = None
        #textSurface = None
        if self.active:
            self.dbackground = self.activecolor
        else:
            self.dbackground = self.inactivecolor
        super(textBoxWidget, self).redrawInBox(surfacein)
        #if textSurface != None  and textRect != None:
        #    surfacein.blit(textSurface, textRect)

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.textRect = (0,0,0,0)
        self.action = "self.activate()"
        self.mytext = ""
        self.dbackground = None
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()"
        }
        super(textBoxWidget, self).__init__(id,parent,style,data)

class sliderWidget(widget):

    def prossesinputs(self,eventname,event,surface,globals):
        super(sliderWidget,self).prossesinputs(eventname,event,surface,globals)
        if eventname == "Mousemove":
            ex = event.pos[0]
            ey = event.pos[1]
            #print(event.pos)
            #print((self.x,self.y,self.w,self.h) )
            o = surface.get_abs_offset()
            #print(o)
            if self.ispressing:
                lgx = self.gx
                lex = ex + lgx - self.x
                if lex > 0:
                    if lex + self.hlargest() < self.w :
                        lex = lex
                    else:
                        lex = self.w - self.hlargest()
                else:
                    lex = 0
                self.rx = round(lex/self.slider["inc"])*self.slider["inc"]
                lgy = self.gy
                ley = ey + lgy - self.y
                if ley > 0:
                    if ley + self.vlargest()< self.h:
                        ley = ley
                    else:
                        ley = self.h - self.vlargest()
                else:
                    ley = 0
                self.ry = round(ley/self.slider["inc"])*self.slider["inc"]
            if self.testState("slidehover"):
                self.mouseover = True
            else:
                self.mouseover = False
        elif eventname == "Mousedown" and self.mouseover:
            self.gx =  self.x - event.pos[0] + self.rx
            self.gy =  self.y - event.pos[1] + self.ry
            self.ispressing = True
        elif eventname == "Mouseup":
            self.ispressing = False
        elif eventname == "Mouseleave":
            self.ispressing = False
            self.mouseover = False

    """A Slider Widget"""
    def redrawInBox(self,surfacein):
        #action = self.action
            #print( (self.x,self.y,self.w,self.h) )
            #print( (self.x,self.y,self.w,self.h) )
            #print("H"+str(self.h))
        self.styleize(self.style)
        #print(self.slidenotch)
        if self.slider["inc"] > 0 and "w" in self.slider["notch"]:
                #print("startticks")
                r = (self.w)/self.slider["drawinc"]
                r = round(r-.5)
                r = range(0,r)
                for i in r:
                    pygame.draw.rect(surfacein, (255,0,0),(
                    self.x + ((i+1)*self.slider["drawinc"]),
                    self.y - (self.h/10),
                    1,
                    self.h + (self.h/5)
                    ))
        if self.slider["inc"] > 0 and "h" in self.slider["notch"]:
                #print("startticks")
                r = (self.h)/self.slider["drawinc"]
                r = round(r-.5)
                r = range(0,r)
                for i in r:
                    pygame.draw.rect(surfacein, (255,0,0),(
                    self.x - (self.w/10),
                    self.y + ((i+1)*self.slider["drawinc"]),
                    self.w + (self.w/5),
                    1
                    ))
        global drawy
        global drawx
        drawx = self.rx+self.x
        drawy = self.ry+self.y
        #print(self.x,self.y,self.w,self.h,self.rx,self.ry,self.gx,self.gy)
        for x in self.children:
            x.y = drawy
            x.x = drawx
            x.redraw(surfacein)

        drawx = self.x
        drawy = self.y

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.action = ""
        self.gx=0
        self.gy=0
        super(sliderWidget, self).__init__(id,parent,style,data)

class checkWidget(switchWidget):

    """A Check Box Widget"""
    def redrawInBox(self,surfacein):
        action = self.action
            #print(mouse)
            #print( (self.x,self.y,self.w,self.h) )
            #print( (self.x,self.y,self.w,self.h) )
            #print("H"+str(self.h))
            #print(self.w)
        super(checkWidget, self).redrawInBox(surfacein)
        if self.active:
            self.img = pygame.transform.scale(self.img, (int(self.w), int(self.h)))
            surfacein.blit(self.img,(self.x,self.y))

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.action = "self.switch()"
        path = pathlib.Path(__file__).parent.resolve()
        imgpath = pathlib.PurePath(path,"assets/checkmarksmall.png")
        self.style = {
        "Image":imgpath,
        "Background":"self.dbackground"
        }
        super(buttonWidget, self).__init__(id,parent,style,data)

class radioWidget(buttonWidget):
    def radioio(self):
        p = self.parentref
        c = p.children
        for r in c:
            if type(r) == type(self):
                r.active = False
        p.radiovalue = self.id
        self.active = True

    """A Radio Button Widget"""

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.action = "self.radioio()"
        self.style = {
        "W":"self.hlargest()",
        "H":"self.vlargest()",
        "Background":"self.dbackground"
        }
        super(buttonWidget, self).__init__(id,parent,style,data)
        self.dbackground = self.inactivecolor

class dropdown(widgetCollection):

    def addoption(self,text):
        #print(self.vl)
        r = radioWidget(id=text, parent=self.vl, style={"W":64,"H":32}, data={})
        #print(r.parent)
        textWidget(id=text+"-t", parent=r, style={
        "Text":text,
        "Background":None
        }, data={})

    def open(self):
        x = self.l.find(str(self.id)+"-s")
        if x.condition == None:
            x.condition = "All"
        else:
            x.condition = None

    def create(self, id, parent):
        self.id = id
        ov = vlistWidget(id=id, parent=parent, style={"ABSX":"drawx","ABSY":"drawy"}, data={"HI":"o"})
        #ov.out = True
        #print(ov.parentref)
        l = vlistWidget(id=str(id)+"-ml",parent=ov,style={
        "H":"self.vfitchildren()",
        "W":"self.hlargest()"
        },data={
        "HI":"HI"
        })
        self.l = l
        but = buttonWidget(id=str(id)+"-b", parent=l, action=
        """self.data["dropdown"].open()"""
        , style={
        "W":"64",
        "H":"32",
        "InActiveColor":"lgrey",
        "ActiveColor":"grey"
        },data={"dropdown":self})
        textWidget(id=str(id)+"-bt", parent=but, style={
        "Text":"self.vl.radiovalue",
        "Background":None
        }, data={})
        sw = selectWidget(id=str(id)+"-s", parent=l,
        condition=None, style={

        },data={})
        vl = vlistWidget(id=str(id)+"-vl",parent=sw,style={
        "H":"self.vfitchildren()",
        "W":"self.hlargest()"
        },data={"H":"HI"})
        self.vl = vl
        vl.radiovalue = self.defualt
        textWidget.vl = vl

    def __init__(self, id, parent, defualt=""):
        self.defualt = defualt
        super(dropdown, self).__init__(id, parent)

# Image / Decorative   5

class imageWidget(widget):
    """A Image Widget"""
    def redrawInBox(self,surfacein):
        global drawy
            #print(mouse)
            #print( (self.x,self.y,self.w,self.h) )
            #print( (self.x,self.y,self.w,self.h) )
            #print("H"+str(self.h))
            #print(self.w)
        #print(self.id,(self.x,self.y,self.w,self.h),(drawx,drawy))
        if self.changed:
            if hasattr(self,"img") :
                imgc = self.img
                imgc = pygame.transform.scale(imgc, (int(self.w), int(self.h)))
                imgc,imgr = rot_center(imgc, imgc.get_rect(), self.angle)
                #imgr.center(self.img)
                self.imgr = imgr
                surfacein.blit(imgc,(self.x+imgr[0],self.y+imgr[1]))
        super(imageWidget, self).redrawInBox(surfacein)

    def __init__(self,id=randid,parent="main",style={},data={}):
        self.style = {
        "W":"self.imgr[2]",
        "H":"self.imgr[3]"
        }
        super(imageWidget, self).__init__(id,parent,style,data)

class canvasWidget(widget):

    def copy(self,newid=randid,newparent=None):
        global randid
        randid+=1
        if newparent == None:
            newparent = self.parentref
        o = type(self)(id=newid, parent=newparent, style=self.style)
        #print(self.draws)
        o.draws = self.draws.copy()
        #print(o.draws)
        for c in self.children:
            c.copy(randid,o)
        return o

    def draw(self,type,color,points,width):
        self.draws.append((type,color,points,width))
        self.redrawtime = True

    def redrawInBox(self, surfacein):
        global drawy
        global drawx
        if self.redrawtime:
            try:
                self.mysurface = pygame.Surface((self.w,self.h))
                self.mysurface = self.mysurface.convert_alpha()
                self.mysurface.fill((0,0,0,0))
                self.mysurface.lock()
                self.redrawtime = False
        #print(self.x,self.y)
                #print(self.draws)
                for d in self.draws:
                    if d[0] == "Line":
                        x1 = d[2][0][0]
                        y1 = d[2][0][1]
                        x2 = d[2][1][0]
                        y2 = d[2][1][1]
                        #print((x1,y1),(x2,y2))
                        pygame.draw.line(self.mysurface, d[1],(x1,y1),(x2,y2),d[3] )
                    if d[0] == "Arc":
                        x = d[2][0][0]
                        y = d[2][0][1]
                        h = d[2][0][2]
                        w = d[2][0][3]
                        pygame.draw.arc(self.mysurface, d[1], (x,y,w,h), d[2][1], d[2][2], d[3])
                    if d[0] == "Ellipse":
                        x = d[2][0]
                        y = d[2][1]
                        h = d[2][2]
                        w = d[2][3]
                        pygame.draw.ellipse(self.mysurface,d[1],(x,y,w,h),d[3])
                    if d[0] == "Polygon":
                        ps = []
                        for p in d[2]:
                            x = p[0]
                            y = p[1]
                            ps.append((x,y))
                        pygame.draw.polygon(self.mysurface, d[1], ps, d[3])
                self.changed = False
                self.mysurface.unlock()
                surfacein.blit(self.mysurface,(drawx,drawy))
            except Exception as e:
                #print(e)
                pass
        else:
            surfacein.blit(self.mysurface,(drawx,drawy))
        self.styleize(self.style)
        #super(overlaywidget, self).redrawInBox(surfacein)

    def __init__(self,id,parent,x=0,y=0,w=256,h=256,style={},data={}):
        self.draws = []
        self.redrawtime = True
        super(canvasWidget, self).__init__(id, parent, style)

class graphWidget(widget):
    def copy(self,newid=randid,newparent=None):
        global randid
        randid+=1
        if newparent == None:
            newparent = self.parentref
        o = type(self)(id=newid, parent=newparent, style=self.style)
        o.pxs = self.pxs.copy()
        o.pys = self.pys.copy()
        o.lxs = self.lxs.copy()
        o.lys = self.lys.copy()
        for c in self.children:
            c.copy(randid,o)
        return o

    def point(self,x,y):
        self.pxs.append(x)
        self.pys.append(y)
        self.plotchanged = True

    def linepoint(self,x,y):
        self.lxs.append(x)
        self.lys.append(y)
        self.plotchanged = True

    def redrawInBox(self, surfacein):
        global drawy
        global drawx
        self.styleize(self.style)
        if self.plotchanged:
            fig = pylab.figure(
            figsize=[self.w/96, self.h/96],
            dpi=100,
            )
            ax = fig.gca()
            ax.plot(self.pxs,self.pys,'o')
            ax.plot(self.lxs,self.lys)
            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()
            size = canvas.get_width_height()
            self.grid = pygame.image.fromstring(raw_data, size, "RGB")
            surfacein.blit(self.grid, (self.x,self.y))
            self.styleize(self.style)
            self.plotchanged = False
        else:
            surfacein.blit(self.grid, (self.x,self.y))
        #super(overlaywidget, self).redrawInBox(surfacein)

    def __init__(self,id,parent,style={},data={}):
        self.pxs = []
        self.pys = []
        self.lxs = []
        self.lys = []
        self.grid = None
        self.plotchanged = True
        super(graphWidget, self).__init__(id, parent, style)

class emptyWidget(widget):
    pass

class dataWidget(widget):

    def prossesinputs(self,eventname,event,surface,globals):
        pass
        #super(noneWidget, self).prossesinputs(eventname, event, surface, self.globals)

    def redraw(self,surfacein):
        pass
        #super(noneWidget, self).redrawInBox(surfacein)


#print(len(widget.__subclasses__()))

try:
    path = pathlib.Path(__file__).parent.resolve()
    sourcepath  = pathlib.Path(__file__).parent.resolve()
except Exception as e:
    print(e)

def Font(fontFace, size):
    return pygame.font.Font(fontFace, round(size))

looping = True

clock = pygame.time.Clock()

variablestr = """str(str(sl.ry)+","+str(sl.rx))"""
text = "Hello"
path = pathlib.Path(__file__).parent.resolve()
#print(path)
img_file = "./assets/pythonicon.png"
variabletest = 0
