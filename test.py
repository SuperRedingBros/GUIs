import guis.guis
from guis.guis import *
import pygame
import guis.htmltogui as htmltogui

# TODO:
#
#  https://pypi.org/project/pyttsx3/
#
#  https://pypi.org/project/SpeechRecognition/
#


usefull = False
dw = 1280
dh = 560
ldw = 1280
ldh = 560
variabletest = 0
looping=True
clock = pygame.time.Clock()

def renderframe(events,display,skipevents=False,screen=None):
    #print("frame")
    global dw
    global dh
    if not skipevents:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                screen.prossesinputs("Keydown",event,display,globals())
            if event.type == pygame.KEYUP:
                screen.prossesinputs("Keyup",event,display,globals())
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.prossesinputs("Mousedown",event,display,globals())
            if event.type == pygame.MOUSEMOTION:
                screen.prossesinputs("Mousemove",event,display,globals())
            if event.type == pygame.MOUSEBUTTONUP:
                screen.prossesinputs("Mouseup",event,display,globals())
            if event.type == pygame.FINGERDOWN:
                pass
            if event.type == pygame.FINGERUP:
                pass
            if event.type == pygame.VIDEORESIZE:
                s = pygame.display.get_window_size()
                guis.dw = s[0]
                guis.dh = s[1]
                display.fill((0,0,0))
                pygame.display.update()
            if  event.type == WINDOWLEAVE:
                screen.prossesinputs("Mouseleave",event,display,globals())

    #pygame.display.update()
    screen.redraw(display)

def render():
    global looping
    guis.globallink = globals()
    while looping:
        global variablestr
        global variabletest
        #Quit on clicking the "X" in the corner, or by pressing the escape + enter key.
        variabletest += .5
        clock.tick(60)
        #variablestr = str(round(variabletest))
        #variabletest+=1
        renderframe( pygame.event.get(),gameDisplay,screen=screen )
        screen.update()
        pygame.display.update()
        #pygame.time.wait(1500)
        variabletest += .5
        #print("Tick",clock.get_time())
        #print(vl.countchildren())
    pygame.quit()

if __name__ == '__main__':
    if usefull:
        gameDisplay = pygame.display.set_mode((ldw, ldh), pygame.FULLSCREEN,pygame.RESIZABLE )
        s = pygame.display.get_window_size()
        dw = s[0]
        dh = s[1]
    else:
        gameDisplay = pygame.display.set_mode((ldw, ldh),pygame.RESIZABLE)
    s = pygame.display.get_window_size()
    dw = s[0]
    dh = s[1]
    pygame.display.set_caption('GUI Tests')

if __name__ == '__main__' and False:
    screen = guis.mainWidget(pygame,"red",style={},data={})
    hl1 = guis.wraplistWidget("Hi2",screen,style={
    "Background":"dyellow",
    "Border":{
    "color":"white",
    "width":-1,
    "round":1
    }},data={},wrapwidth=550)
    hl2 = guis.wraplistWidget("Hi2",hl1,style={
    "Background":"yellow",
    "Border":{
    "color":"blue",
    "width":5,
    "round":1
    }},data={},wrapwidth=550)
    helloworld = guis.textWidget(id="Hello", parent=hl1,style={
    "Text":"Hello World Time",
    "Justification":"left top",
    "Wrap":172,
    "Padding":(0,0,0,0),
    "Background":None,
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":1,
    "round":1
    }
    })
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl2)
    helloworld.copy(newid="randid", newparent=hl2)
    helloworld.copy(newid=randid, newparent=hl2)
    helloworld.copy(newid="randid", newparent=hl2)
    #vlistWidget("Hi3","Hi2",0,0,red,grey,style={"W":"self.hfill()"})
    #surfaceWidget("HI",25,25,25,25,"main",white)
    #c.draw("Line",(255,0,0),((0,0),(25,25)),25)
    #c.draw("Arc",(255,0,0),((25,25,55,55),math.radians(25),math.radians(255)),5)
    #c.draw("Ellipse",(255,0,0),((55,55,55,55)),10)
    render()
    #imageWidget(id="Image",parent="Hi",x=0,y=0,color=white,activecolor=white,
    #text="Hi",image="assets/checkmark.png",style={"H":dh,"W":dw})
    quit()

if __name__ == '__main__' and False:
    screen = mainWidget(pygame,"purple",style={},data={})
    vl = vlistWidget(id="Hi12", parent=screen, style={})
    #vl.ignore=["Border"]
    hl1 = wraplistWidget("Hi2",vl,style={},data={},wrapwidth=256)
    hl2 = hlistWidget("Hi123",vl,style={},data={})
    n = noneWidget(id="None")
    popout = floatyBoxWidget(id="Popout", parent=screen, style={
    "H":16
    })
    vl7 = vlistWidget(id="Hi12", parent=popout, style={
    "Background":"grey",
    "W":512,
    "H":256
    })
    helloworld0 = textWidget(id="Hello", parent=vl7,style={
    "Text":"Hello World Time",
    "Justification":"left top",
    "W":"72",
    "H":"72",
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":-1,
    "round":1
    },
    "Gradient":{
        "base":(255,0,255),
        "end":(0,0,0),
        "types":"text",
        "inverse":False,
        "vert":True,
        "flip":False
    }
    })
    sw2 = switchWidget(id="Switch",parent=vl7,style={
    "W":32,
    "H":32,
    "Round":(16,16,16,16),
    "ActiveColor":"lred",
    "Background":"white",
    "Gradient":{
        "base":"red",
        "end":"yellow",
        "types":["background"],
        "inverse":"self.active",
        "vert":False,
        "flip":False
    }
    })
    cb2 = checkWidget(id="Check",parent=vl7,style={
    "W":64,
    "H":64
    })
    b = buttonWidget(id="Button", parent=vl7, action="popout.out = False", style={
    "W":64,
    "H":32
    })
    textWidget(id="Text", parent=b,style={
    "Text":"Ok.",
    "Color":"black",
    "Background":None,
    "W":64,
    "H":32
    })

    emptyWidget(id="Empty", parent=vl, style={
    "W":64,
    "H":32
    }, data={})

    dr = dropdown("Test", vl, "Hello")
    dr.addoption("Hello")
    dr.addoption("Hi")
    dr.addoption("Hola")
    dr.addoption("Aloha")
    buttonWidget(id="Button", parent=vl, action="popout.out = True", style={
    "W":64,
    "H":32
    })
    counter = textWidget(id="HelloCounter", parent=hl1,style={
    "Text":
    """text""",
    "W":"64",
    "H":"64",
    "Wrap":104,
    "Color":"white",
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Background":(255,2,2),
    "Justification":"left top",
    "Gradient":{
        "base":(155,125,0),
        "end":(55,0,0),
        "types":"background",
        "inverse":True,
        "vert":False,
        "flip":False
    }
    },data={"Break":False,"Load":'L'})
    helloworld = textWidget(id="Hello", parent=hl1,style={
    "Text":"Hello World Time",
    "Justification":"left top",
    "W":"172",
    "H":"72",
    "Wrap":128,
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    },
    "Gradient":{
        "base":(255,0,255),
        "end":(0,0,0),
        "types":"text",
        "inverse":False,
        "vert":True,
        "flip":False
    }
    })
    helloworld.copy(newid=randid)
    sl = sliderWidget(id="Slider", parent=vl, style={
    "W":512,
    "H":72,
    "Background":"grey",
    "Slider":{
        "x":0,
        "w":130,
        "h":0,
        "y":0,
        "dw":8,
        "dwo":12,
        "dh":8,
        "dho":12,
        "inc":1,
        "drawinc":5,
        "notch":""
    }
    })
    hlw1 = hlistWidget(id="Arc List", parent=vl, style={})
    ov = overlayWidget("Indicator", parent=hlw1, style={})
    imbs = textWidget(id="HelloTwo", parent=ov, style={
    "Text":"",
    "Color":"black",
    "W":64,
    "H":64,
    "Background":"grey",
    "Round":(32,32,32,32)
    })
    arcp = arcProgressWidget(id="Arc", parent=ov,style={
    "Text":"variablestr",
    "W":64,
    "H":64,
    "Background":None,
    "Color":"red",
    "FillValue": """sl.rx/sl.w""",
    "Maxangle":360,
    "Angle":-90,
    "Flip":False,
    "Image":"self.arrowwhite"
    })
    arcc = canvasWidget("Canvas", parent=ov, style={
    "W":64,
    "H":64,
    "Background":None
    })
    arcc.draw("Arc",(255,0,0),((0,0,64,64),math.radians(0),math.radians(360)),2)
    ov.copy()
    hpr = hprogressWidget(id="Hello", parent=vl,style={
    "Text":"variablestr",
    "W":"dw",
    "H":32,
    "Background":"lgrey",
    "Color":"cornflowerblue",
    "FillValue": """sl.rx/sl.w""",
    "Round":(25,25,25,25),
    "Flip":False
    })
    tb = textBoxWidget("TextBox",hl1,style={
    "Text":"Type!",
    "Color":"black",
    "InactiveColor":"grey",
    "ActiveColor":"lgrey",
    "Background":None
    })
    tbt = textWidget(id="Hello", parent=tb,style={
    "Text":"self.parentref.mytext if self.parentref.mytext != '' else self.parentref.text",
    "Justification":"left top",
    "W":"self.textboxw(64)",
    "H":"self.textboxh(32)",
    "Color":"white",
    "Wrap":128,
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    },
    "Background":"self.parentref.dbackground"
    })
    cb = checkWidget(id="Check",parent=hl1,style={
    "W":64,
    "H":64
    })
    hl2 = hlistWidget("Hi1234",vl,style={
    "W":"dw"
    })
    hwt = textWidget(id="HelloTwo", parent=sl, style={
    "Text":"Hello World Nice To See You",
    "Justification":"left top",
    "Wrap":256
    })
    ov2 = overlayWidget("Hi1212", parent=vl, style={})
    imb = textWidget(id="HelloTwo", parent=ov2, style={
    "Text":"",
    "Color":"black",
    "W":64,
    "H":64,
    "Background":"white",
    "Round":(32,32,32,32)
    })
    i = imageWidget(id="Image", parent=ov2, style={
    "W":64,
    "H":64,
    "Image":"img_file"
    })
    hlw = hlistWidget(id="RadioList", parent=vl, style={})
    r = radioWidget(id="randid", parent=hlw, style={
    "Color":"black",
    "ActiveColor":"lyellow",
    "InActiveColor":"White",
    "W":16,
    "H":16
    })
    r.copy(newid="randid")
    r.copy(newid="randid")
    r.copy(newid="randid")
    w = canvasWidget("Canvas", parent=vl, style={
    "W":56,
    "H":56,
    "Background":"white"
    })
    sw = switchWidget(id="Switch",parent=vl,style={
    "W":32,
    "H":32,
    "Round":(16,16,16,16),
    "ActiveColor":"lred",
    "Background":"white",
    "Gradient":{
    "base":"red",
    "end":"yellow",
    "types":"background",
    "inverse":"self.active",
    "vert":False,
    "flip":False
    }
    })
    #c.draw("Line",(255,0,0),((0,0),(25,25)),25)
    #c.draw("Arc",(255,0,0),((25,25,55,55),math.radians(25),math.radians(255)),5)
    #c.draw("Ellipse",(255,0,0),((55,55,55,55)),10)
    w.draw("Polygon",(255,0,0),((25,25),(52,52),(52,25)),2)
    g = graphWidget("Graph", vl, style={
    "W":72,
    "H":72
    })
    fg = screen.find("Graph")
    fg.linepoint(1, 1)
    fg.linepoint(1, 2)
    g2 = g.copy()
    g2.linepoint(2, 2)
    drag = dragSnaplessWidget("Drag", vl, style={
    "W":64,
    "H":32
    })
    imb2 = textWidget(id="HelloTwo", parent=drag, style={
    "Text":"Hello",
    "Color":"black",
    "W":64,
    "H":32,
    "Background":"white",
    "Round":(16,16,16,16),
    "Margin":(0,0,0,0),
    "Border":{
    "color":"white",
    "width":-1,
    "round":1
    }
    })
    drop = dropWidget("Drop", vl, style={
    "W":64,
    "H":32,
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    }
    })
    drop1 = dropWidget("Drop1", vl, style={
    "W":64,
    "H":32,
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    }
    })
    drop2 = dropWidget("Drop2", vl, style={
    "W":64,
    "H":32,
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    }
    })
    abs = absDrawWidget(id="Draw", parent=vl, style={})
    t2 = textWidget(id="Hello", parent=abs,style={
    "Text":"Hello",
    "Justification":"left top",
    "ABSX":100,
    "ABSY":100,
    "Color":"black",
    "Wrap":128,
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":5,
    "round":1
    },
    "Background":"white"
    })
    render()
    #imageWidget(id="Image",parent="Hi",x=0,y=0,color=white,activecolor=white,
    #text="Hi",image="assets/checkmark.png",style={"H":dh,"W":dw})

    quit()

if __name__ == '__main__' and False:
    htmltogui.setup(gameDisplay)

    screen = htmltogui.openfile("./guis/testhtml/test.html")
    render()

if __name__ == '__main__' and False:
    gameDisplay.fill(blue)
    pygame.display.update()
    screen = mainWidget("blue",inglobals=globals(),style={},data={})
    vl = vlistWidget("vl",screen,style={
    "H":dh,
    "W":750
    })
    vl.ovy = "auto"
    t = textWidget(id="Text", parent=vl,style={
    "Text":"Ok. jskkskskskksksksksksksksksksksksksksk",
    "Color":"black",
    "Background":None,
    "W":750,
    "H":32
    })
    i = imageWidget(id="Image", parent=vl, style={
    "W":64,
    "H":64,
    "Image":"img_file",
    "Angle":"int(variabletest)"
    })
    for x in range(0):
        t.copy()
        i.copy()
    #vlistWidget("Hi3","Hi2",0,0,red,grey,style={"W":"self.hfill()"})
    #surfaceWidget("HI",25,25,25,25,"main",white)
    #c.draw("Line",(255,0,0),((0,0),(25,25)),25)
    #c.draw("Arc",(255,0,0),((25,25,55,55),math.radians(25),math.radians(255)),5)
    #c.draw("Ellipse",(255,0,0),((55,55,55,55)),10)
    render()
    #imageWidget(id="Image",parent="Hi",x=0,y=0,color=white,activecolor=white,
    #text="Hi",image="assets/checkmark.png",style={"H":dh,"W":dw})
    quit()

if __name__ == '__main__' and True:
    screen = mainWidget("blue",inglobals=globals(),style={},data={})
    l = vlistWidget("hvl",screen,style={
    "W":"dw-8",
    "H":"dh-8"
    })
    l.ovx="auto"
    l.ovy="auto"
    tb = textBoxWidget("TextBox",l,style={
    "Text":"Type!",
    "Color":"black",
    "InactiveColor":"grey",
    "ActiveColor":"lgrey",
    "Background":None,
    "W":"self.hfitchildren()",
    "H":"self.vfitchildren()"
    })
    tbt = textWidget(id="Hello", parent=tb,style={
    "Text":"self.parentref.getText()",
    "Justification":"left top",
    "W":"self.textboxw(64,256)",
    "H":"self.textboxh(32,256)",
    "Color":"white",
    "Wrap":128,
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    },
    "Background":"self.parentref.dbackground"
    })
    textWidget("Text",None,style={
        "Text":"Hello",
        "W":64,
        "H":32
    })
    emptyWidget("Goon",l,style={
    "H":16,
    "W":32,
    "Background":"red",
    "Margin":(32,32,32,32),
    "Padding":(32,32,32,32),
    "Border":{
    "color":"green",
    "width":2
    }
    })
    hl = hlistWidget("hl",l,style={
    "W":"self.parentref.w",
    "H":256,
    "Background":"dred"
    })
    dropWidget("S",hl,style={
    "W":128,
    "H":64,
    "Background":"red"
    })
    vl = vlistWidget("Scroll",hl,style={
    "W":512,
    "H":256,
    "Margin":(32,32,32,32),
    "Padding":(0,0,0,0),
    "Background":"black",
    "Border":{
    "color":"green",
    "width":5,
    "round":1
    }})
    vl.ovx="scroll"
    vl.ovy="scroll"
    #vl.display = "vlist"
    vl.wrapwidth = 256
    vl.wrap = 128
    drop = dropdown("Text",vl,style={
    "activecolor":"black","inactivecolor":"None","background":"None","Color":"white"},defualt="Hi")
    drop.addoption("Hi")
    drop.addoption("hello")
    drop.addoption("Hola")
    imageWidget("Text",vl,style={
        "Text":"",
        "W":128,
        "H":128,
        "round":(25,25,25,25),
        "activecolor":"red",
        "color":(255,255,255)
    })
    radioWidget("Text",vl,style={
        "Text":"",
        "W":128,
        "H":64,
        "round":(25,25,25,25),
        "activecolor":"red",
        "color":(255,255,255)
    })
    radioWidget("Text",vl,style={
        "Text":"",
        "W":128,
        "H":64,
        "round":(25,25,25,25),
        "activecolor":"red",
        "color":(255,255,255)
    })
    radioWidget("Text",vl,style={
        "Text":"",
        "W":128,
        "H":64,
        "round":(25,25,25,25),
        "activecolor":"red",
        "color":(255,255,255)
    })
    render()

if(__name__=="__main__" and False):
    screen = mainWidget("blue",inglobals=globals(),style={},data={})
    l = vlistWidget("hvl",screen,style={
    "W":"dw-8",
    "H":"dh-8"
    })
    l.ovx="auto"
    l.ovy="auto"
    tb = textBoxWidget("TextBox",l,style={
    "Text":"Type!",
    "Color":"black",
    "InactiveColor":"grey",
    "ActiveColor":"lgrey",
    "Background":None,
    "W":"self.hfitchildren()",
    "H":"self.vfitchildren()"
    })
    tbt = textWidget(id="Hello", parent=tb,style={
    "Text":"self.parentref.getText()",
    "Justification":"left top",
    "W":"self.textboxw(64,256)",
    "H":"self.textboxh(32,256)",
    "Color":"white",
    "Wrap":128,
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    },
    "Background":"self.parentref.dbackground"
    })
    textWidget("Text",None,style={
        "Text":"Hello",
        "W":64,
        "H":32
    })
    slider = sliderWidget(id="-scrolly", parent=l, style={
    "Background":"dgrey",
    "W":128,
    "H":128,
    "InactiveColor":"grey",
    "ActiveColor":"lgrey",
    "Slider":{
        "x":0,
        "w":12,
        "h":"64",
        "y":8,
        "dw":2,
        "wo":8,
        "dh":8,
        "ho":12,
        "inc":1,
        "drawinc":5,
        "notch":[]
    }}, data={"Test"})
    barx = emptyWidget(id="-BarX", parent=slider, style={
    "Text":"",
    "Color":"black",
    "H":8,
    "W":12,
    "Background":"grey",
    "Round":(5,5,5,5)
    })
    render()
