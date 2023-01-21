try:
    from . import colors
    from .colors import *
except:
    from colors import *

try:
    from . import css
except:
    import css


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

globallink = {}

parser = css.cssparser()

def setParser(input):
    global parser
    parser = input

path = pathlib.Path(__file__).parent.resolve()

def setGlobalLink(input):
    global globallink
    globallink = input

class Styleizor():
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
        for k in style:
            if k not in self.ignore:
                x = self.getstyle(k)
                if x != None:
                    x = self.calc(x)
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

    def wrapfith(self):
        #print(h)
        return self.wrapedwidth


# End Style

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

    def copy(self,newid="",newparent=None):
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

    def testState(self,state,surface):
        if state=="hover":
            ex,ey = pygame.mouse.get_pos()
            x,y = surface.get_abs_offset()
            #print(ex)
            #print(self.rx,self.x)
            b = (
            self.rx+self.w+self.x+x > ex > self.rx+self.x+x
            and
            self.ry+self.h+self.y+y > ey > self.ry+self.y+y
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
            #print(ex,ey)
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
        #print(v)
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

    def _init_(self,style):
        self.style = style


class widget(Styleizor):

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
        if lglobals==None:
            lglobals = globals().copy()
            lglobals.update(globallink)
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

    def drawBorderNoBox(self,surfacein):
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
        if self.useboxmodel:
            self.redrawBoxModel(surfacein)
        else:
            self.redrawNoBox(surfacein)

    def redrawNoBox(self,surfacein):
        global drawx
        global drawy
        orx=drawx
        ory=drawy
        self.styleize(self.style)
        self.entermargins()
        self.drawInterior(surfacein)
        self.padcontent()
        self.shiftContent()
        self.redrawInBox(surfacein)
        self.unpadcontent()
        self.unpadcontent()
        self.drawBorderNoBox(surfacein)
        self.exitmargins()
        drawy=ory
        drawx=orx

    def redrawBoxModel(self,surfacein):
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

    def shiftContent(self):
        global drawx
        global drawy
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

    def initialvalues(self):
        self.h = 0
        self.w = 0
        self.wrapedhight = 0
        self.wrapedwidth = 0
        self.y = 0
        self.radiovalue = ""
        self.notifys = []
        self.popouts = []
        self.rx = 0
        self.ry = 0
        self.ovy = "visible"
        self.ovx = "visible"
        self.x = 0
        self.out = False
        self.children = []
        self.child = ""
        self.sibling = ""
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
        self.wrap = -1
        self.image = "./assets/pythonicon.png"
        self.imgr = (0,0,0,0)
        self.absx = 0
        self.absy = 0
        self.lastgradient = "Blahb"
        self.display="vlist"
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
        fontpath = str(pathlib.PurePath(path,"assets/Xolonium-Bold.ttf"))
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
        self.useboxmodel = True
        #print(parent)

    def preinit(self,id,parent,style={},data={}):
        self.id = id
        self.parent = parent
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

    def __init__(self, id="", parent=None,style={},data={}):
        self.preinit(id,parent,style,data)
        self.initialvalues()
        self.add(parent)
        self.lookup(parser)
        self.styleize(style)
